# Stage 1 — Setup (Cursor / Python script)

**Rules:** Build only this stage, then stop. Reuse names from earlier stages when we have them. Never invent satellites or data: if an input or an earlier stage is missing, stop with a clear error. Keep the code short, with comments, and explain it simply. Report success only from real output.

**You are my Python tutor.** We’re building **Satellite Orbit Explorer** in Cursor as a reusable Python project in 8 stages:
1) setup · 2) load GP JSON · 3) parse elements · 4) time window · 5) propagate · 6) orbit summary · 7) plots · 8) KML and report.

**Model:** two-body Kepler orbit, spherical Earth, simple Greenwich rotation. GP records hold SGP4 mean elements, so this is an **educational approximation**, not precision orbit prediction.

**Project layout for this stage:**
```text
scw26-challenge3/                  # repo root
  README.md
  input_data/
    orbit_workshop_inputs.zip
  satellite_orbit_explorer/
    orbit_explorer.py
    requirements.txt
    data/
      input/
      output/
```
Keep helpers in `orbit_explorer.py` for now (no separate modules yet).

---

## Stage 1 deliverables

1. **Create a root `README.md`**
   - Project title: Satellite Orbit Explorer | Amelia
   - Short description of the educational goal
   - List the 8 stages
   - How to create the venv, install deps, and run the script
   - Brief note on input data (zip → `data/input/`)

2. **Create the project folder + venv-friendly deps**
   - Add `satellite_orbit_explorer/requirements.txt` with at least: `matplotlib`, `requests`
   - Create a virtual environment and install deps (show the commands you use)

3. **Create `satellite_orbit_explorer/orbit_explorer.py`** with:
   - A top docstring titled:
     `Satellite Orbit Explorer · built during Space Career Week 2026 · GNSS Academy`
     listing the 8 stages
   - Imports:
     `json`, `math`, `time`, `zipfile`, `xml.etree.ElementTree as ET`,
     `datetime` / `timedelta` / `timezone`, `pathlib.Path`,
     `matplotlib.pyplot as plt`, `matplotlib.colors.to_hex`, `requests`
   - Constants:
     `MU_EARTH_KM3_S2 = 398600.4418`
     `EARTH_RADIUS_KM = 6378.137`
   - Paths (local, not Colab):
     `PROJECT_DIR` = directory containing this script
     `IN_DIR` = `PROJECT_DIR / "data" / "input"`
     `OUT_DIR` = `PROJECT_DIR / "data" / "output"`
     `REPO_ROOT` = `PROJECT_DIR.parent`
     `INPUT_ZIP` = `REPO_ROOT / "input_data" / "orbit_workshop_inputs.zip"`
     Create `IN_DIR` and `OUT_DIR`
   - Config: `STEP_SECONDS = 5`, `DURATION_HOURS = 24`, `LIVE_GROUP = None`
   - Required input names constant, e.g. `REQUIRED_INPUT_FILES` =
     `orbital_elements.json`, `data_manifest.json`, `world_map.txt`
   - **`extract_inputs()`** (final unpack design — reuse in later stages):
     - If all three required files are already in `IN_DIR`, do nothing (short “already present” note)
     - Else if `INPUT_ZIP` exists and `zipfile.is_zipfile` passes, extract **only those three files** into `IN_DIR`
     - Else stop with a clear error (place the zip under `input_data/`) — do not invent files
     - Always finish by verifying all three paths `is_file()`; if any are missing, raise a clear error listing them
   - Short comments explaining: what `MU` and Earth radius are for; why we use UTC; units are km and km/s
   - An `if __name__ == "__main__":` block that calls `extract_inputs()` and prints the configuration (paths, constants, step, duration)

4. **Conventions:** UTC-aware datetimes, km, km/s.

5. **Success check:** run
   `python orbit_explorer.py`
   and show the real terminal output. Stop after Stage 1.

**Note:** Stage 2 adds `read_gp_json` and prints satellite records. Do not load/parse GP JSON in Stage 1 beyond ensuring the files are present via `extract_inputs()`.

---

## Teaching note (for the tutor)

After implementing, explain in 3–5 short lines what this stage set up and what the printed values mean — beginner-friendly.
