# 05 — Orbit families (LEO, MEO, GEO, IGSO)

These names are **families**, not single magic altitudes. Use period, height, inclination, and eccentricity together.

Numbers below match our workshop summary (educational Kepler values).

---

## LEO — Low Earth Orbit

**Idea:** A few hundred km up; period roughly **90–100 minutes**.

**Workshop example: PULSAR-0**
- Period ≈ **1.58 h**
- Altitude ≈ **500 km**
- i ≈ **97.5°** (near-polar / sun-synchronous-class)

**On the map:** many ground-track stripes in 24 h, shifting west.

**If you used ISS instead:** still LEO period ~1.5 h, but i ≈ **51.6°** → tracks don’t go near the poles the same way.

Search: `low Earth orbit`, `sun synchronous orbit`.

---

## MEO — Medium Earth Orbit

**Idea:** Thousands to tens of thousands of km; periods of several hours.  
Many **GNSS** satellites live here.

**Workshop example: Galileo 29**
- Period ≈ **14.08 h**
- Altitude ≈ **23 200 km**
- i ≈ **55°**

**On the map:** a wide wave, fewer revolutions per day than LEO.

**If you used a GPS satellite:** similar MEO story (period ~12 h for GPS, different from Galileo’s design).

Search: `Galileo satellite orbit`, `MEO GNSS`.

---

## Geosynchronous vs geostationary (easy to mix up)

### Geosynchronous
Period ≈ **one sidereal day** (~23 h 56 min ≈ **23.93 h** in our table).  
The ground track **repeats** each day, but may still move north/south.

### Geostationary (GEO)
A special geosynchronous case:
- Period ≈ sidereal day  
- **i ≈ 0°** (equatorial)  
- **e ≈ 0** (circular)  

Then the satellite appears to **hover** over one longitude.

**Workshop example: SES-5**
- Period ≈ **23.93 h**
- i ≈ **0.05°**
- Nearly fixed near **5°E**  
→ treated as **GEO-like** in this project.

**On the map / Google Earth:** looks like a **dot** — easy to miss!

Search: `geostationary vs geosynchronous`.

---

## IGSO — Inclined Geosynchronous Orbit

**Idea:** Same ~24 h period class as GEO, but **tilted** (and often a bit eccentric).  
Ground track is typically a **figure-8** (analemma-like), not a point.

**Workshop example: QZS-2 (Michibiki-2)**
- Period ≈ **23.94 h**
- i ≈ **39°**
- e ≈ **0.075**
- Slow near northern **apogee** → asymmetric loops

**On the map:** figure-8 over Asia/Oceania region in our run.  
**Speed plot:** largest vmin→vmax change of the four.

Search: `QZSS IGSO`, `inclined geosynchronous orbit`.

---

## Side-by-side (workshop)

| Family | Example | Period | Inclination | Map sketch |
|--------|---------|--------|-------------|------------|
| LEO | PULSAR-0 | ~1.6 h | ~97.5° | Many shifting passes |
| MEO / GNSS | Galileo 29 | ~14.1 h | ~55° | Wide wave |
| GEO-like | SES-5 | ~23.93 h | ~0° | One spot |
| IGSO | QZS-2 | ~23.94 h | ~39° | Figure-8 |

---

## What changes if the satellite set changes?

Same code path (`parse_gp_elements` → `propagate` → plots). Only the **element numbers** change.

| Swap-in | Likely family | What you’d notice |
|---------|---------------|-------------------|
| ISS / station pieces | LEO | Dense LEO tracks, mid inclinations |
| More Galileo/GPS | MEO | Several wide GNSS waves |
| Another GEO comsat | GEO | Another fixed longitude |
| QZSS / BeiDou IGSO | IGSO | Other figure-8 longitudes |
| Weather sat in sun-sync LEO | LEO | Polar-ish stripes like PULSAR |

Optional live mode: `LIVE_GROUP = "STATIONS"` pulls a stations group and keeps the first four by catalog ID — great for seeing “same pipeline, new cast.”

Next: [06 — Outputs & code map](06-outputs-and-code-map.md)
