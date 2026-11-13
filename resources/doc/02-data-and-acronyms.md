# 02 — Data & acronyms

## Who provides the data?

**CelesTrak** — a public site that redistributes US catalog orbit data in convenient formats.  
Our workshop files were downloaded from CelesTrak GP queries (see `data_manifest.json`).

Search: `CelesTrak GP JSON`, or read  
[CelesTrak GP data formats](https://celestrak.org/NORAD/documentation/gp-data-formats.php).

## Acronyms you’ll see in this project

### NORAD / catalog ID
**NORAD** historically labeled the US Space Surveillance catalog.  
Today you’ll also hear **SATCAT** (satellite catalog).  
**NORAD_CAT_ID** is simply the object’s **ID number** (e.g. SES-5 = `38652`).

### GP — General Perturbations
A **GP** record is a compact set of **mean orbital elements** fitted so a standard model can predict the object for a while.  
Think: “official orbit postcard,” not a full physics simulation dump.

### TLE — Two-Line Element set
The classic **text** GP format: two (or three) fixed-width lines.  
Hard for beginners: fields are packed by character column, 2-digit years, and old **5-digit** ID limits.

Example idea (not to memorize): line 1 has drag/catalog metadata; line 2 has inclination, eccentricity, mean motion, …

### OMM — Orbit Mean-Elements Message
A **modern** standard (CCSDS) for the same kind of mean elements, with **named fields**.  
CelesTrak’s **JSON** uses OMM-style names (`INCLINATION`, `MEAN_MOTION`, …).  
That’s what we load in `orbital_elements.json`.

**Why we prefer OMM JSON over TLE in this project**
- Clear field names  
- ISO-like dates  
- Room for **6-digit** catalog numbers  

Code: `read_gp_json()`.

### SGP4 — Simplified General Perturbations 4
The **usual propagator** meant to be used with GP/TLE mean elements.  
It includes many “average Earth isn’t perfect” effects in a standardized way.

**Important for this course project:**  
We do **not** implement full SGP4. We use a **two-body Kepler** classroom model + simple Earth rotation (**GMST**).  
So: *same input postcard, simpler travel rules.*

Search: `SGP4 explained`, `TLE mean elements`.

### Epoch
The **time stamp** of the element set. Propagation starts from this moment.  
If the epoch is old (workshop **QZS-2** ≈ 17 Oct 2026), the common 24 h window is farther from the photo → larger “stale data” teaching error.

Code: `parse_gp_epoch()`, Stage 4 offsets in `print_epoch_offsets()`.

### UTC
**Coordinated Universal Time** — one global clock. We use timezone-aware UTC datetimes so “midnight” isn’t ambiguous.

### GNSS
**Global Navigation Satellite System** — constellations that provide positioning (GPS, Galileo, GLONASS, BeiDou, QZSS, …).  
**Galileo 29** is a GNSS-style MEO example in our pack.

### Other short ones
| Term | Meaning here |
|------|----------------|
| **μ (MU)** | Earth’s gravitational parameter — “strength of gravity” in our formulas (`MU_EARTH_KM3_S2`) |
| **Mean elements** | Averaged orbit parameters (not the same as “mean anomaly” alone) |
| **ECEF** | Axes fixed to the rotating Earth (used after GMST rotation) |
| **TEME** | A common inertial frame associated with SGP4 products (we keep the idea simple) |

## Workshop files (what each is for)

| File | Role |
|------|------|
| `orbital_elements.json` | The four GP JSON records we propagate |
| `data_manifest.json` | Provenance: URLs, epochs, caveats (not used for math) |
| `world_map.txt` | Coastline points for map plots (`latitude longitude` per line) |

Code: `extract_inputs()`.

## Live data (optional)

If `LIVE_GROUP = "STATIONS"` (or another CelesTrak group name):

- Download GP JSON for that **group**
- Cache as `gp_<GROUP>.json` for up to **2 hours** (don’t poll)
- Take the **first four** objects sorted by catalog ID

Code: `apply_live_group_if_requested()`.  
Same theory; different satellites → different tracks.

## SGP4 vs our Kepler model (the foggy bit)

| | Official GP use | This project |
|--|-----------------|--------------|
| Input | GP / TLE / OMM mean elements | Same kind of numbers |
| Motion model | **SGP4** (designed for those means) | **Kepler two-body** + spherical Earth + **GMST** |
| Goal | Operational-ish prediction | Learning & clear comparisons |
| Expect | Better short-term realism | Approximate paths; good orbit-*type* intuition |

So when SES-5 sits near 5°E, that’s a **sanity check** that our rotation/signs are reasonable — not a claim of centimetre accuracy.

Next: [03 — Orbital elements](03-orbital-elements.md)
