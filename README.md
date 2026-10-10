# Computational RF toolkit
Educational RF engineering portfolio examples. Synthetic models are clearly separated from measurements. These examples do not establish professional seniority.

## Setup
Python 3.10 or newer:
```bash
python -m venv .venv
# Ubuntu: source .venv/bin/activate
# Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
python -m unittest -v test_rf_analysis
```
Dependencies are not pinned: after verifying your local environment, record it with `python -m pip freeze > requirements-lock.txt`.

## Run
```bash
python array_beamforming.py
python matching_optimization.py
python monte_carlo_tolerance.py
python compare_simulation_measurement.py simulated.csv measured.csv
python touchstone_analysis.py antenna.s1p
```
Sample CSVs are synthetic 50-ohm-reference RLC reflections in dB. `antenna.s1p` must be your own Touchstone data. Touchstone processing requires scikit-rf and rejects full-reflection/active magnitudes for finite VSWR analysis. A measured PRX/gain spreadsheet is not an S11 input.

## Methods and limits
- S11 = 20 log10(|Gamma|), VSWR = (1+|Gamma|)/(1-|Gamma|).
- Mismatch loss = -10 log10(1-|Gamma|^2), not total antenna efficiency.
- Threshold bands use linear crossing interpolation in dB and identify scan-edge truncation.
- Comparison interpolates simulated dB values onto measured frequencies only in their overlap; it is not complex network interpolation.
- Array analysis assumes isotropic elements without coupling, ideal phase control, and half-wavelength spacing. Beamwidth uses a finite angular grid.
- Matching minimizes worst reflection on a sampled band using ideal L/C, then verifies on a denser grid. It does not guarantee a global continuous-frequency optimum or account for component Q.
- Monte Carlo acceptance concerns one frequency and chosen independent uniform tolerances. It is not measured production yield.

Validation covers analytic impedances, resonance, separate bands, scan limits, invalid inputs, steering, and an exact L-match case. Tests exercise shared core calculations. A separate end-to-end run with scikit-rf is needed for Touchstone processing.
