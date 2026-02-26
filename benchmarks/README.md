# Benchmarks

## Target Datasets

| Dataset | Domain          | Records   | Status       |
|---------|-----------------|-----------|--------------|
| SWaT    | Water treatment | 946,722   | Pending access (iTrust, SUTD) |
| WADI    | Water distribution | 1,048,571 | Pending access (iTrust, SUTD) |

## Protocol

S_total is computed per sliding window (width w, stride s) over the
multivariate sensor stream. KLD is calculated between the model's
predicted distribution P_model and the empirical window distribution
P_observed. Anomaly threshold τ is derived from the 99th percentile
of S_total on the training partition.

## Reproducing
```bash
python benchmarks/run_swat.py --window 60 --stride 1 --tau 0.99
```

Access credentials for SWaT/WADI must be obtained independently from
the iTrust lab (Singapore University of Technology and Design).
