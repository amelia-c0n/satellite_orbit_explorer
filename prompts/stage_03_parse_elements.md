# Stage 3 — Parse Kepler elements (Cursor / Python script)

**Rules:** Build only this stage, then stop. Reuse the names defined in earlier stages. Never invent satellites or data: if an input or an earlier stage is missing, stop with a clear error. Keep the code short, with comments, and explain it simply. Report success only from real output.

**Context:** Stages 1–2 already provide `extract_inputs`, `read_gp_json`, `MU_EARTH_KM3_S2`, `IN_DIR`, and the `__main__` load of `sats` / `data_manifest` / `source_note`. Extend `orbit_explorer.py` — do not start a new project.

**Model reminder:** GP records hold **SGP4 mean elements**. Converting them with two-body Kepler formulas is an **educational approximation**, not precision orbit prediction.

---

## Stage 3 deliverables

Add to `satellite_orbit_explorer/orbit_explorer.py`:

### 1. `parse_gp_epoch(text)`
- Parse with `datetime.fromisoformat(text.rstrip("Z"))`
- Attach `tzinfo=timezone.utc` (CelesTrak epochs are UTC without an offset in the string)

### 2. `parse_gp_elements(rec)`
Return a dict with:
- `name` from `OBJECT_NAME`
- `norad_id` as `int` from `NORAD_CAT_ID`
- `label` = `f"{name} [{norad_id}]"`
- `epoch` from `parse_gp_epoch(rec["EPOCH"])`
- `n_rad_s` = `2 * math.pi * MEAN_MOTION / 86400` (rev/day → rad/s)
- `a_km` = `(MU_EARTH_KM3_S2 / n_rad_s**2) ** (1/3)` (Kepler’s third law)
- `e` = `ECCENTRICITY` (already a decimal fraction)
- `i_rad`, `raan_rad`, `argp_rad`, `M0_rad` — convert from degrees with `math.radians(...)`

If a required GP field is missing, let earlier validation catch it, or raise a clear `ValueError` — do not invent values.

### 3. Build and print a table
- `elements = [parse_gp_elements(s) for s in sats]`
- `elements_table(elements)` returns the **lines** of a text table showing: name, NORAD, epoch, `a` [km], `e`, and the four angles **in degrees** (convert back from radians for display)
- Print the table (join lines or print each line)
- Keep `elements_table` reusable for Stage 8

### 4. Field → symbol mapping (not a Markdown notebook cell)
Add a short comment block near `parse_gp_elements` **and** a small section in the root `README.md` with a table mapping each GP field to its symbol and unit conversion, plus a one-line note that GP values are SGP4 mean elements so our two-body use is approximate.

Suggested mapping content:

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

### 5. Wire `__main__`
After loading `sats` (Stage 2), build `elements` and print `elements_table(elements)`. Keep Stage 2 prints (`source_note` + name/NORAD/EPOCH) unless they become redundant; prefer keeping them short and then showing the table.

### 6. Success check
Run:

```bash
cd satellite_orbit_explorer
source .venv/bin/activate
python orbit_explorer.py
```

Show the **real** printed elements table. Stop after Stage 3.

---

## Teaching note (for the tutor)

After implementing, explain in a few short lines what `a`, `e`, and the angles mean — beginner-friendly, no jargon pile-on.
