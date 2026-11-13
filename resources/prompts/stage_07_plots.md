# Stage 7 — Plots (Cursor / Python script)

**Rules:** Build only this stage, then stop. Reuse the names defined in earlier stages. Never invent satellites or data: if an input or an earlier stage is missing, stop with a clear error. Keep the code short, with comments, and explain it simply. Report success only from real output.

**Context:** Stages 1–6 already provide `IN_DIR`, `OUT_DIR`, `elements`, `tracks`, `times` / point `time` fields, `matplotlib.pyplot as plt`, and `to_hex` (imported earlier; use if handy). Extend `orbit_explorer.py`. Use **Matplotlib only** (no Cartopy). If `world_map.txt`, `elements`, or `tracks` is missing, stop with a clear error.

---

## Stage 7 deliverables

### 1. `load_coastline(path)`
- `world_map.txt` lines are `latitude longitude` (**latitude first**)
- Blank lines separate coastline **segments**
- Return a `list` of segments; each segment is a list of `(lon, lat)` points
- **Never** join segments across blank lines (that would draw false lines across oceans)

### 2. Colors
- `COLORS = ["tab:blue", "tab:orange", "tab:green", "tab:red"]` — one per satellite in order
- Stage 8 reuses `COLORS` (keep the name)

### 3. Figure 1 — ground tracks
- Gray coastline from `load_coastline(IN_DIR / "world_map.txt")`
- For each track: **scatter** lon/lat with small dots (scatter avoids false lines across ±180°)
- Legend using each element’s `label`
- x: −180…180, y: −90…90
- Save `OUT_DIR / "ground_tracks.png"` at **200 dpi**, then `plt.show()`

### 4. Figure 2 — speed vs time
- One **stacked subplot per satellite**
- y: speed [km/s], x: UTC time
- Same `COLORS` order as the satellites
- Shared x-axis; disable y-axis offset notation (e.g. `ticklabel_format(useOffset=False)` or equivalent)
- Save `OUT_DIR / "velocity_timeseries.png"` at 200 dpi (same dpi as fig 1 is fine), then `plt.show()`

Prefer small helpers, e.g. `plot_ground_tracks(...)` and `plot_speed_timeseries(...)`, called from `__main__`.

### 5. What the plots mean (not a Markdown notebook cell)
Add a short comment near the plot code **and** a brief section in the root `README.md`:

**Ground tracks**
- **PULSAR-0:** many passes shifting west (fast LEO + Earth rotation)
- **Galileo:** a wide wave (MEO)
- **SES-5:** essentially one spot — period ≈ Earth’s rotation (geostationary-like)
- **QZS-2:** asymmetric figure-8 — same ~sidereal-day period, but **i ≈ 39°** and slow **northern apogee** (IGSO)

**Speed**
- Eccentric orbits (especially QZS-2) go **faster near perigee** and slower near apogee (Kepler / vis-viva)

### 6. Wire `__main__`
After Stage 6 summaries, build the two figures and save/show them. Keep earlier prints.

### 7. Headless / Cursor note
`plt.show()` may open windows locally. That is fine. If a non-interactive run is needed later, we can gate it — do **not** skip saving the PNGs.

### 8. Success check
Run:

```bash
cd satellite_orbit_explorer
source .venv/bin/activate
python orbit_explorer.py
```

Confirm **real** files exist:
- `data/output/ground_tracks.png`
- `data/output/velocity_timeseries.png`

Print their paths (and sizes if easy). Stop after Stage 7.

---

## Teaching note (for the tutor)

After implementing, explain in a few short lines why scatter is used for ground tracks and why SES-5 looks like a dot — beginner-friendly.
