# 03 — Orbital elements

Orbital elements are the **minimum set of numbers** that describe an ellipse around Earth and where the satellite is on it at the epoch.

Watch a visual first if you can:  
[Orbital elements animation (example)](https://www.youtube.com/watch?v=QZrYaKwZwhI)  
Search: `orbital elements 3D RAAN argument of perigee`.

Code that builds our dict: `parse_gp_elements()` → fields like `a_km`, `e`, `i_rad`, `raan_rad`, `argp_rad`, `M0_rad`, `n_rad_s`, `epoch`.

---

## The size & shape

### a — semi-major axis (km)
Half the long axis of the ellipse. **Bigger a ⇒ higher, slower orbit.**

We don’t read `a` from the JSON directly. We get mean motion **n**, then use Kepler’s third law:

\[
a = \left(\frac{\mu}{n^2}\right)^{1/3}
\]

Workshop ballpark:
- PULSAR-0 ≈ **6881 km** (LEO)
- Galileo 29 ≈ **29 600 km** (MEO)
- SES-5 / QZS-2 ≈ **42 160–42 170 km** (geosynchronous-class size)

### e — eccentricity (unitless)
How oval the orbit is.
- **0** ≈ circle  
- Larger e ⇒ bigger gap between closest and farthest points  

Workshop:
- Galileo ≈ **0.00016** (most circular here)
- SES-5 / PULSAR-0 also nearly circular  
- QZS-2 ≈ **0.075** (clearly more oval)

**Perigee** = closest point; **apogee** = farthest.  
Altitudes in the summary use:

- perigee altitude ≈ `a(1−e) − R_Earth`  
- apogee altitude ≈ `a(1+e) − R_Earth`  

Code: `orbit_summary()`.

### n — mean motion
How fast the satellite goes around, on average.  
In GP JSON: **revolutions per day**.  
We convert to **radians per second** for math:

`n_rad_s = 2π × MEAN_MOTION / 86400`

**Period** (hours) ≈ `2π / n_rad_s / 3600`.

---

## The tilt

### i — inclination (degrees)
Angle between the orbit plane and Earth’s equator.
- **0°** → equatorial (SES-5 ≈ **0.05°**)
- **≈ 90°** → polar (PULSAR-0 ≈ **97.5°**, slightly retrograde)
- **≈ 55°** → Galileo-like MEO
- **≈ 39°** → QZS-2 IGSO

**Retrograde** means the satellite goes westbound relative to Earth’s spin (i > 90°).

---

## The foggy orientation angles (Ω and ω)

These say **how the ellipse is twisted in space**. They confuse everyone at first.

### Ω — RAAN (Right Ascension of the Ascending Node)
**Where** the orbit crosses the equator going **north**, measured in an inertial sky reference.

Plain picture:
1. Find the line where the orbit plane meets the equator.  
2. The **ascending node** is the crossing going north.  
3. **RAAN** is the angle that locates that node around Earth.

In JSON: `RA_OF_ASC_NODE` (degrees) → we store `raan_rad`.

Search: `RAAN explained animation`.

### ω — argument of perigee
Once the orbit plane is fixed, **where along that plane** is the low point (perigee)?  
**ω** is that angle, measured from the ascending node to perigee.

In JSON: `ARG_OF_PERICENTER` → `argp_rad`.

You need Ω and ω to place the ellipse correctly before asking “where is the satellite *on* the ellipse?”

---

## Where is the satellite on the ellipse? (M, E, ν)

### M — mean anomaly (foggy but important)
A **uniform clock angle** along the orbit: it increases steadily with time,

\[
M(t) = M_0 + n\,(t - t_{\text{epoch}})
\]

even though the satellite does **not** move at constant true speed on an oval.

- On a circle, mean anomaly matches the easy geometric angle.  
- On an oval, we must convert **M → E → true anomaly ν**.

In JSON: `MEAN_ANOMALY` → `M0_rad` at epoch.

Search: `mean anomaly vs true anomaly`.

### E — eccentric anomaly
A helper angle used in Kepler’s equation:

\[
M = E - e\sin E
\]

Code: `solve_kepler(M, e)` (Newton’s method).

### ν — true anomaly
The real “where on the ellipse from perigee” angle used for position.  
Then **u = ω + ν** (argument of latitude) feeds the 3D position formulas in `propagate()`.

---

## Workshop examples (what each element set “feels” like)

| Sat | a | e | i | Story |
|-----|---|---|---|--------|
| PULSAR-0 | small | tiny | ~97.5° | Low, near-polar, many revs/day |
| Galileo 29 | medium | tiniest | ~55° | GNSS / MEO |
| SES-5 | ~GEO | tiny | ~0° | Hangs over one longitude |
| QZS-2 | ~GEO | larger | ~39° | Same period class, but figure-8 IGSO |

## What if we used other satellites?

Same element meanings; different numbers change the plot:

| If you loaded… | You’d expect… |
|----------------|-----------------|
| **ISS** (`LIVE_GROUP="STATIONS"`) | LEO stripes like PULSAR, but i ≈ 51.6°, not polar |
| **Another GEO** | Another near-fixed longitude (maybe not 5°E) |
| **A Molniya / HEO** | Very large e → huge speed swing, long dwell at apogee |
| **Sun-synchronous LEO** | i near ~97–99°, ground tracks that keep similar lighting |

Next: [04 — Propagation & Earth](04-propagation-and-earth.md)
