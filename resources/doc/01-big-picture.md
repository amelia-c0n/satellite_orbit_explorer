# 01 — Big picture

## What this project answers

Given real public orbit data for a few satellites, we:

1. **Read** their orbit “snapshots”
2. **Translate** those numbers into simple geometry (size, tilt, ovalness, …)
3. **Predict** where each satellite is over **24 hours** (educational math)
4. **Compare** them (period, height, speed)
5. **Draw** ground tracks and speed plots
6. **Export** Google Earth files + a text report

Default data: workshop pack for **PULSAR-0**, **Galileo 29**, **SES-5**, **QZS-2**.

## The story in one paragraph

An orbit catalog entry is a **photo of the orbit at one instant** (the **epoch**).  
We pretend Earth is a smooth ball and gravity is simple (**two-body Kepler**).  
From that photo we advance time every few seconds, find the satellite’s place in space, then ask: “After Earth has rotated, where is that point over the map?” That path is the **ground track**. Speeds come from a simple energy formula (**vis-viva**).

## End-to-end pipeline (matches the code stages)

```text
Input zip / optional live CelesTrak
        ↓
  GP JSON records          ← Stage 2  (read_gp_json)
        ↓
  Kepler elements          ← Stage 3  (parse_gp_elements)
        ↓
  Shared UTC time grid     ← Stage 4  (build_time_grid)
        ↓
  Lat, lon, alt, speed     ← Stage 5  (propagate, solve_kepler, gmst_rad)
        ↓
  Summary table            ← Stage 6  (orbit_summary)
        ↓
  PNG plots                ← Stage 7  (plot_ground_tracks, …)
        ↓
  KML + report + zip       ← Stage 8
```

Optional Stage 9: set `LIVE_GROUP` to download another CelesTrak list (e.g. space stations).

## Two ideas to keep straight

1. **Catalog math (SGP4 world)** — How the official GP numbers were produced (fancy).  
2. **Our classroom math (Kepler world)** — How *this* project moves the satellite (simple).

We **reuse GP numbers** as if they were Kepler elements. That is useful for learning and comparing orbit *types*, but it is **not** precision flight dynamics.

## What “success” looks like in the outputs

- **PULSAR-0:** many LEO stripes shifting west  
- **Galileo:** wide wavy MEO track  
- **SES-5:** almost one spot near **~5°E** on the equator  
- **QZS-2:** figure-8 style IGSO path; bigger speed changes  

Next: [02 — Data & acronyms](02-data-and-acronyms.md)
