# Satellite Orbit Explorer | Amelia

Educational Python project from Space Career Week 2026 (GNSS Academy).  
We load real CelesTrak GP orbital data, explain how satellites move with a simple two-body model, compare orbits, and produce plots, a summary report, and a KML export.

**Note:** GP records are SGP4 mean elements. Our model is an educational approximation (Kepler two-body, spherical Earth, simple Greenwich rotation) — not precision orbit prediction.

## Stages

1. Setup
2. Load GP JSON
3. Parse elements
4. Time window
5. Propagate
6. Orbit summary
7. Plots
8. KML and report

## Setup and run

```bash
cd satellite_orbit_explorer
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python orbit_explorer.py
```

## Input data

Workshop inputs live in `input_data/orbit_workshop_inputs.zip` at the repo root.  
Running the script unpacks them into `satellite_orbit_explorer/data/input/`.  
Outputs go to `satellite_orbit_explorer/data/output/`.

A shorter file-side note also lives in `satellite_orbit_explorer/data/input/README.md`.

| File | Role |
|------|------|
| `orbital_elements.json` | Main science input: 4 CelesTrak GP JSON records (OMM field names) |
| `data_manifest.json` | Provenance: download URLs, epochs, matching TLEs, known limits |
| `world_map.txt` | Coastline points (`lat lon`) for ground-track map backgrounds |

**Satellites in the pack** (downloaded from CelesTrak on 2026-11-10):

| Name | NORAD ID | Rough orbit type |
|------|----------|------------------|
| PULSAR-0 | 64541 | Low Earth, near-polar |
| GSAT0225 (Galileo 29) | 59598 | Medium Earth / GNSS |
| SES-5 | 38652 | Near-equatorial, GEO-like |
| QZS-2 (Michibiki-2) | 42738 | Inclined, more eccentric |

**Teaching caveat:** QZS-2’s epoch is older (2026-10-17). Treat its common-window path as a stale-data example. Kepler use of GP mean elements is an educational approximation, not precision prediction.

**Why OMM JSON instead of old TLEs?** Named fields are easier to read than fixed-width TLE columns, and epochs use ISO-8601 dates. OMM JSON also supports six-digit catalog numbers that the classic 5-digit TLE format cannot store.

## GP fields → model symbols

GP values are **SGP4 mean elements**, so using them in a two-body Kepler model is approximate.

| GP field | Symbol | Conversion / unit |
|----------|--------|-------------------|
| MEAN_MOTION | n | rev/day → rad/s (`× 2π / 86400`) |
| (derived) | a | km via Kepler: `a = (μ / n²)^(1/3)` |
| ECCENTRICITY | e | already decimal (unitless) |
| INCLINATION | i | deg → rad |
| RA_OF_ASC_NODE | Ω (RAAN) | deg → rad |
| ARG_OF_PERICENTER | ω | deg → rad |
| MEAN_ANOMALY | M₀ | deg → rad |
| EPOCH | t₀ | ISO text → UTC datetime |

## Common time window

We use one shared UTC grid for plots and comparisons: from the newest epoch floored to UTC midnight, for `DURATION_HOURS`, sampled every `STEP_SECONDS`.

Each record is still propagated from **its own epoch**, so error grows as the window moves farther from that epoch. The workshop **QZS-2** record dates from **17 October 2026**, so it is flagged as a stale-data teaching example when the offset exceeds 7 days.

## Propagation (Stage 5)

We advance each orbit with two-body Kepler math, then rotate into Earth-fixed coordinates with GMST (simple Greenwich rotation) to get lat/lon/alt and vis-viva speed. SES-5 staying near about **5°E** is a sanity check that the GMST / rotation signs are right — not a forced longitude offset.
