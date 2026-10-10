"""Ideal isotropic uniform linear array, angle measured from broadside.
No coupling, element pattern, or hardware losses. python array_beamforming.py
"""
import numpy as np
import pandas as pd
from scipy.signal import find_peaks

def pattern(theta_deg,steer_deg=20,n=16,spacing_lambda=0.5):
    theta=np.deg2rad(np.asarray(theta_deg)); steer=np.deg2rad(steer_deg)
    phase=2*np.pi*spacing_lambda*(np.sin(theta)-np.sin(steer))
    return np.abs(np.exp(1j*np.outer(phase,np.arange(n))).mean(axis=1))

def main():
    theta=np.linspace(-90,90,36001);a=pattern(theta);k=np.argmax(a)
    nulls,_=find_peaks(-a)
    left=nulls[nulls<k];right=nulls[nulls>k]
    if not len(left) or not len(right):raise ValueError("Cannot bound main lobe")
    l,r=left[-1],right[0]
    sidelobe=np.max(np.r_[a[:l],a[r+1:]])
    above=np.flatnonzero(a[l:r+1]>=a[k]/np.sqrt(2))+l
    print("Steering peak (deg):",theta[k])
    print("Approximate 3 dB beamwidth (deg):",theta[above[-1]]-theta[above[0]])
    print("Peak sidelobe relative to main peak (dB):",20*np.log10(sidelobe/a[k]))
    pd.DataFrame(dict(angle_deg=theta,normalized_amplitude=a)).to_csv("array_pattern.csv",index=False)
if __name__=="__main__":main()
