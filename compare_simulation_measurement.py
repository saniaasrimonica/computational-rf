"""Compare CSVs with frequency_Hz,S11_dB columns within their shared range.
python compare_simulation_measurement.py simulated.csv measured.csv
Interpolation is in dB, not complex S-parameters; error is descriptive.
"""
import argparse
import numpy as np
import pandas as pd

def load(path):
    d=pd.read_csv(path)[["frequency_Hz","S11_dB"]].astype(float).sort_values("frequency_Hz")
    if len(d)<2 or not np.isfinite(d.to_numpy()).all() or d.frequency_Hz.duplicated().any():
        raise ValueError("Need at least two finite unique frequency points")
    return d

def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument("simulation");p.add_argument("measurement");a=p.parse_args()
    s,m=load(a.simulation),load(a.measurement)
    lo=max(s.frequency_Hz.min(),m.frequency_Hz.min());hi=min(s.frequency_Hz.max(),m.frequency_Hz.max())
    q=m[(m.frequency_Hz>=lo)&(m.frequency_Hz<=hi)].copy()
    if len(q)<2: raise ValueError("Insufficient overlap")
    q["simulation_dB"]=np.interp(q.frequency_Hz,s.frequency_Hz,s.S11_dB)
    q["error_dB"]=q.S11_dB-q.simulation_dB
    print("RMSE (dB):",np.sqrt(np.mean(q.error_dB**2)))
    print("Maximum absolute difference (dB):",q.error_dB.abs().max())
    q.to_csv("comparison_results.csv",index=False)
if __name__=="__main__":main()
