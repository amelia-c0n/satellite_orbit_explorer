# Optional extension — Live CelesTrak data (Cursor / Python script)

**Rules:** Build only this stage, then stop. Reuse the names defined in earlier stages. Never invent satellites or data: if an input or an earlier stage is missing, stop with a clear error. Keep the code short, with comments, and explain it simply. Report success only from real output.

**Context:** Stages 1–2 already provide `LIVE_GROUP`, `IN_DIR`, `requests`, `read_gp_json`, and the `__main__` load of workshop `sats` / `source_note`. Extend `orbit_explorer.py`. This is an **optional** path after Stage 2 logic — do not invent satellite records.

**CelesTrak courtesy:** cache downloads; do **not** poll repeatedly. Refresh only if the cache file is missing or older than **2 hours**.

---

## Deliverables

### 1. Helper: `load_live_group_or_workshop(...)`
Add a small function (name can vary slightly; keep it clear) used right after the Stage 2 workshop load:

**If `LIVE_GROUP is None`:**
- Print that the **workshop snapshot** is used
- Leave `sats` / `source_note` unchanged
- Return without downloading

**If `LIVE_GROUP` is set** (e.g. `"STATIONS"`):
- Cache path: `IN_DIR / f"gp_{LIVE_GROUP}.json"`
- Download only if cache is **missing** or **older than 2 hours**:
  - URL: `https://celestrak.org/NORAD/elements/gp.php?GROUP={LIVE_GROUP}&FORMAT=JSON`
  - `requests.get(..., timeout=30)`
  - `raise_for_status()`
  - Parse/check with `response.json()` (must be a list of GP records)
  - Write the JSON to the cache path
- If cache is fresh, load from cache (no network)
- Validate with `read_gp_json(cache_path)` (or equivalent field checks)
- Replace `sats` with the **first four** records after sorting by `NORAD_CAT_ID`
- Update `source_note` to include the group name and retrieval/cache time
- Print the selected satellites (name, NORAD, EPOCH)

If download fails or the group returns fewer than 4 usable records, stop with a **clear error** — do not invent satellites. Fall back is only when `LIVE_GROUP is None` (workshop files).

### 2. Wire into `__main__`
Place the live-group step **immediately after** Stage 2 loads workshop `sats` and builds the initial `source_note` (before Stage 3 `parse_gp_elements`).

Keep `LIVE_GROUP = None` as the default in Stage 1 config so normal workshop runs stay offline.

### 3. Docs
Briefly note in the root `README.md`:
- Optional live mode via `LIVE_GROUP` (example: `"STATIONS"`)
- 2-hour cache under `data/input/gp_<GROUP>.json`
- Respect CelesTrak: don’t poll

### 4. Success check (two runs)

**A. Default (workshop):**
```bash
# LIVE_GROUP is None
python orbit_explorer.py
```
Must print that the workshop snapshot is used; rest of pipeline unchanged.

**B. Live (only when you ask / after you set it):**
Set `LIVE_GROUP = "STATIONS"` in the Stage 1 config, then run again.  
Show real output: cache download or cache hit, `source_note`, and the four selected stations.

For this implementation stage, implement the code with default `LIVE_GROUP = None`, demonstrate run A, and **do not** leave `LIVE_GROUP` set to `"STATIONS"` unless the user asks. Stop after this optional stage.

---

## Teaching note (for the tutor)

Explain briefly what a CelesTrak `GROUP` is and why caching matters — beginner-friendly.
