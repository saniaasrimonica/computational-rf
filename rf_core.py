"""Reusable RF calculations. Frequency is Hz; S11 is complex amplitude."""
import numpy as np

def metrics(s11):
    g = np.abs(np.asarray(s11, dtype=complex))
    if np.any(~np.isfinite(g)) or np.any(g >= 1):
        raise ValueError("Expected finite passive reflection with magnitude below 1")
    with np.errstate(divide="ignore"):
        return 20*np.log10(g), (1+g)/(1-g), -10*np.log10(1-g*g)

def bands(f, y, threshold=-10):
    f, y = np.asarray(f, float), np.asarray(y, float)
    if len(f)<2 or f.shape!=y.shape or np.any(np.diff(f)<=0) or not np.all(np.isfinite(f)) or not np.all(np.isfinite(y)):
        raise ValueError("Expected finite aligned arrays with increasing frequencies")
    # Linear interpolation of crossings in dB, keeping separate bands separate.
    inside=y<=threshold
    result=[]; start=f[0] if inside[0] else None
    for i in range(1,len(f)):
        if inside[i]!=inside[i-1]:
            crossing=f[i-1]+(threshold-y[i-1])*(f[i]-f[i-1])/(y[i]-y[i-1])
            if inside[i]: start=crossing
            else: result.append((start,crossing,start==f[0],False)); start=None
    if start is not None: result.append((start,f[-1],start==f[0],True))
    return result

def rlc_gamma(f, resistance, inductance, capacitance, z0=50):
    f=np.asarray(f,float)
    if np.any(f<=0) or min(resistance,inductance,capacitance,z0)<=0:
        raise ValueError("Positive frequency and circuit parameters required")
    w=2*np.pi*f
    z=resistance+1j*(w*inductance-1/(w*capacitance))
    return (z-z0)/(z+z0)
