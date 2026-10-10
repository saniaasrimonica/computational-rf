"""RF reference-case validation using Python's standard library.
Run: python validate_rf_metrics.py
Valid for finite passive loads with positive resistance and real Z0 > 0.
This checks independent analytic cases; it does not test notebook file execution.
"""
import math
import unittest


def rf_metrics(z_load, z0=50.0):
    z_load = complex(z_load)
    if not math.isfinite(z0) or z0 <= 0:
        raise ValueError("Reference impedance must be finite and positive")
    if not (math.isfinite(z_load.real) and math.isfinite(z_load.imag)) or z_load.real <= 0:
        raise ValueError("Load must be finite with positive resistance")
    magnitude = abs((z_load - z0) / (z_load + z0))
    if magnitude >= 1:
        raise ValueError("Load is numerically indistinguishable from full reflection")
    return {
        "gamma_magnitude": magnitude,
        "s11_db": 20 * math.log10(magnitude) if magnitude else -math.inf,
        "vswr": (1 + magnitude) / (1 - magnitude),
        "mismatch_loss_db": -10 * math.log10(1 - magnitude**2),
    }


class RFReferenceTests(unittest.TestCase):
    def test_matched_load(self):
        m = rf_metrics(50)
        self.assertEqual(m["gamma_magnitude"], 0)
        self.assertEqual(m["s11_db"], -math.inf)
        self.assertEqual(m["vswr"], 1)
        self.assertEqual(m["mismatch_loss_db"], 0)

    def test_75_ohm_load(self):
        m = rf_metrics(75)
        self.assertAlmostEqual(m["gamma_magnitude"], 0.2)
        self.assertAlmostEqual(m["s11_db"], -13.9794000867)
        self.assertAlmostEqual(m["vswr"], 1.5)
        self.assertAlmostEqual(m["mismatch_loss_db"], 0.1772876696)

    def test_complex_load(self):
        # 50+j50 ohms gives Gamma=(1+j2)/5, |Gamma|^2=1/5.
        m = rf_metrics(50 + 50j)
        self.assertAlmostEqual(m["gamma_magnitude"]**2, 0.2)
        self.assertAlmostEqual(m["mismatch_loss_db"], -10 * math.log10(0.8))

    def test_rlc_resonance(self):
        f0, inductance = 2.4e9, 5e-9
        omega = 2 * math.pi * f0
        capacitance = 1 / (omega**2 * inductance)
        reactance = omega * inductance - 1 / (omega * capacitance)
        self.assertAlmostEqual(reactance, 0)
        self.assertAlmostEqual(rf_metrics(60 + 1j * reactance)["vswr"], 1.2)

    def test_invalid_inputs(self):
        for z_load, z0 in [(-10, 50), (50, 0), (complex(float("nan"), 0), 50)]:
            with self.assertRaises(ValueError):
                rf_metrics(z_load, z0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
