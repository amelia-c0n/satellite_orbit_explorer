# Stage 4 — Common UTC time window (Cursor / Python script)

**Rules:** Build only this stage, then stop. Reuse the names defined in earlier stages. Never invent satellites or data: if an input or an earlier stage is missing, stop with a clear error. Keep the code short, with comments, and explain it simply. Report success only from real output.

**Context:** Stages 1–3 already provide `elements` (from `parse_gp_elements`), `STEP_SECONDS`, `DURATION_HOURS`, and `timezone.utc`. Extend `orbit_explorer.py` — do not start a new project. If `elements` is missing, stop with a clear error.

**Model reminder:** Each GP record is propagated from **its own epoch**. A shared plot/report window is convenient, but larger `start - epoch` offsets mean larger approximation error (especially for stale records like QZS-2).

---

## Stage 4 deliverables

Add to `satellite_orbit_explorer/orbit_explorer.py`:

### 1. Build one common UTC time grid
Using the existing `elements` list and config:

- `start` = the **newest** epoch among `elements`, floored to **UTC midnight**  
  (date of that newest epoch at `00:00:00` with `tzinfo=timezone.utc`)
- `end` = `start + timedelta(hours=DURATION_HOURS)`
- `n_points` = `(end - start) // timedelta(seconds=STEP_SECONDS) + 1`  
  (integer number of steps; the grid **includes both ends**)
- `times` = list of UTC datetimes:  
  `start`, `start + STEP_SECONDS`, …, `end`

Do not invent epochs. If `elements` is empty, raise a clear error.

### 2. Print diagnostics
- Print the window: `start`, `end`, `DURATION_HOURS`, `STEP_SECONDS`, and `n_points`
- For each satellite in `elements`, print:
  - `label` (or name + NORAD)
  - epoch
  - offset `start - epoch` in **days** (float is fine)
  - if offset **> 7 days**, flag it clearly as a **stale record**

### 3. Why this matters (not a Markdown notebook cell)
Add a short comment near the time-grid code **and** a brief note in the root `README.md` explaining once:

- each record is propagated from its own epoch, so error grows with the time offset from that epoch
- the workshop’s **QZS-2** record dates from **17 October 2026** (stale relative to the common window)

### 4. Wire `__main__`
After building `elements` (Stage 3), compute `start`, `end`, `n_points`, `times`, and print the diagnostics above. Keep earlier stage prints.

Suggested helper names (keep short; reuse later): e.g. `build_time_grid(elements)` returning `(start, end, times)` or similar — optional but preferred over a long inline block.

### 5. Success check
Run:

```bash
cd satellite_orbit_explorer
source .venv/bin/activate
python orbit_explorer.py
```

Show the **real** printed window, `n_points`, and per-satellite offsets (with the QZS-2 stale flag). Stop after Stage 4.

---

## Teaching note (for the tutor)

After implementing, explain in a few short lines what the common window is and why QZS-2 is flagged — beginner-friendly.
