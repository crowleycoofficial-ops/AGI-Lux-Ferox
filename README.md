# AGI-Lux-Ferox

**Thermodynamic Information Engine · TRL 3 → 4**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)]()

## Overview

Lux Ferox operationalises **Total Surprise** ($S_\text{total}$) as the
Kullback-Leibler divergence between a generative model and empirical
observations, bounded below by Landauer's erasure cost:

$$W_{\min} = k_B \, T \ln 2 \cdot S_{\text{total}}$$

The architecture targets a European sovereign hardware stack (CEA-Leti, Imec, X-FAB).

## Installation
```bash
git clone https://github.com/crowleycoofficial-ops/AGI-Lux-Ferox.git
cd AGI-Lux-Ferox
pip install numpy scipy
```

## Usage
```python
import numpy as np
from core import calculate_surprise

# Model distribution (prior belief)
p_model = np.array([0.7, 0.2, 0.1])

# Observed distribution (empirical)
p_obs = np.array([0.1, 0.3, 0.6])

result = calculate_surprise(p_model, p_observed=p_obs, temperature=300.0)

print(f"S_total :  {result['S_total']:.4f} bits")
print(f"W_min   :  {result['W_min_joules']:.4e} J")
```

## Running Unit Tests
```bash
python core/surprise.py
```
