"""Bounded minimax series-L/shunt-C match of an illustrative 100-ohm load.
python matching_optimization.py
Component limits: L=0.1–20 nH, C=0.1–10 pF. Ideal lossless components.
"""
import numpy as np
from scipy.optimize import differential_evolution

def reflection(parameters,f):
    l_nh,c_pf=parameters;w=2*np.pi*f
    z=1j*w*l_nh*1e-9+1/(1/100+1j*w*c_pf*1e-12)
    return (z-50)/(z+50)

def main():
    f=np.linspace(2.3e9,2.5e9,401)
    objective=lambda q:np.max(np.abs(reflection(q,f)))
    result=differential_evolution(objective,[(0.1,20),(0.1,10)],seed=42,tol=1e-8)
    if not result.success:raise RuntimeError(result.message)
    dense=np.linspace(f[0],f[-1],4001)
    print("L (nH), C (pF):",result.x)
    print("Worst S11 on dense verification grid (dB):",20*np.log10(objective_dense(result.x,dense)))
    print("Unmatched S11 (dB):",20*np.log10(1/3))
def objective_dense(q,f):return np.max(np.abs(reflection(q,f)))
if __name__=="__main__":main()
