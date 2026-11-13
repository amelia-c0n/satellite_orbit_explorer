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

## Setup and run (checklist)

1. `cd satellite_orbit_explorer`
2. `python3 -m venv .venv` (first time only)
3. `source .venv/bin/activate`
4. `pip install -r requirements.txt` (first time / when deps change)
5. `python orbit_explorer.py`
6. Find outputs in `satellite_orbit_explorer/data/output/`
7. Optional: open `satellite_orbit_outputs.zip` or the individual PNG / KML / report files

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

## Orbit summary (Stage 6)

Approximate two-body values from the workshop GP records:

| Satellite | What the numbers mean |
|-----------|------------------------|
| **PULSAR-0** | Period ~**1.58 h**, inclination ~**97.5°** → retrograde, near-polar, sun-synchronous-class LEO |
| **Galileo 29** | Period ~**14.08 h** → medium Earth / GNSS |
| **SES-5** | Period ~**23.93 h** (≈ one sidereal day), near-equatorial → geostationary-like |
| **QZS-2** | Period ~**23.93 h**, but **e ~ 0.07** and **i ~ 39°** → inclined geosynchronous (**IGSO**), not geostationary |

## Plots (Stage 7)

Saved under `satellite_orbit_explorer/data/output/`:

- `ground_tracks.png` — coastline + scatter ground tracks (scatter avoids fake lines across ±180°)
- `velocity_timeseries.png` — speed vs UTC time, one panel per satellite

**How to read the ground tracks**
- **PULSAR-0:** many passes shifting west (fast LEO + Earth rotating underneath)
- **Galileo 29:** a wide wave (MEO)
- **SES-5:** essentially one spot — period ≈ Earth’s rotation (geostationary-like)
- **QZS-2:** asymmetric figure-8 — same ~sidereal-day period, but inclination ~39° and a slow northern apogee (IGSO)

**How to read the speed plots:** eccentric orbits (especially QZS-2) go faster near perigee and slower near apogee.

## KML + report (Stage 8)

Also written under `satellite_orbit_explorer/data/output/`:

| File | What it is |
|------|------------|
| `orbit_tracks_ecef.kml` | 3D Earth-fixed orbits (`LineString`, absolute altitude in metres) |
| `orbit_animation.kml` | Ground-track animation (`gx:MultiTrack`, clamp to ground, 60 s steps) |
| `orbit_report.txt` | Text report: source note, window, summary + elements tables |
| `satellite_orbit_outputs.zip` | All five deliverables (2 PNG + 2 KML + report) |

### Open in Google Earth Pro

1. Install / open [Google Earth Pro](https://www.google.com/earth/versions/#earth-pro)
2. **File → Open** and choose `orbit_tracks_ecef.kml` to see the 3D orbit lines in space
3. Open `orbit_animation.kml` for the moving ground-track animation
4. Use the time slider / animation controls at the top of Earth Pro to **play** the tracks
5. Toggle placemarks in the Places panel to show/hide individual satellites

Colours match the Matplotlib figures (blue / orange / green / red).
