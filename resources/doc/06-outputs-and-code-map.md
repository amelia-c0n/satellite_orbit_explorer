# 06 — Outputs & code map

Where theory shows up in files and functions. Main script:  
`satellite_orbit_explorer/orbit_explorer.py`

---

## Output files (`data/output/`)

| File | What it shows | Related theory |
|------|----------------|----------------|
| `ground_tracks.png` | lon/lat paths + coastlines | GMST + spherical lat/lon |
| `velocity_timeseries.png` | speed vs UTC | vis-viva; e drives swing |
| `orbit_tracks_ecef.kml` | 3D paths in space (absolute altitude) | inertial→ECEF position |
| `orbit_animation.kml` | Moving ground tracks in Google Earth | same lat/lon, time animation |
| `orbit_report.txt` | Tables + source note + window | elements + summary |
| `satellite_orbit_outputs.zip` | All five bundled | sharing / demo |

### Open KML in Google Earth Pro
1. File → Open → choose the `.kml`  
2. **Animation** file: use the **time slider / play** control  
3. **ECEF** file: zoom out for GEO-height lines; SES-5 is a tiny path far above Earth  
4. Places panel: toggle each satellite  

SES-5 looking “missing” usually means you’re looking for a long trail — it’s basically a **point**.

---

## Code map (theory → function)

### Setup & inputs
| Topic | Function / name |
|-------|------------------|
| Paths, μ, Earth radius, step/duration | constants at top; `print_configuration()` |
| Unzip workshop files | `extract_inputs()` |
| Load/validate GP JSON | `read_gp_json()` |
| Optional live group | `apply_live_group_if_requested()` |

### Elements & time
| Topic | Function |
|-------|----------|
| Epoch parse (UTC) | `parse_gp_epoch()` |
| a, e, i, Ω, ω, M, n | `parse_gp_elements()` |
| Print elements | `elements_table()` |
| Common UTC grid | `build_time_grid()` |
| Stale epoch warning | `print_epoch_offsets()` |

### Physics
| Topic | Function |
|-------|----------|
| Kepler equation M→E | `solve_kepler()` |
| Earth rotation angle | `gmst_rad()` |
| Full 7-step prediction | `propagate()` |
| Checks (GMST, SES-5, …) | `run_propagation_checks()` |

### Summary & plots
| Topic | Function |
|-------|----------|
| Period, peri/apo, vmin/vmax | `orbit_summary()`, `summary_table()` |
| Coastline segments | `load_coastline()` |
| Ground-track figure | `plot_ground_tracks()` |
| Speed figure | `plot_speed_timeseries()` |
| Colours | `COLORS` |

### Export
| Topic | Function |
|-------|----------|
| Matplotlib colour → KML aabbggrr | `matplotlib_color_to_kml_abgr()` |
| 3D orbit KML | `write_orbit_tracks_ecef_kml()` |
| Animated ground KML | `write_orbit_animation_kml()` |
| Text report | `write_orbit_report()` |
| Zip bundle | `zip_orbit_outputs()` |

---

## Constants worth remembering

| Name | Role |
|------|------|
| `MU_EARTH_KM3_S2` | Gravity parameter μ for Kepler / vis-viva |
| `EARTH_RADIUS_KM` | Spherical Earth radius for altitude |
| `STEP_SECONDS` | Time grid spacing (5) |
| `DURATION_HOURS` | Window length (24) |
| `LIVE_GROUP` | `None` = workshop; e.g. `"STATIONS"` = live |
| `ANIM_STEP_SECONDS` | KML animation sample (60) |

Units in this project: **km**, **km/s**, **UTC**.

---

## How to study with the code open

1. Read [03 — Orbital elements](03-orbital-elements.md), then inspect one dict from `parse_gp_elements`.  
2. Read [04 — Propagation](04-propagation-and-earth.md) while skimming the numbered comments inside `propagate()`.  
3. Run the script, open `orbit_report.txt` + `ground_tracks.png`, and match each sat to [05 — Orbit families](05-orbit-families.md).

Back to the [index](00-index.md).
