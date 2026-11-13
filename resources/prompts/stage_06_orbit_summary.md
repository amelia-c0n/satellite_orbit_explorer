# Stage 6 — Orbit summary (Cursor / Python script)

**Rules:** Build only this stage, then stop. Reuse the names defined in earlier stages. Never invent satellites or data: if an input or an earlier stage is missing, stop with a clear error. Keep the code short, with comments, and explain it simply. Report success only from real output.

**Context:** Stages 1–5 already provide `elements`, `tracks`, `EARTH_RADIUS_KM`, and element fields (`a_km`, `e`, `i_rad`, `n_rad_s`, `name`, `norad_id`, …). Extend `satellite_orbit_explorer/orbit_explorer.py`. If `elements` or `tracks` is missing/empty, or their lengths differ, stop with a clear error.

**Model reminder:** Summaries use two-body Kepler quantities derived from GP mean elements — educational approximation.

---

## Stage 6 deliverables

Add to `orbit_explorer.py`:

### 1. `orbit_summary(el, pts)`
Return a dict with:
- `name`, `norad_id` from `el`
- `period_h` = `2 * math.pi / n_rad_s / 3600` (hours)
- `perigee_km` = `a_km * (1 - e) - EARTH_RADIUS_KM`
- `apogee_km` = `a_km * (1 + e) - EARTH_RADIUS_KM`
- `e` from `el`
- `i_deg` = degrees from `i_rad`
- `speed_min_km_s`, `speed_max_km_s` = min/max of `speed_km_s` over `pts`

If `pts` is empty, raise a clear error — do not invent speeds.

### 2. Build summaries and table
- `summaries = [orbit_summary(el, pts) for el, pts in zip(elements, tracks)]`
- `summary_table(summaries)` returns the **lines** of a text table with all those values
- Print the table
- Keep `summary_table` reusable for Stage 8

### 3. Assert (if present)
If Galileo 29 (**NORAD 59598**) is in `summaries` / `elements`, assert its `period_h` is between **14.0 and 14.2** hours.

### 4. Interpret the values (not a Markdown notebook cell)
Add a short comment near the summary code **and** a brief section in the root `README.md` interpreting:

- **PULSAR-0:** period ~**1.58 h**, inclination ~**97.5°** (retrograde, near-polar, sun-synchronous-class)
- **Galileo 29:** period ~**14.08 h**
- **SES-5** and **QZS-2:** period ~**23.93 h** (about one sidereal day)
- **QZS-2:** eccentricity ~**0.07**, inclination ~**39°** → inclined geosynchronous orbit (**IGSO**), not geostationary

Do not invent satellites; only interpret ones present in the loaded data.

### 5. Wire `__main__`
After Stage 5 builds `tracks`, compute `summaries`, print `summary_table(summaries)`, run the Galileo assert if applicable. Keep earlier stage output.

### 6. Success check
Run:

```bash
cd satellite_orbit_explorer
source .venv/bin/activate
python orbit_explorer.py
```

Show the **real** printed summary table (and assert passing). Stop after Stage 6.

---

## Teaching note (for the tutor)

After implementing, explain in a few short lines what period, perigee/apogee, and “GEO vs IGSO” mean using the printed numbers — beginner-friendly.
