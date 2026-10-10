"""Analyze a Touchstone file: python touchstone_analysis.py antenna.s1p"""
import argparse
import numpy as np
import pandas as pd
import skrf as rf
from rf_core import metrics, bands

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file"); args=parser.parse_args()
    network=rf.Network(args.file)
    f=network.f; s=network.s[:,0,0]
    db,vswr,loss=metrics(s)
    pd.DataFrame(dict(frequency_Hz=f,S11_dB=db,VSWR=vswr,mismatch_loss_dB=loss)).to_csv("touchstone_results.csv",index=False)
    i=np.argmin(db)
    print(f"Minimum S11: {db[i]:.3f} dB at {f[i]/1e9:.6f} GHz")
    # Exact matched points have -inf dB; clip solely for crossing interpolation.
    for lo,hi,left,right in bands(f,np.maximum(db,-300)):
        print(f"Band: {lo/1e9:.6f}–{hi/1e9:.6f} GHz; edge-limited: {left or right}")
if __name__=="__main__": main()
