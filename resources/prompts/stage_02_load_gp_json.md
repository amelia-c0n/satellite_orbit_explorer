# Stage 2 — Load GP JSON (Cursor / Python script)

**Rules:** Build only this stage, then stop. Reuse the names defined in earlier stages. Never invent satellites or data: if an input or an earlier stage is missing, stop with a clear error. Keep the code short, with comments, and explain it simply. Report success only from real output.

**Context:** Stage 1 already created `PROJECT_DIR`, `IN_DIR`, `OUT_DIR`, `INPUT_ZIP`, `REQUIRED_INPUT_FILES`, `extract_inputs()`, and `orbit_explorer.py`. Extend that script — do not start a new project.

**Model reminder:** GP records hold SGP4 mean elements; our later math is an educational Kepler approximation.

---

## Stage 2 deliverables

Add to `satellite_orbit_explorer/orbit_explorer.py` (reuse Stage 1 names):

### 1. Reuse `extract_inputs()` from Stage 1
Call the existing helper at the start of `__main__`. Do not reintroduce a second unpack function. If Stage 1’s version is incomplete, finish it to match Stage 1’s final design (skip if present → extract only the three required files → verify all three exist). No Colab upload poll; no `files.upload()`.

### 2. `read_gp_json(path)`
- Load the JSON list from `path`.
- Check that **every** record has:  
  `OBJECT_NAME`, `NORAD_CAT_ID`, `EPOCH`, `MEAN_MOTION`, `ECCENTRICITY`, `INCLINATION`, `RA_OF_ASC_NODE`, `ARG_OF_PERICENTER`, `MEAN_ANOMALY`.
- Raise `ValueError` if anything is missing or the top level is not a list.

### 3. Run them in `if __name__ == "__main__":`
After setup / `extract_inputs()`:

- `sats = read_gp_json(IN_DIR / "orbital_elements.json")`
- Load `data_manifest` from `IN_DIR / "data_manifest.json"`
- Build `source_note`: a one-line description that includes `data_manifest["retrieved_utc"]`
- Print `source_note`
- Print each satellite’s **name**, **NORAD ID**, and **EPOCH**

### 4. Short explanation (not a Markdown cell)
In the script docstring or a short comment block near `read_gp_json`, explain in **two sentences** why OMM JSON is easier than the old TLE format: named fields, ISO dates, and support for six-digit catalog numbers.

Optionally mirror those two sentences in the root `README.md` under Input data (keep it brief).

### 5. Success check
Run:

```bash
cd satellite_orbit_explorer
source .venv/bin/activate
python orbit_explorer.py
```

Show the **real** terminal output (`source_note` + one line per satellite). Stop after Stage 2.

---

## Teaching note (for the tutor)

After implementing, explain in a few short lines what GP/OMM JSON is and what we just loaded — beginner-friendly.
