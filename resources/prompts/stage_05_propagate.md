# Stage 5 — Propagate orbits (Cursor / Python script)

**Rules:** Build only this stage, then stop. Reuse the names defined in earlier stages. Never invent satellites or data: if an input or an earlier stage is missing, stop with a clear error. Keep the code short, with comments, and explain it simply. Report success only from real output.

**Context:** Stages 1–4 already provide `elements`, `times`, `MU_EARTH_KM3_S2`, `EARTH_RADIUS_KM`, and the Kepler element dict keys (`a_km`, `e`, `i_rad`, `raan_rad`, `argp_rad`, `M0_rad`, `n_rad_s`, `epoch`, …). Extend `orbit_explorer.py`. If `elements` or `times` is missing/empty, stop with a clear error.

**Model reminder:** Two-body Kepler + spherical Earth + simple Greenwich rotation. Educational approximation of SGP4 mean elements — not precision orbit prediction.

---

## Stage 5 deliverables

Add to `satellite_orbit_explorer/orbit_explorer.py`. This is the physics stage — keep **seven numbered comments** inside `propagate` explaining each step.

### 1. `solve_kepler(M, e)`
Newton–Raphson on Kepler’s equation `M = E - e*sin(E)`:
- Initial guess: `E = M`, or `E = math.pi` if `e > 0.8`
- Iterate up to 50 times; raise a clear error if it does not converge
- Convergence: residual `|E - e*sin(E) - M|` small enough for float work (e.g. `< 1e-12` internally is fine)

### 2. `gmst_rad(t)`
Greenwich Mean Sidereal Time, IAU-1982 (Meeus eq. 12.4):
- `d` = days since J2000 (`2000-01-01 12:00:00` UTC)
- `T = d / 36525`
- `theta_deg = 280.46061837 + 360.98564736629*d + 0.000387933*T**2 - T**3/38710000`
- Reduce modulo 360°, return radians

`t` must be timezone-aware UTC (or treat as UTC consistently with Stage 4).

### 3. `propagate(el, times)`
Return a **list of dicts**, one per time, each with:
`time`, `lat_deg`, `lon_deg`, `alt_km`, `speed_km_s`

Implement with these **seven numbered comment steps**:

1. `M = M0 + n*(t - epoch)`, modulo `2*pi`
2. `E = solve_kepler(M, e)`
3. `r = a*(1 - e*cos(E))`,  
   `nu = atan2(sqrt(1-e**2)*sin(E), cos(E) - e)`,  
   `u = argp + nu`
4. Inertial position:  
   `x = r*(cos(RAAN)*cos(u) - sin(RAAN)*sin(u)*cos(i))`  
   `y = r*(sin(RAAN)*cos(u) + cos(RAAN)*sin(u)*cos(i))`  
   `z = r*sin(u)*sin(i)`
5. Rotate by `theta = gmst_rad(t)` into Earth-fixed axes:  
   `x' = cos(theta)*x + sin(theta)*y`  
   `y' = -sin(theta)*x + cos(theta)*y`  
   (`z` unchanged)
6. Spherical:  
   `lat = atan2(z, hypot(x', y'))`,  
   `lon = atan2(y', x')` in **degrees**,  
   `alt = r - EARTH_RADIUS_KM`
7. Vis-viva speed: `sqrt(mu * (2/r - 1/a))`

Use the element dict fields already defined (`a_km`, etc.). Do not invent orbital numbers.

### 4. Build tracks and print samples
- `tracks = [propagate(el, times) for el in elements]`
- For each satellite, print the **first**, **middle**, and **last** point (time, lat, lon, alt, speed), labeled with `el["label"]`

Prefer pairing safely, e.g. `for el, track in zip(elements, tracks): ...`. If lengths disagree, raise a clear error.

### 5. Assert checks (run once in `__main__` or a small `run_propagation_checks()` helper)
Use `assert` (or raise `AssertionError` with a clear message):

1. **GMST at J2000** is about **280.46°**  
   (`math.degrees(gmst_rad(J2000))` near 280.46)
2. **Kepler residual** below `1e-10` for a few sample `(M, e)` pairs after `solve_kepler`
3. If **SES-5 (NORAD 38652)** is in `elements`, its longitude over the track stays between **4° and 6° East**  
   (handle lon wrapping sensibly if needed; typical GEO lon should stay in that band)

If check (3) fails, look for a **GMST or sign error** in the ECEF rotation. **Never** add an ad-hoc longitude offset to force the test to pass.

### 6. Wire `__main__`
After Stage 4’s `start` / `end` / `times`, run checks, build `tracks`, print the sample points. Keep earlier stage output.

### 7. Success check
Run:

```bash
cd satellite_orbit_explorer
source .venv/bin/activate
python orbit_explorer.py
```

Show **real** output: asserts passing (no traceback) and first/middle/last points per satellite. Stop after Stage 5.

---

## Optional README note
One short bullet under the model / time-window docs: Stage 5 propagates with Kepler + GMST; SES-5 ~5°E is a sanity check, not a forced offset.

---

## Teaching note (for the tutor)

After implementing, explain in a few short lines the path from mean anomaly → position on Earth → speed — beginner-friendly.
