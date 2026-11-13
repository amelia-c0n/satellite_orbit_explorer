# Learning guide — Satellite Orbit Explorer

Beginner-friendly notes for the physics and the full project path.  
Read in order the first time; later jump to any section you need.

## Study path

| # | Guide | What you’ll understand |
|---|--------|-------------------------|
| 1 | [01 — Big picture](01-big-picture.md) | What the project does end-to-end |
| 2 | [02 — Data & acronyms](02-data-and-acronyms.md) | GP, TLE, OMM, NORAD, SGP4 vs our Kepler model |
| 3 | [03 — Orbital elements](03-orbital-elements.md) | a, e, i, Ω, ω, M — with our four workshop sats |
| 4 | [04 — Propagation & Earth](04-propagation-and-earth.md) | Kepler’s equation, GMST, lat/lon, ground tracks, speed |
| 5 | [05 — Orbit families](05-orbit-families.md) | LEO, MEO, GEO, IGSO — and what other sats would look like |
| 6 | [06 — Outputs & code map](06-outputs-and-code-map.md) | Plots, KML, report ↔ functions in `orbit_explorer.py` |

## Quick acronym cheat sheet

| Acronym | Plain meaning |
|---------|----------------|
| **GP** | General Perturbations — public “orbit snapshot” data |
| **TLE** | Two-Line Element — old compact text format for GP |
| **OMM** | Orbit Mean-Elements Message — modern named-field format (our JSON) |
| **NORAD / SATCAT ID** | Catalog number that identifies an object in space |
| **SGP4** | The usual high-quality propagator for GP/TLE data (we do **not** run full SGP4) |
| **Kepler / two-body** | Simple model: Earth as a point mass, one satellite, no drag/Moon/Sun |
| **GMST** | Greenwich Mean Sidereal Time — how far Earth has rotated |
| **LEO / MEO / GEO / IGSO** | Low / Medium / Geostationary / Inclined geosynchronous orbit families |
| **UTC** | Coordinated Universal Time — our clock (no time zones) |
| **ECEF** | Earth-Centered, Earth-Fixed — coordinates that rotate with Earth |
| **KML** | Keyhole Markup Language — Google Earth file format |
| **GNSS** | Global Navigation Satellite System (GPS, Galileo, …) |

## Workshop satellites (default run)

| Satellite | Rough role in this project |
|-----------|----------------------------|
| **PULSAR-0** | Fast low polar-ish LEO |
| **Galileo 29** | GNSS / MEO |
| **SES-5** | Near-equatorial GEO-like (almost a fixed point on the map) |
| **QZS-2** | Inclined geosynchronous (IGSO), more oval; older epoch |

Optional live mode (`LIVE_GROUP = "STATIONS"`) swaps in other objects (e.g. ISS). Same math; different shapes on the map.

## Suggested online searches / links

- NASA: [Orbits and Kepler’s Laws](https://science.nasa.gov/learn/basics-of-space-flight/chapter5-1/)
- CelesTrak: [GP data formats](https://celestrak.org/NORAD/documentation/gp-data-formats.php)
- Video example: [orbital elements animation](https://www.youtube.com/watch?v=QZrYaKwZwhI)
- Search ideas: `orbital elements explained`, `RAAN argument of perigee`, `GMST sidereal time`, `geostationary vs geosynchronous`, `SGP4 vs Kepler`

Also see the short starter note: [orbit-theory-learning.md](orbit-theory-learning.md) (points here).
