# Stage 8 — KML export + report (Cursor / Python script)

**Rules:** Build only this stage, then stop. Reuse the names defined in earlier stages. Never invent satellites or data: if an input or an earlier stage is missing, stop with a clear error. Keep the code short, with comments, and explain it simply. Report success only from real output.

**Context:** Stages 1–7 already provide `elements`, `tracks`, `summaries`, `source_note`, `start` / `end` / `STEP_SECONDS` / `DURATION_HOURS`, `COLORS`, `OUT_DIR`, `elements_table`, `summary_table`, `to_hex`, `ET` (`xml.etree.ElementTree`), and the two PNG paths. Extend `orbit_explorer.py`. If any of those are missing, stop with a clear error.

---

## Stage 8 deliverables

Build **KML 2.2** with `xml.etree.ElementTree`:
- Default namespace: `http://www.opengis.net/kml/2.2`
- Register `gx` namespace: `http://www.google.com/kml/ext/2.2`

### Shared styling
For each satellite, a `Style` whose icon and line colour match its figure colour:
- Convert Matplotlib colour → hex with `to_hex`
- Reorder to KML **aabbggrr** (example: `tab:blue` `#1f77b4` → `ffb4771f`)
- Icon href: `http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png` (white icon so the colour shows)

Helper suggestion: `matplotlib_color_to_kml_abgr(color) -> str`.

### 1. `orbit_tracks_ecef.kml`
- Document name / title: `Multi-Satellite Orbits | Earth-fixed`
- One `Placemark` with a `LineString` per satellite
- `altitudeMode` = `absolute`
- Coordinates: `lon,lat,alt` with altitude in **metres** (`alt_km * 1000`)

### 2. `orbit_animation.kml`
- Document name / title: `Multi-Satellite Ground Tracks | Animation`
- Per satellite: one `Placemark` with a `gx:MultiTrack`
- Keep **one point per 60 s** (subsample the 5 s grid)
- Start a **new** `gx:Track` wherever longitude jumps by more than **180°** (date-line break)
- In each `gx:Track`:
  - `altitudeMode` = `clampToGround`
  - all `<when>` UTC timestamps as `YYYY-MM-DDTHH:MM:SSZ`
  - matching `<gx:coord>` values as `lon lat 0` (space-separated)

### 3. `orbit_report.txt`
Plain text including:
- Title: `Satellite Orbit Report - built during Space Career Week 2026, GNSS Academy`
- `source_note`
- The time window and step
- A one-line model caveat (Kepler / SGP4 mean elements / educational approximation)
- `summary_table(summaries)` lines
- `elements_table(elements)` lines

### 4. Zip the five outputs
Create `OUT_DIR / "satellite_orbit_outputs.zip"` containing:
1. `ground_tracks.png`
2. `velocity_timeseries.png`
3. `orbit_tracks_ecef.kml`
4. `orbit_animation.kml`
5. `orbit_report.txt`

**Local adaptation (not Colab):** do **not** use `google.colab.files.download`. Just write the zip under `OUT_DIR` and print its path/size. The user can open/share that file from the project folder.

### 5. How to open / “Run all” (not notebook Markdown cells)
Update the root `README.md` with:
- A short **Run all** checklist (`venv` → `python orbit_explorer.py` → find outputs in `data/output/`)
- How to open the KML files in **Google Earth Pro** and play the animation (`orbit_animation.kml`)

### 6. Wire `__main__`
After Stage 7 saves the PNGs, write the two KMLs, the report, and the zip. Print the output paths. Keep earlier stage prints.

### 7. Success check
Run:

```bash
cd satellite_orbit_explorer
source .venv/bin/activate
python orbit_explorer.py
```

Confirm **real** files exist under `data/output/`:
- `orbit_tracks_ecef.kml`
- `orbit_animation.kml`
- `orbit_report.txt`
- `satellite_orbit_outputs.zip` (contains the five artifacts)

Print paths and zip member names from real output. Stop after Stage 8.

---

## Teaching note (for the tutor)

After implementing, explain in a few short lines what the ECEF LineString KML vs the animated ground-track KML are for — beginner-friendly.
