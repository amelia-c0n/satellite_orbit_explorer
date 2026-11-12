"""
Satellite Orbit Explorer · built during Space Career Week 2026 · GNSS Academy

Educational project: retrieve orbital data, explain how satellites move,
compare orbits, and produce clear visualizations.

Stages:
  1) setup
  2) load GP JSON
  3) parse elements
  4) time window
  5) propagate
  6) orbit summary
  7) plots
  8) KML and report

Model: two-body Kepler orbit, spherical Earth, simple Greenwich rotation.
GP records hold SGP4 mean elements — this is an educational approximation,
not precision orbit prediction.

Conventions: UTC-aware datetimes, distances in km, speeds in km/s.
"""

import json
import math
import time
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path

import matplotlib.pyplot as plt
import requests
from matplotlib.colors import to_hex

# MU: Earth's gravitational parameter (km^3/s^2). Used later for orbit math
# (e.g. relating orbit size to orbital period and speed).
MU_EARTH_KM3_S2 = 398600.4418

# Mean equatorial Earth radius (km). Used for altitude and ground-track ideas.
EARTH_RADIUS_KM = 6378.137

# Paths: everything is relative to this script (works on your Mac, not Colab).
PROJECT_DIR = Path(__file__).resolve().parent
# IN_DIR expects: orbital_elements.json, data_manifest.json, world_map.txt
# (see data/input/README.md and the repo root README).
IN_DIR = PROJECT_DIR / "data" / "input"
OUT_DIR = PROJECT_DIR / "data" / "output"

IN_DIR.mkdir(parents=True, exist_ok=True)
OUT_DIR.mkdir(parents=True, exist_ok=True)

# How finely we sample the orbit (every 5 seconds) and for how long (24 hours).
STEP_SECONDS = 5
DURATION_HOURS = 24

# Optional later: live CelesTrak group download. Unused in Stage 1.
LIVE_GROUP = None

# Repo-root zip with workshop GP JSON and supporting files.
REPO_ROOT = PROJECT_DIR.parent
INPUT_ZIP = REPO_ROOT / "input_data" / "orbit_workshop_inputs.zip"


def unpack_workshop_inputs() -> None:
    """Unzip workshop GP JSON + map + manifest into IN_DIR. Do not invent files."""
    if not INPUT_ZIP.is_file():
        raise FileNotFoundError(
            f"Missing input zip: {INPUT_ZIP}\n"
            "Place orbit_workshop_inputs.zip under input_data/ and try again."
        )
    with zipfile.ZipFile(INPUT_ZIP, "r") as zf:
        zf.extractall(IN_DIR)


def print_configuration() -> None:
    """Show the Stage 1 setup so we can verify paths and constants."""
    print("Satellite Orbit Explorer — Stage 1 setup")
    print(f"  PROJECT_DIR     = {PROJECT_DIR}")
    print(f"  IN_DIR          = {IN_DIR}")
    print(f"  OUT_DIR         = {OUT_DIR}")
    print(f"  MU_EARTH_KM3_S2 = {MU_EARTH_KM3_S2}  # km^3/s^2")
    print(f"  EARTH_RADIUS_KM = {EARTH_RADIUS_KM}  # km")
    print(f"  STEP_SECONDS    = {STEP_SECONDS}")
    print(f"  DURATION_HOURS  = {DURATION_HOURS}")
    print(f"  LIVE_GROUP      = {LIVE_GROUP}")
    print(f"  INPUT_ZIP       = {INPUT_ZIP}")
    print(f"  IN_DIR files    = {sorted(p.name for p in IN_DIR.iterdir())}")


if __name__ == "__main__":
    # UTC keeps time unambiguous worldwide (no local daylight-saving surprises).
    unpack_workshop_inputs()
    print_configuration()
