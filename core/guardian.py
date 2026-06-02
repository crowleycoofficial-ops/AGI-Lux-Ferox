"""
core/guardian.py

Hard-science constraint guard for information pipelines.

The guard deliberately ignores message semantics. It only uses measurable
system quantities such as compute load, arrival frequency, and sampling
capacity. This makes it suitable as a physical/operational safety layer
around higher-level information engines: when the pipeline is overloaded or the
input cadence exceeds the sampling envelope, the guard throttles or discards
packets before semantic processing can amplify a feedback loop.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
import time
from typing import Iterable, Literal


GuardAction = Literal["PASS", "THROTTLE", "DISCARD"]


@dataclass(frozen=True)
class SignalDecision:
    """Decision emitted by :class:`HardScienceGuardian` for one signal packet.

    Attributes:
        action: Physical control action. ``PASS`` forwards the packet,
            ``THROTTLE`` injects latency, and ``DISCARD`` shunts the packet.
        reason: Machine-readable explanation based only on physical metrics.
        compute_load: Normalized compute load in the range ``[0, +inf)``.
        arrival_hz: Input event frequency in hertz.
        nyquist_limit_hz: Maximum resolvable input frequency given the current
            sampling rate, equal to ``sampling_hz / 2``.
        latency_seconds: Latency the caller should inject for ``THROTTLE``.
        overload_active: Whether the hysteresis latch is currently in overload.
        payload_forwarded: ``False`` when the packet was discarded.
    """

    action: GuardAction
    reason: str
    compute_load: float
    arrival_hz: float
    nyquist_limit_hz: float
    latency_seconds: float
    overload_active: bool
    payload_forwarded: bool


class HardScienceGuardian:
    """Semantic-agnostic guard based on load and sampling constraints.

    The guardian implements two physical controls:

    1. Load hysteresis: when ``compute_load`` crosses ``threshold_load``, the
       overload latch activates and emits ``THROTTLE`` until load falls below
       ``threshold_load - hysteresis``.
    2. Nyquist shunt: when the observed arrival frequency is greater than half
       the sampling frequency, the packet is discarded to avoid aliasing in the
       downstream discrete-time pipeline.

    No message text, labels, truth claims, or sociological consensus signals are
    inspected by this class.
    """

    def __init__(
        self,
        threshold_load: float = 0.85,
        sampling_hz: float = 1_000.0,
        latency_penalty: float = 0.5,
        hysteresis: float = 0.05,
    ) -> None:
        if threshold_load <= 0:
            raise ValueError("threshold_load must be positive.")
        if sampling_hz <= 0:
            raise ValueError("sampling_hz must be positive.")
        if latency_penalty < 0:
            raise ValueError("latency_penalty cannot be negative.")
        if hysteresis < 0:
            raise ValueError("hysteresis cannot be negative.")
        if hysteresis >= threshold_load:
            raise ValueError("hysteresis must be smaller than threshold_load.")

        self.threshold_load = float(threshold_load)
        self.sampling_hz = float(sampling_hz)
        self.latency_penalty = float(latency_penalty)
        self.hysteresis = float(hysteresis)
        self._overload_active = False

    @property
    def nyquist_limit_hz(self) -> float:
        """Maximum resolvable input frequency under Nyquist-Shannon."""
        return self.sampling_hz / 2.0

    def process_signal(
        self,
        compute_load: float,
        arrival_hz: float,
        *,
        apply_latency: bool = False,
    ) -> SignalDecision:
        """Classify one packet using only physical pipeline measurements.

        Args:
            compute_load: Normalized hardware or runtime load. Values above
                ``threshold_load`` trigger throttling.
            arrival_hz: Packet/event arrival rate in hertz.
            apply_latency: If true, the method sleeps for ``latency_penalty``
                seconds when a throttle action is emitted. The default returns
                the latency budget without sleeping, which is friendlier to tests
                and async services.

        Returns:
            A :class:`SignalDecision` containing the action and metrics.
        """
        compute_load = self._validate_non_negative(compute_load, "compute_load")
        arrival_hz = self._validate_non_negative(arrival_hz, "arrival_hz")

        self._update_overload_latch(compute_load)

        if arrival_hz > self.nyquist_limit_hz:
            return SignalDecision(
                action="DISCARD",
                reason="NYQUIST_ALIASING_RISK",
                compute_load=compute_load,
                arrival_hz=arrival_hz,
                nyquist_limit_hz=self.nyquist_limit_hz,
                latency_seconds=0.0,
                overload_active=self._overload_active,
                payload_forwarded=False,
            )

        if self._overload_active:
            if apply_latency and self.latency_penalty > 0:
                time.sleep(self.latency_penalty)
            return SignalDecision(
                action="THROTTLE",
                reason="COMPUTE_LOAD_HYSTERESIS",
                compute_load=compute_load,
                arrival_hz=arrival_hz,
                nyquist_limit_hz=self.nyquist_limit_hz,
                latency_seconds=self.latency_penalty,
                overload_active=True,
                payload_forwarded=True,
            )

        return SignalDecision(
            action="PASS",
            reason="WITHIN_PHYSICAL_ENVELOPE",
            compute_load=compute_load,
            arrival_hz=arrival_hz,
            nyquist_limit_hz=self.nyquist_limit_hz,
            latency_seconds=0.0,
            overload_active=False,
            payload_forwarded=True,
        )

    def process_stream(
        self,
        compute_loads: Iterable[float],
        arrival_rates_hz: Iterable[float],
    ) -> list[SignalDecision]:
        """Process a finite stream of load/rate measurements."""
        return [
            self.process_signal(load, rate)
            for load, rate in zip(compute_loads, arrival_rates_hz)
        ]

    def reset(self) -> None:
        """Clear the overload hysteresis latch."""
        self._overload_active = False

    def _update_overload_latch(self, compute_load: float) -> None:
        if compute_load >= self.threshold_load:
            self._overload_active = True
        elif compute_load <= self.threshold_load - self.hysteresis:
            self._overload_active = False

    @staticmethod
    def _validate_non_negative(value: float, name: str) -> float:
        value = float(value)
        if not math.isfinite(value):
            raise ValueError(f"{name} must be finite.")
        if value < 0:
            raise ValueError(f"{name} cannot be negative.")
        return value


if __name__ == "__main__":
    print("=" * 60)
    print("core/guardian.py - Unit Tests")
    print("=" * 60)

    guardian = HardScienceGuardian(
        threshold_load=0.85,
        sampling_hz=100.0,
        latency_penalty=0.0,
        hysteresis=0.05,
    )

    nominal = guardian.process_signal(compute_load=0.50, arrival_hz=10.0)
    assert nominal.action == "PASS"
    assert nominal.payload_forwarded is True
    print("Test 1 PASSED: nominal signal passes")

    overloaded = guardian.process_signal(compute_load=0.90, arrival_hz=10.0)
    assert overloaded.action == "THROTTLE"
    assert overloaded.overload_active is True
    print("Test 2 PASSED: overload triggers throttle")

    latched = guardian.process_signal(compute_load=0.82, arrival_hz=10.0)
    assert latched.action == "THROTTLE"
    assert latched.overload_active is True
    print("Test 3 PASSED: hysteresis keeps throttle active")

    cooled = guardian.process_signal(compute_load=0.70, arrival_hz=10.0)
    assert cooled.action == "PASS"
    assert cooled.overload_active is False
    print("Test 4 PASSED: cooled pipeline returns to pass")

    aliased = guardian.process_signal(compute_load=0.50, arrival_hz=75.0)
    assert aliased.action == "DISCARD"
    assert aliased.payload_forwarded is False
    assert aliased.reason == "NYQUIST_ALIASING_RISK"
    print("Test 5 PASSED: Nyquist aliasing risk discards packet")

    batch = guardian.process_stream([0.1, 0.9], [1.0, 1.0])
    assert [decision.action for decision in batch] == ["PASS", "THROTTLE"]
    print("Test 6 PASSED: stream processing returns ordered decisions")

    print("=" * 60)
    print("All guardian tests passed.")
    print("=" * 60)
