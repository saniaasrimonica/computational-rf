"""Synthetic component tolerance study, not measured manufacturing yield.
Uniform independent +/-5% R,L,C tolerances; seed 42; 10,000 trials.
Acceptance: S11 <= -10 dB at 2.4 GHz only, not across a bandwidth.
"""
import numpy as np
import pandas as pd
from rf_core import rlc_gamma

def main():
    rng=np.random.default_rng(42);count=10000;f0=2.4e9;l0=5e-9;c0=1/((2*np.pi*f0)**2*l0)
    r=60*rng.uniform(.95,1.05,count);l=l0*rng.uniform(.95,1.05,count);c=c0*rng.uniform(.95,1.05,count)
    w=2*np.pi*f0;z=r+1j*(w*l-1/(w*c));g=(z-50)/(z+50)
    db=20*np.log10(np.abs(g)); passed=db<=-10
    fraction=passed.mean();se=np.sqrt(fraction*(1-fraction)/count)
    print("Acceptance fraction under these assumptions:",fraction)
    print("Binomial standard error:",se)
    print("S11 percentiles 5/50/95 (dB):",np.percentile(db,[5,50,95]))
    pd.DataFrame(dict(resistance_ohm=r,inductance_H=l,capacitance_F=c,S11_dB=db,accepted=passed)).to_csv("tolerance_results.csv",index=False)
if __name__=="__main__":main()
