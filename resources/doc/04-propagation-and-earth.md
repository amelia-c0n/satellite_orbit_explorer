# 04 — Propagation & Earth

**Propagation** = “move the satellite forward in time from its epoch.”  
Code centerpiece: `propagate(el, times)` with helpers `solve_kepler()` and `gmst_rad()`.

---

## Shared time window (Stage 4)

We build **one UTC grid** for all satellites so plots line up:

- `start` = newest epoch, floored to **UTC midnight**
- `end` = start + `DURATION_HOURS` (24)
- sample every `STEP_SECONDS` (5) → **17 281** points including both ends

Code: `build_time_grid()`.

Each satellite still uses **its own epoch** inside the formulas.  
Offset `start − epoch` large ⇒ more stale (workshop **QZS-2**).

---

## The seven steps inside `propagate` (classroom physics)

### 1) Advance mean anomaly
\[
M = M_0 + n(t - t_{\text{epoch}}) \quad (\bmod 2\pi)
\]
Steady clock angle from epoch.

### 2) Solve Kepler’s equation → E
\[
M = E - e\sin E
\]
Code: `solve_kepler`.

### 3) Radius and true anomaly
- Distance from Earth center: \( r = a(1 - e\cos E) \)  
- True anomaly ν from E  
- \( u = \omega + \nu \)

### 4) Position in inertial space (x, y, z)
Rotate by Ω (RAAN), i (inclination), and u.  
This is “where in space, ignoring Earth’s spin for a moment.”

### 5) Rotate into Earth-fixed axes with GMST (foggy bit)
Earth spins. To get a point **over the map**, we rotate around Earth’s axis by **GMST**.

**GMST** = **Greenwich Mean Sidereal Time**  
Roughly: “how far has Greenwich moved under the stars?”  
We use the IAU-1982 / Meeus polynomial in `gmst_rad(t)`.

Search: `sidereal time vs solar time`, `GMST satellite ground track`.

After rotation we have Earth-fixed `(x′, y′, z)`.

### 6) Latitude, longitude, altitude
- lat / lon from the Earth-fixed vector (spherical Earth)  
- altitude ≈ `r − EARTH_RADIUS_KM`

### 7) Speed (vis-viva)
\[
v = \sqrt{\mu\left(\frac{2}{r} - \frac{1}{a}\right)}
\]
Faster when **r** is smaller (near perigee).  
That’s why **QZS-2** shows the biggest speed swing.

---

## Ground tracks

A **ground track** is the sequence of (lon, lat) over time.

Why scatter dots (not one long line)?  
Crossing **±180°** longitude would draw a fake line across the map. Dots avoid that.  
Code: `plot_ground_tracks()`; coastline from `load_coastline()`.

### What our four tracks teach
- **PULSAR-0:** many passes; Earth turns under a fast LEO → tracks shift west  
- **Galileo:** fewer, wider waves (MEO)  
- **SES-5:** period ≈ one sidereal day + i≈0 → **almost one point** (~5°E)  
- **QZS-2:** ~same period class but tilted + eccentric → **asymmetric figure-8**

### What other sats would do
- **ISS:** LEO bands at ~51.6° latitude reach (not polar)  
- **True polar 90°:** tracks toward the poles  
- **Another GEO:** another fixed longitude  
- **Highly eccentric HEO:** long slow dwell near apogee longitude/latitude

---

## Frames in plain language

| Idea | Plain meaning |
|------|----------------|
| **Inertial** | Axes that don’t spin with Earth (good for orbit geometry) |
| **Earth-fixed / ECEF** | Axes glued to Earth (good for lat/lon) |
| **GMST** | The bridge angle between those two for our simple model |

We keep Earth **spherical**. Real Earth is slightly squashed; SGP4 cares more about that than we do here.

---

## Sanity checks in the code

- GMST at J2000 ≈ 280.46°  
- Kepler residual very small  
- If SES-5 is present: longitude stays about **4°–6°E** (rotation sign check)  
- If Galileo 29 is present: period about **14.0–14.2 h**

Code: `run_propagation_checks()`, `check_galileo_period()`.

Next: [05 — Orbit families](05-orbit-families.md)
