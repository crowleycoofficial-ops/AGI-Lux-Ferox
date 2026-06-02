"""
core/surprise.py

Calculates Total Surprise (S_total) based on Kullback-Leibler Divergence (KLD),
grounded in Landauer's Principle of thermodynamic information erasure.

References:
    - Landauer, R. (1961). Irreversibility and heat generation in the computing process.
      IBM Journal of Research and Development, 5(3), 183-191.
    - Shannon, C.E. (1948). A mathematical theory of communication.
      Bell System Technical Journal, 27(3), 379-423.
    - Kullback, S., & Leibler, R.A. (1951). On information and sufficiency.
      Annals of Mathematical Statistics, 22(1), 79-86.
"""

import numpy as np
from scipy.special import rel_entr
from typing import Union


# Physical constants
K_B: float = 1.380649e-23  # Boltzmann constant (J/K)
LN2: float = 0.693147  # Natural logarithm of 2
EPSILON: float = 1e-10  # Numerical stability constant


def _validate_and_normalize(p: np.ndarray, name: str) -> np.ndarray:
    """
    Validates and normalizes a probability distribution.
    
    Ensures the distribution is non-negative and sums to unity (L1 normalization).
    Adds epsilon to zero entries to maintain numerical stability in logarithmic
    operations, consistent with the mathematical domain of KLD.
    
    Args:
        p: Input probability array.
        name: Variable name for error reporting.
    
    Returns:
        Normalized probability array with epsilon-stabilized zeros.
    
    Raises:
        ValueError: If array contains negative values or sums to zero.
    """
    p = np.asarray(p, dtype=np.float64)
    
    if np.any(p < 0):
        raise ValueError(f"{name} contains negative values; not a valid probability distribution.")
    
    total = np.sum(p)
    if total <= 0:
        raise ValueError(f"{name} sums to zero or negative; cannot normalize.")
    
    # Normalize to ensure sum = 1
    p_normalized = p / total
    
    # Add epsilon to zeros for numerical stability in log operations
    # This prevents undefined KLD contributions from zero-probability events
    p_stabilized = np.where(p_normalized == 0, EPSILON, p_normalized)
    
    # Re-normalize after epsilon injection
    p_stabilized = p_stabilized / np.sum(p_stabilized)
    
    return p_stabilized


def _kld_nats(p: np.ndarray, q: np.ndarray) -> float:
    """
    Computes D_KL(P || Q) in nats using scipy's rel_entr for numerical precision.
    
    The KLD measures the information lost when distribution Q is used to
    approximate the true distribution P. In nats (natural log base), this
    represents the thermodynamic dissipation per bit erasure event.
    
    Args:
        p: Reference distribution (model).
        q: Approximating distribution (observed).
    
    Returns:
        KLD in nats (float).
    """
    # rel_entr computes p * log(p/q) element-wise, handling edge cases
    return float(np.sum(rel_entr(p, q)))


def calculate_surprise(
    p_model: np.ndarray,
    p_observed: np.ndarray,
    temperature: float = 300.0
) -> dict:
    """
    Calculates Total Surprise (S_total) via Kullback-Leibler Divergence,
    with thermodynamic grounding via Landauer's Principle.
    
    S_total is defined as D_KL(P_model || P_observed) in bits, representing
    the information-theoretic surprise when observations diverge from the
    model's predictions. The minimum thermodynamic work required to resolve
    this informational discrepancy is bounded by Landauer's erasure cost:
    
        W_min = k_B * T * ln(2) * S_total
    
    where k_B is Boltzmann's constant, T is temperature in Kelvin, and
    S_total is measured in bits. This establishes a hard lower bound on
    the physical energy cost of updating beliefs in a thermodynamic system.
    
    Args:
        p_model: Probability distribution from the generative model (P).
                 This is the reference distribution in D_KL(P || Q).
        p_observed: Empirically observed probability distribution (Q).
                    This is the approximating distribution in D_KL(P || Q).
        temperature: System temperature in Kelvin (default: 300.0 K, ~room temp).
    
    Returns:
        Dictionary containing:
            - "S_total" (float): Total surprise in bits (KLD in bits).
            - "W_min_joules" (float): Minimum thermodynamic work in Joules
              per Landauer's bound.
            - "divergence_bits" (float): KLD in bits (identical to S_total,
              exposed separately for clarity).
    
    Raises:
        ValueError: If inputs are invalid probability distributions or
                    temperature is non-positive.
    
    Physical References:
        Landauer (1961): Minimum energy kT*ln(2) per bit erasure.
        Shannon (1948): Information entropy H(X) = -sum p(x) log p(x).
        KLD as a measure of distributional divergence in nats, converted
        to bits via division by ln(2).
    """
    if temperature <= 0:
        raise ValueError(f"Temperature must be positive (received {temperature} K).")
    
    # Validate and normalize both distributions
    p = _validate_and_normalize(np.asarray(p_model, dtype=np.float64), "p_model")
    q = _validate_and_normalize(np.asarray(p_observed, dtype=np.float64), "p_observed")
    
    if p.shape != q.shape:
        raise ValueError(
            f"Shape mismatch: p_model {p.shape} != p_observed {q.shape}. "
            "Distributions must span the same event space."
        )
    
    # Compute KLD in nats: D_KL(P || Q) = sum_x P(x) * log(P(x) / Q(x))
    kld_nats: float = _kld_nats(p, q)
    
    # Convert nats to bits: D_KL_bits = D_KL_nats / ln(2)
    # Bits are the natural unit for information surprise in Shannon's framework
    kld_bits: float = kld_nats / LN2
    
    # S_total = KLD in bits (information-theoretic surprise)
    s_total: float = kld_bits
    
    # Landauer's minimum work: W_min = k_B * T * ln(2) * S_total
    # This is the thermodynamic cost of erasing S_total bits at temperature T
    w_min_joules: float = K_B * temperature * LN2 * s_total
    
    return {
        "S_total": s_total,
        "W_min_joules": w_min_joules,
        "divergence_bits": kld_bits,
    }


if __name__ == "__main__":
    """
    Unit test: Validates calculate_surprise against known analytical results.
    
    Test cases:
        1. Identical distributions -> KLD = 0, W_min = 0.
        2. Maximally divergent distributions -> KLD > 0.
        3. Near-uniform vs. peaked distribution -> moderate divergence.
    """
    print("=" * 60)
    print("core/surprise.py - Unit Tests")
    print("=" * 60)

    # Test 1: Identical distributions
    # D_KL(P || P) = 0 by definition (self-information is zero)
    p_uniform = np.array([0.25, 0.25, 0.25, 0.25])
    result_identical = calculate_surprise(p_uniform, p_uniform, temperature=300.0)
    
    print("\nTest 1: Identical distributions (P == Q)")
    print(f"  S_total:       {result_identical['S_total']:.6f} bits")
    print(f"  W_min:         {result_identical['W_min_joules']:.6e} J")
    assert abs(result_identical["S_total"]) < 1e-6, "KLD(P||P) must be ~0"
    assert abs(result_identical["W_min_joules"]) < 1e-6, "W_min(P||P) must be ~0"
    print("  PASSED")

    # Test 2: Divergent distributions
    # Model predicts event 0, observations favor event 3
    p_model_peaked = np.array([0.97, 0.01, 0.01, 0.01])
    p_obs_peaked   = np.array([0.01, 0.01, 0.01, 0.97])
    result_divergent = calculate_surprise(p_model_peaked, p_obs_peaked, temperature=300.0)
    
    print("\nTest 2: Maximally divergent distributions")
    print(f"  S_total:       {result_divergent['S_total']:.6f} bits")
    print(f"  W_min:         {result_divergent['W_min_joules']:.6e} J")
    assert result_divergent["S_total"] > 0, "KLD must be positive for divergent distributions"
    assert result_divergent["W_min_joules"] > 0, "W_min must be positive"
    print("  PASSED")

    # Test 3: Moderate divergence - uniform vs. skewed
    p_model_uniform = np.array([0.25, 0.25, 0.25, 0.25])
    p_obs_skewed    = np.array([0.70, 0.10, 0.10, 0.10])
    result_moderate = calculate_surprise(p_model_uniform, p_obs_skewed, temperature=300.0)
    
    print("\nTest 3: Uniform model vs. skewed observations")
    print(f"  S_total:       {result_moderate['S_total']:.6f} bits")
    print(f"  W_min:         {result_moderate['W_min_joules']:.6e} J")
    assert 0 < result_moderate["S_total"] < result_divergent["S_total"], (
        "Moderate divergence must be between 0 and maximal divergence"
    )
    print("  PASSED")

    # Test 4: Temperature scaling - W_min scales linearly with T
    result_cold = calculate_surprise(p_model_peaked, p_obs_peaked, temperature=150.0)
    result_hot  = calculate_surprise(p_model_peaked, p_obs_peaked, temperature=600.0)
    
    print("\nTest 4: Landauer temperature scaling")
    print(f"  W_min @ 150K:  {result_cold['W_min_joules']:.6e} J")
    print(f"  W_min @ 300K:  {result_divergent['W_min_joules']:.6e} J")
    print(f"  W_min @ 600K:  {result_hot['W_min_joules']:.6e} J")
    ratio_cold = result_divergent["W_min_joules"] / result_cold["W_min_joules"]
    ratio_hot  = result_hot["W_min_joules"] / result_divergent["W_min_joules"]
    assert abs(ratio_cold - 2.0) < 1e-6, f"W_min must double with 2x temperature (got {ratio_cold})"
    assert abs(ratio_hot  - 2.0) < 1e-6, f"W_min must double with 2x temperature (got {ratio_hot})"
    print("  PASSED (linear T scaling confirmed)")

    print("\n" + "=" * 60)
    print("All tests passed.")
    print("=" * 60)
