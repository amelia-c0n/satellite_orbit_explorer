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
