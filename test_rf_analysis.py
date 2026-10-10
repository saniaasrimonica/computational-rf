import unittest
import numpy as np
from rf_core import metrics,bands,rlc_gamma
from array_beamforming import pattern
from matching_optimization import reflection

class RFTests(unittest.TestCase):
    def test_75ohm(self):
        db,v,loss=metrics([.2]);self.assertAlmostEqual(db[0],-13.9794000867);self.assertAlmostEqual(v[0],1.5)
    def test_matched(self):
        db,v,loss=metrics([0]);self.assertTrue(np.isneginf(db[0]));self.assertEqual(v[0],1);self.assertEqual(loss[0],0)
    def test_invalid(self):
        with self.assertRaises(ValueError):metrics([1.1])
    def test_separate_bands(self):
        b=bands([1,2,3,4,5],[-5,-15,-5,-15,-5]);self.assertEqual([(x[0],x[1]) for x in b],[(1.5,2.5),(3.5,4.5)])
    def test_edge_band(self):
        self.assertEqual(bands([1,2],[-15,-15]),[(1.,2.,True,True)])
    def test_frequency_validation(self):
        with self.assertRaises(ValueError):bands([2,1],[-15,-5])
    def test_resonance(self):
        f=2.4e9;l=5e-9;c=1/((2*np.pi*f)**2*l);self.assertAlmostEqual(abs(rlc_gamma([f],60,l,c)[0]),1/11)
    def test_steering(self):
        self.assertAlmostEqual(pattern([20])[0],1.)
    def test_analytic_match(self):
        # 100||(-j100) = 50-j50; series +j50 matches at f0.
        f=2.4e9;w=2*np.pi*f
        self.assertLess(abs(reflection([50/w*1e9,1/(100*w)*1e12],np.array([f]))[0]),1e-12)
if __name__=="__main__":unittest.main(verbosity=2)
