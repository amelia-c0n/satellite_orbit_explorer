# Learning Kepler orbits & the theory behind this project

Use this when the code feels confusing. Learn in **layers** — intuition first, equations later.

You can add more links here as you study.

---

## 1. Start here (intuition, little math)

### What an orbit is
Gravity pulls you into a continuous “fall” around Earth.

- NASA — [Orbits and Kepler’s Laws](https://science.nasa.gov/learn/basics-of-space-flight/chapter5-1/)  
  (*Basics of Space Flight*, Chapter 5)

### Shape words we use
Circle vs oval (`e`), tilt (`i`), size (`a`).

- Example orbital-elements animation:  
  [YouTube — orbital elements explained](https://www.youtube.com/watch?v=QZrYaKwZwhI)  
  (add more useful videos here later)

---

## 2. Then match our project (same order as the code)

| Idea | Plain meaning | Where it shows up for us |
|------|----------------|---------------------------|
| Epoch | “This snapshot is valid at this time” | Stages 2–4 |
| a, e, i, Ω, ω, M | Size, ovalness, tilt, orientation, where along the track | Stage 3 |
| Kepler’s equation | Turn “time along orbit” into position on the ellipse | Stage 5 `solve_kepler` |
| GMST | Earth has rotated under the satellite | Stage 5 `gmst_rad` |
| Lat / lon / alt | Where it is over the map | Stage 5 `propagate` |

---

## 3. Best free next reads

- **NASA Basics of Space Flight — Chapter 5** (linked above): clearest official intro
- **CelesTrak / T.S. Kelso** — [GP data formats](https://celestrak.org/NORAD/documentation/gp-data-formats.php): more “data” than physics, but good context for why TLEs / GP exist
- Short visuals: search **“orbital elements 3D animation”** (RAAN / argument of perigee click faster with a picture)

---

## 4. One gentle book later (optional)

- *It’s ONLY Rocket Science* (Lucy Rogers), or another “spaceflight for beginners” overview — not a homework textbook
- Skip heavy engineering books until the pictures make sense

---

## 5. How to use *our* project as the textbook

When something feels foggy, pick **one symbol at a time** (e.g. only `e`, or only GMST) and look at **PULSAR-0 vs SES-5** numbers from the Stage 3 table. Concrete satellite examples usually stick better than abstract theory.

Our model reminder: GP records are **SGP4 mean elements**. The Kepler + spherical-Earth + GMST path in this project is an **educational approximation**, not precision orbit prediction.
