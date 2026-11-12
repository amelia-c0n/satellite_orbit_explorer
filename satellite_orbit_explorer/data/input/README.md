# Input data (unpacked workshop files)

These files come from `input_data/orbit_workshop_inputs.zip` at the repo root  
(native CelesTrak GP JSON, retrieved 2026-11-10). See the project root `README.md` for the full overview.

| File | What it is |
|------|------------|
| `orbital_elements.json` | Orbit snapshots for PULSAR-0, Galileo 29, SES-5, and QZS-2 |
| `data_manifest.json` | Where the data came from, epochs, and known limitations |
| `world_map.txt` | Simple world coastline points for map plots later |

Do not invent satellites or orbital numbers. If a required file is missing, fix the zip / unpack step instead of making up data.

**Note:** QZS-2 has an older epoch (2026-10-17) than the others — useful as a stale-data teaching example.
