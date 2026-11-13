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

# Optional later: live CelesTrak group download. Unused in early stages.
LIVE_GROUP = None

# Repo-root zip with workshop GP JSON and supporting files.
REPO_ROOT = PROJECT_DIR.parent
INPUT_ZIP = REPO_ROOT / "input_data" / "orbit_workshop_inputs.zip"

REQUIRED_INPUT_FILES = (
    "orbital_elements.json",
    "data_manifest.json",
    "world_map.txt",
)

# Fields every CelesTrak GP / OMM JSON record must have for this project.
REQUIRED_GP_FIELDS = (
    "OBJECT_NAME",
    "NORAD_CAT_ID",
    "EPOCH",
    "MEAN_MOTION",
    "ECCENTRICITY",
    "INCLINATION",
    "RA_OF_ASC_NODE",
    "ARG_OF_PERICENTER",
    "MEAN_ANOMALY",
)


def extract_inputs() -> None:
    """Ensure the three workshop input files are in IN_DIR (no invented data)."""
    missing = [name for name in REQUIRED_INPUT_FILES if not (IN_DIR / name).is_file()]

    if not missing:
        print(f"Input files already present in {IN_DIR}")
    else:
        if not INPUT_ZIP.is_file() or not zipfile.is_zipfile(INPUT_ZIP):
            raise FileNotFoundError(
                f"Missing or invalid input zip: {INPUT_ZIP}\n"
                "Place orbit_workshop_inputs.zip under input_data/ and try again."
            )
        print(f"Extracting {', '.join(REQUIRED_INPUT_FILES)} from {INPUT_ZIP}")
        with zipfile.ZipFile(INPUT_ZIP, "r") as zf:
            names_in_zip = set(zf.namelist())
            for name in REQUIRED_INPUT_FILES:
                if name not in names_in_zip:
                    raise FileNotFoundError(f"Zip is missing required file: {name}")
                zf.extract(name, IN_DIR)

    still_missing = [name for name in REQUIRED_INPUT_FILES if not (IN_DIR / name).is_file()]
    if still_missing:
        raise FileNotFoundError(
            "Required input file(s) missing after extract: "
            + ", ".join(still_missing)
        )


def read_gp_json(path: Path) -> list:
    """Load CelesTrak GP JSON (OMM field names) and check required fields.

    OMM JSON is easier than classic TLEs: fields have clear names instead of
    fixed character columns, and dates use ISO-8601. It also supports six-digit
    catalog numbers, which the old 5-digit TLE format cannot store.
    """
    with path.open(encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError(f"Expected a JSON list of GP records in {path}")

    for i, record in enumerate(data):
        if not isinstance(record, dict):
            raise ValueError(f"GP record {i} is not an object in {path}")
        missing = [key for key in REQUIRED_GP_FIELDS if key not in record]
        if missing:
            raise ValueError(
                f"GP record {i} missing field(s) {missing} in {path}"
            )

    return data


def parse_gp_epoch(text: str) -> datetime:
    """Parse a CelesTrak EPOCH string as UTC (no offset in the text)."""
    return datetime.fromisoformat(text.rstrip("Z")).replace(tzinfo=timezone.utc)


def parse_gp_elements(rec: dict) -> dict:
    """Convert one GP record into Kepler elements in model units (km, rad, s).

    GP field → symbol / conversion (SGP4 mean elements; two-body use is approximate):
      MEAN_MOTION       n     rev/day → rad/s  (× 2π / 86400)
      (derived)         a     km via Kepler    a = (μ / n²)^(1/3)
      ECCENTRICITY      e     already decimal  (unitless)
      INCLINATION       i     deg → rad
      RA_OF_ASC_NODE    Ω     deg → rad
      ARG_OF_PERICENTER ω     deg → rad
      MEAN_ANOMALY      M₀    deg → rad
      EPOCH             t₀    ISO text → UTC datetime
    """
    name = rec["OBJECT_NAME"]
    norad_id = int(rec["NORAD_CAT_ID"])
    n_rad_s = 2.0 * math.pi * float(rec["MEAN_MOTION"]) / 86400.0
    a_km = (MU_EARTH_KM3_S2 / n_rad_s**2) ** (1.0 / 3.0)

    return {
        "name": name,
        "norad_id": norad_id,
        "label": f"{name} [{norad_id}]",
        "epoch": parse_gp_epoch(rec["EPOCH"]),
        "n_rad_s": n_rad_s,
        "a_km": a_km,
        "e": float(rec["ECCENTRICITY"]),
        "i_rad": math.radians(float(rec["INCLINATION"])),
        "raan_rad": math.radians(float(rec["RA_OF_ASC_NODE"])),
        "argp_rad": math.radians(float(rec["ARG_OF_PERICENTER"])),
        "M0_rad": math.radians(float(rec["MEAN_ANOMALY"])),
    }


def elements_table(elements: list) -> list[str]:
    """Return text-table lines for orbit elements (angles shown in degrees)."""
    headers = (
        f"{'name':<28} {'NORAD':>6}  {'epoch_utc':<24}  "
        f"{'a_km':>10}  {'e':>10}  "
        f"{'i_deg':>8}  {'raan_deg':>9}  {'argp_deg':>9}  {'M0_deg':>8}"
    )
    lines = [headers, "-" * len(headers)]
    for el in elements:
        lines.append(
            f"{el['name']:<28} {el['norad_id']:>6}  "
            f"{el['epoch'].strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]:<24}  "
            f"{el['a_km']:>10.3f}  {el['e']:>10.7f}  "
            f"{math.degrees(el['i_rad']):>8.4f}  "
            f"{math.degrees(el['raan_rad']):>9.4f}  "
            f"{math.degrees(el['argp_rad']):>9.4f}  "
            f"{math.degrees(el['M0_rad']):>8.4f}"
        )
    return lines


def print_configuration() -> None:
    """Show the Stage 1 setup so we can verify paths and constants."""
    print("Satellite Orbit Explorer — configuration")
    print(f"  PROJECT_DIR     = {PROJECT_DIR}")
    print(f"  IN_DIR          = {IN_DIR}")
    print(f"  OUT_DIR         = {OUT_DIR}")
    print(f"  MU_EARTH_KM3_S2 = {MU_EARTH_KM3_S2}  # km^3/s^2")
    print(f"  EARTH_RADIUS_KM = {EARTH_RADIUS_KM}  # km")
    print(f"  STEP_SECONDS    = {STEP_SECONDS}")
    print(f"  DURATION_HOURS  = {DURATION_HOURS}")
    print(f"  LIVE_GROUP      = {LIVE_GROUP}")
    print(f"  INPUT_ZIP       = {INPUT_ZIP}")


def build_time_grid(elements: list) -> tuple[datetime, datetime, list[datetime]]:
    """One common UTC grid for all satellites (includes both ends).

    Each GP record is still propagated from its own epoch, so prediction error
    grows with (start - epoch). The workshop QZS-2 record is from 2026-10-17.
    """
    if not elements:
        raise ValueError("elements is empty; load and parse GP records first")

    newest_epoch = max(el["epoch"] for el in elements)
    start = datetime(
        newest_epoch.year, newest_epoch.month, newest_epoch.day, tzinfo=timezone.utc
    )
    end = start + timedelta(hours=DURATION_HOURS)
    step = timedelta(seconds=STEP_SECONDS)
    n_points = (end - start) // step + 1
    times = [start + i * step for i in range(n_points)]
    return start, end, times


def print_epoch_offsets(elements: list, start: datetime) -> None:
    """Print start-minus-epoch offsets; flag records older than 7 days as stale."""
    print("Epoch offsets relative to common window start:")
    for el in elements:
        offset_days = (start - el["epoch"]).total_seconds() / 86400.0
        stale = "  STALE RECORD (>7 days)" if offset_days > 7.0 else ""
        print(
            f"  {el['label']}: epoch={el['epoch'].isoformat()}  "
            f"offset={offset_days:.3f} days{stale}"
        )


# J2000 epoch for GMST (IAU-1982 / Meeus): 2000-01-01 12:00 UTC
J2000_UTC = datetime(2000, 1, 1, 12, 0, 0, tzinfo=timezone.utc)


def solve_kepler(M: float, e: float, tol: float = 1e-12, max_iter: int = 50) -> float:
    """Solve Kepler's equation M = E - e*sin(E) with Newton-Raphson."""
    M = math.fmod(M, 2.0 * math.pi)
    if M < 0.0:
        M += 2.0 * math.pi

    E = math.pi if e > 0.8 else M
    for _ in range(max_iter):
        f = E - e * math.sin(E) - M
        fp = 1.0 - e * math.cos(E)
        delta = f / fp
        E -= delta
        if abs(f) < tol and abs(delta) < tol:
            return E
    raise RuntimeError(
        f"solve_kepler did not converge in {max_iter} iterations "
        f"(M={M}, e={e}, residual={E - e * math.sin(E) - M})"
    )


def gmst_rad(t: datetime) -> float:
    """Greenwich Mean Sidereal Time [rad], IAU-1982 (Meeus eq. 12.4)."""
    if t.tzinfo is None:
        raise ValueError("gmst_rad expects a timezone-aware UTC datetime")
    d = (t.astimezone(timezone.utc) - J2000_UTC).total_seconds() / 86400.0
    T = d / 36525.0
    theta_deg = (
        280.46061837
        + 360.98564736629 * d
        + 0.000387933 * T**2
        - T**3 / 38710000.0
    )
    theta_deg = theta_deg % 360.0
    if theta_deg < 0.0:
        theta_deg += 360.0
    return math.radians(theta_deg)


def propagate(el: dict, times: list) -> list:
    """Propagate one satellite on the shared UTC grid (educational two-body model)."""
    if not times:
        raise ValueError("times is empty; build the Stage 4 time grid first")

    a = el["a_km"]
    e = el["e"]
    i = el["i_rad"]
    raan = el["raan_rad"]
    argp = el["argp_rad"]
    M0 = el["M0_rad"]
    n = el["n_rad_s"]
    epoch = el["epoch"]
    mu = MU_EARTH_KM3_S2

    points = []
    for t in times:
        # 1) Mean anomaly advances from epoch: M = M0 + n*(t - epoch), mod 2π
        dt_s = (t - epoch).total_seconds()
        M = (M0 + n * dt_s) % (2.0 * math.pi)

        # 2) Solve Kepler's equation for eccentric anomaly E
        E = solve_kepler(M, e)

        # 3) Radius, true anomaly ν, and argument of latitude u = ω + ν
        cos_E = math.cos(E)
        sin_E = math.sin(E)
        r = a * (1.0 - e * cos_E)
        nu = math.atan2(math.sqrt(1.0 - e * e) * sin_E, cos_E - e)
        u = argp + nu

        # 4) Position in inertial (equatorial) axes
        cos_u = math.cos(u)
        sin_u = math.sin(u)
        cos_raan = math.cos(raan)
        sin_raan = math.sin(raan)
        cos_i = math.cos(i)
        sin_i = math.sin(i)
        x = r * (cos_raan * cos_u - sin_raan * sin_u * cos_i)
        y = r * (sin_raan * cos_u + cos_raan * sin_u * cos_i)
        z = r * (sin_u * sin_i)

        # 5) Rotate by GMST into Earth-fixed axes (simple Greenwich rotation)
        theta = gmst_rad(t)
        cos_th = math.cos(theta)
        sin_th = math.sin(theta)
        x_ecef = cos_th * x + sin_th * y
        y_ecef = -sin_th * x + cos_th * y

        # 6) Spherical lat/lon [deg] and altitude above spherical Earth [km]
        lat_deg = math.degrees(math.atan2(z, math.hypot(x_ecef, y_ecef)))
        lon_deg = math.degrees(math.atan2(y_ecef, x_ecef))
        alt_km = r - EARTH_RADIUS_KM

        # 7) Vis-viva orbital speed [km/s]
        speed_km_s = math.sqrt(mu * (2.0 / r - 1.0 / a))

        points.append(
            {
                "time": t,
                "lat_deg": lat_deg,
                "lon_deg": lon_deg,
                "alt_km": alt_km,
                "speed_km_s": speed_km_s,
            }
        )
    return points


def run_propagation_checks(elements: list, tracks: list) -> None:
    """Sanity checks for Kepler, GMST, and SES-5 longitude (no forced offsets)."""
    # GMST at J2000 ≈ 280.46 degrees
    gmst_j2000_deg = math.degrees(gmst_rad(J2000_UTC))
    assert abs(gmst_j2000_deg - 280.46) < 0.01, (
        f"GMST at J2000 expected ~280.46 deg, got {gmst_j2000_deg}"
    )

    # Kepler residual below 1e-10 for a few (M, e) samples
    for M_sample, e_sample in ((0.0, 0.0), (1.0, 0.1), (math.pi, 0.5), (5.0, 0.75)):
        E = solve_kepler(M_sample, e_sample)
        M_wrapped = M_sample % (2.0 * math.pi)
        if M_wrapped < 0.0:
            M_wrapped += 2.0 * math.pi
        residual = abs(E - e_sample * math.sin(E) - M_wrapped)
        assert residual < 1e-10, (
            f"Kepler residual {residual} for M={M_sample}, e={e_sample}"
        )

    # SES-5 (NORAD 38652) should sit near ~5°E if GMST / rotation signs are correct
    if len(elements) != len(tracks):
        raise ValueError("elements and tracks length mismatch")
    for el, track in zip(elements, tracks):
        if el["norad_id"] != 38652:
            continue
        if not track:
            raise ValueError("SES-5 track is empty")
        lons = [p["lon_deg"] for p in track]
        lon_min, lon_max = min(lons), max(lons)
        assert 4.0 <= lon_min and lon_max <= 6.0, (
            "SES-5 longitude should stay between 4° and 6° East; "
            f"got [{lon_min:.3f}, {lon_max:.3f}]. "
            "Check GMST or ECEF rotation signs — do not add a longitude offset."
        )
        print(
            f"SES-5 longitude check OK: "
            f"[{lon_min:.3f}, {lon_max:.3f}] deg East"
        )
        break


def print_track_samples(elements: list, tracks: list) -> None:
    """Print first, middle, and last propagated point for each satellite."""
    if len(elements) != len(tracks):
        raise ValueError("elements and tracks length mismatch")
    print("Propagation samples (first / middle / last):")
    for el, track in zip(elements, tracks):
        if not track:
            raise ValueError(f"Empty track for {el['label']}")
        mid = len(track) // 2
        print(f"  {el['label']}")
        for tag, p in (("first", track[0]), ("middle", track[mid]), ("last", track[-1])):
            print(
                f"    {tag:6s}  {p['time'].isoformat()}  "
                f"lat={p['lat_deg']:8.3f}  lon={p['lon_deg']:8.3f}  "
                f"alt_km={p['alt_km']:8.1f}  speed_km_s={p['speed_km_s']:6.3f}"
            )


def orbit_summary(el: dict, pts: list) -> dict:
    """Compute period, altitudes, and speed range for one satellite.

    Workshop interpretation (approximate two-body values from GP means):
      PULSAR-0  ~1.58 h, i~97.5°  → retrograde near-polar (sun-synchronous-class)
      Galileo 29 ~14.08 h         → MEO / GNSS
      SES-5 / QZS-2 ~23.93 h      → about one sidereal day (geosynchronous)
      QZS-2 e~0.07, i~39°         → IGSO (inclined geosynchronous), not geostationary
    """
    if not pts:
        raise ValueError(f"No propagated points for {el.get('label', el.get('name'))}")

    speeds = [p["speed_km_s"] for p in pts]
    a = el["a_km"]
    e = el["e"]
    return {
        "name": el["name"],
        "norad_id": el["norad_id"],
        "period_h": 2.0 * math.pi / el["n_rad_s"] / 3600.0,
        "perigee_km": a * (1.0 - e) - EARTH_RADIUS_KM,
        "apogee_km": a * (1.0 + e) - EARTH_RADIUS_KM,
        "e": e,
        "i_deg": math.degrees(el["i_rad"]),
        "speed_min_km_s": min(speeds),
        "speed_max_km_s": max(speeds),
    }


def summary_table(summaries: list) -> list[str]:
    """Return text-table lines for orbit summaries (reused in Stage 8)."""
    headers = (
        f"{'name':<28} {'NORAD':>6}  {'period_h':>8}  "
        f"{'perigee_km':>10}  {'apogee_km':>10}  {'e':>10}  {'i_deg':>8}  "
        f"{'vmin':>6}  {'vmax':>6}"
    )
    lines = [headers, "-" * len(headers)]
    for s in summaries:
        lines.append(
            f"{s['name']:<28} {s['norad_id']:>6}  {s['period_h']:>8.3f}  "
            f"{s['perigee_km']:>10.1f}  {s['apogee_km']:>10.1f}  "
            f"{s['e']:>10.7f}  {s['i_deg']:>8.4f}  "
            f"{s['speed_min_km_s']:>6.3f}  {s['speed_max_km_s']:>6.3f}"
        )
    return lines


def check_galileo_period(summaries: list) -> None:
    """Galileo 29 (NORAD 59598) should have period ~14.08 h."""
    for s in summaries:
        if s["norad_id"] != 59598:
            continue
        assert 14.0 <= s["period_h"] <= 14.2, (
            f"Galileo 29 period_h expected in [14.0, 14.2], got {s['period_h']}"
        )
        print(f"Galileo 29 period check OK: {s['period_h']:.4f} h")
        break


# One color per satellite (Stage 8 reuses this list).
COLORS = ["tab:blue", "tab:orange", "tab:green", "tab:red"]


def load_coastline(path: Path) -> list:
    """Load world_map.txt: 'latitude longitude' lines; blank lines split segments.

    Returns a list of segments of (lon, lat) points. Never join across blanks —
    that would draw false lines across oceans.
    """
    if not path.is_file():
        raise FileNotFoundError(f"Missing coastline file: {path}")

    segments: list[list[tuple[float, float]]] = []
    current: list[tuple[float, float]] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            text = line.strip()
            if not text:
                if current:
                    segments.append(current)
                    current = []
                continue
            lat_s, lon_s = text.split()
            # File order is latitude first; we store (lon, lat) for plotting.
            current.append((float(lon_s), float(lat_s)))
    if current:
        segments.append(current)
    if not segments:
        raise ValueError(f"No coastline segments found in {path}")
    return segments


def plot_ground_tracks(elements: list, tracks: list, coastline: list) -> Path:
    """Figure 1: gray coast + scatter ground tracks (dots avoid ±180° false lines).

    What you should see (workshop sats):
      PULSAR-0 — many passes shifting west (fast LEO + Earth rotation)
      Galileo  — a wide wave (MEO)
      SES-5    — one spot (period ≈ Earth rotation; geostationary-like)
      QZS-2    — asymmetric figure-8 (IGSO: ~sidereal day, i≈39°, slow N apogee)
    """
    if len(elements) != len(tracks):
        raise ValueError("elements and tracks length mismatch")

    fig, ax = plt.subplots(figsize=(11, 5.5))
    for segment in coastline:
        lons = [p[0] for p in segment]
        lats = [p[1] for p in segment]
        ax.plot(lons, lats, color="0.6", linewidth=0.4, zorder=1)

    for i, (el, track) in enumerate(zip(elements, tracks)):
        color = COLORS[i % len(COLORS)]
        lons = [p["lon_deg"] for p in track]
        lats = [p["lat_deg"] for p in track]
        ax.scatter(
            lons,
            lats,
            s=2,
            c=color,
            label=el["label"],
            zorder=2,
            linewidths=0,
        )

    ax.set_xlim(-180, 180)
    ax.set_ylim(-90, 90)
    ax.set_xlabel("Longitude [deg]")
    ax.set_ylabel("Latitude [deg]")
    ax.set_title("Ground tracks (24 h educational Kepler propagation)")
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, linewidth=0.3, alpha=0.5)
    ax.legend(loc="upper left", fontsize=8, markerscale=3)
    fig.tight_layout()

    out_path = OUT_DIR / "ground_tracks.png"
    fig.savefig(out_path, dpi=200)
    plt.show()
    plt.close(fig)
    return out_path


def plot_speed_timeseries(elements: list, tracks: list) -> Path:
    """Figure 2: stacked speed [km/s] vs UTC time.

    Eccentric orbits (esp. QZS-2) speed up near perigee and slow near apogee.
    """
    if len(elements) != len(tracks):
        raise ValueError("elements and tracks length mismatch")
    if not elements:
        raise ValueError("elements is empty")

    n = len(elements)
    fig, axes = plt.subplots(
        n, 1, sharex=True, figsize=(11, 2.2 * n), squeeze=False
    )
    for i, (el, track) in enumerate(zip(elements, tracks)):
        ax = axes[i, 0]
        color = COLORS[i % len(COLORS)]
        times_plot = [p["time"] for p in track]
        speeds = [p["speed_km_s"] for p in track]
        ax.plot(times_plot, speeds, color=color, linewidth=1.0)
        ax.set_ylabel("km/s")
        ax.set_title(el["label"], fontsize=10, loc="left")
        ax.grid(True, linewidth=0.3, alpha=0.5)
        ax.ticklabel_format(axis="y", useOffset=False)

    axes[-1, 0].set_xlabel("UTC time")
    fig.suptitle("Orbital speed vs time (vis-viva)", fontsize=12)
    fig.tight_layout()

    out_path = OUT_DIR / "velocity_timeseries.png"
    fig.savefig(out_path, dpi=200)
    plt.show()
    plt.close(fig)
    return out_path


# KML 2.2 + Google Earth gx extensions
KML_NS = "http://www.opengis.net/kml/2.2"
GX_NS = "http://www.google.com/kml/ext/2.2"
ET.register_namespace("", KML_NS)
ET.register_namespace("gx", GX_NS)

KML_ICON_HREF = "http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png"
ANIM_STEP_SECONDS = 60  # subsample 5 s grid to one point per minute for animation


def _kml(tag: str) -> str:
    return f"{{{KML_NS}}}{tag}"


def _gx(tag: str) -> str:
    return f"{{{GX_NS}}}{tag}"


def matplotlib_color_to_kml_abgr(color) -> str:
    """Convert Matplotlib colour to KML aabbggrr (e.g. tab:blue #1f77b4 → ffb4771f)."""
    hex_rrggbb = to_hex(color).lstrip("#")
    if len(hex_rrggbb) != 6:
        raise ValueError(f"Expected RRGGBB hex from to_hex, got {hex_rrggbb!r}")
    rr, gg, bb = hex_rrggbb[0:2], hex_rrggbb[2:4], hex_rrggbb[4:6]
    return f"ff{bb}{gg}{rr}"


def _add_kml_style(document: ET.Element, style_id: str, color_abgr: str) -> None:
    """Icon + line style; white circle icon so the colour tint shows."""
    style = ET.SubElement(document, _kml("Style"), {"id": style_id})
    icon_style = ET.SubElement(style, _kml("IconStyle"))
    ET.SubElement(icon_style, _kml("color")).text = color_abgr
    icon = ET.SubElement(icon_style, _kml("Icon"))
    ET.SubElement(icon, _kml("href")).text = KML_ICON_HREF
    line_style = ET.SubElement(style, _kml("LineStyle"))
    ET.SubElement(line_style, _kml("color")).text = color_abgr
    ET.SubElement(line_style, _kml("width")).text = "2"


def _write_kml(path: Path, root: ET.Element) -> Path:
    tree = ET.ElementTree(root)
    tree.write(path, encoding="utf-8", xml_declaration=True)
    return path


def write_orbit_tracks_ecef_kml(elements: list, tracks: list) -> Path:
    """Earth-fixed 3D orbits: one absolute LineString per satellite (alt in metres)."""
    if len(elements) != len(tracks):
        raise ValueError("elements and tracks length mismatch")

    root = ET.Element(_kml("kml"))
    document = ET.SubElement(root, _kml("Document"))
    ET.SubElement(document, _kml("name")).text = "Multi-Satellite Orbits | Earth-fixed"

    for i, (el, track) in enumerate(zip(elements, tracks)):
        if not track:
            raise ValueError(f"Empty track for {el['label']}")
        style_id = f"style-{el['norad_id']}"
        color_abgr = matplotlib_color_to_kml_abgr(COLORS[i % len(COLORS)])
        _add_kml_style(document, style_id, color_abgr)

        placemark = ET.SubElement(document, _kml("Placemark"))
        ET.SubElement(placemark, _kml("name")).text = el["label"]
        ET.SubElement(placemark, _kml("styleUrl")).text = f"#{style_id}"
        line = ET.SubElement(placemark, _kml("LineString"))
        ET.SubElement(line, _kml("altitudeMode")).text = "absolute"
        # KML coordinates: lon,lat,alt_m (space-separated points)
        coords = " ".join(
            f"{p['lon_deg']:.6f},{p['lat_deg']:.6f},{p['alt_km'] * 1000.0:.1f}"
            for p in track
        )
        ET.SubElement(line, _kml("coordinates")).text = coords

    return _write_kml(OUT_DIR / "orbit_tracks_ecef.kml", root)


def _subsample_track_60s(track: list) -> list:
    """Keep one propagated point per ANIM_STEP_SECONDS."""
    if STEP_SECONDS <= 0 or ANIM_STEP_SECONDS % STEP_SECONDS != 0:
        raise ValueError("ANIM_STEP_SECONDS must be a multiple of STEP_SECONDS")
    stride = ANIM_STEP_SECONDS // STEP_SECONDS
    return track[::stride]


def _split_tracks_at_dateline(points: list) -> list[list]:
    """Start a new segment wherever longitude jumps by more than 180°."""
    if not points:
        return []
    segments = [[points[0]]]
    for prev, cur in zip(points, points[1:]):
        if abs(cur["lon_deg"] - prev["lon_deg"]) > 180.0:
            segments.append([cur])
        else:
            segments[-1].append(cur)
    return segments


def write_orbit_animation_kml(elements: list, tracks: list) -> Path:
    """Animated ground tracks: gx:MultiTrack, clampToGround, date-line splits."""
    if len(elements) != len(tracks):
        raise ValueError("elements and tracks length mismatch")

    root = ET.Element(_kml("kml"))
    document = ET.SubElement(root, _kml("Document"))
    ET.SubElement(document, _kml("name")).text = (
        "Multi-Satellite Ground Tracks | Animation"
    )

    for i, (el, track) in enumerate(zip(elements, tracks)):
        if not track:
            raise ValueError(f"Empty track for {el['label']}")
        style_id = f"style-anim-{el['norad_id']}"
        color_abgr = matplotlib_color_to_kml_abgr(COLORS[i % len(COLORS)])
        _add_kml_style(document, style_id, color_abgr)

        placemark = ET.SubElement(document, _kml("Placemark"))
        ET.SubElement(placemark, _kml("name")).text = el["label"]
        ET.SubElement(placemark, _kml("styleUrl")).text = f"#{style_id}"
        multi = ET.SubElement(placemark, _gx("MultiTrack"))

        for segment in _split_tracks_at_dateline(_subsample_track_60s(track)):
            gx_track = ET.SubElement(multi, _gx("Track"))
            ET.SubElement(gx_track, _kml("altitudeMode")).text = "clampToGround"
            # All <when> first, then matching <gx:coord> (KML Track convention)
            for p in segment:
                t = p["time"].astimezone(timezone.utc)
                ET.SubElement(gx_track, _kml("when")).text = t.strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                )
            for p in segment:
                ET.SubElement(gx_track, _gx("coord")).text = (
                    f"{p['lon_deg']:.6f} {p['lat_deg']:.6f} 0"
                )

    return _write_kml(OUT_DIR / "orbit_animation.kml", root)


def write_orbit_report(
    path: Path,
    source_note: str,
    start: datetime,
    end: datetime,
    elements: list,
    summaries: list,
) -> Path:
    """Plain-text report for demo/submit (reuses summary and elements tables)."""
    model_caveat = (
        "Model caveat: educational two-body Kepler + spherical Earth + GMST; "
        "GP values are SGP4 mean elements — not precision orbit prediction."
    )
    lines = [
        "Satellite Orbit Report - built during Space Career Week 2026, GNSS Academy",
        source_note,
        (
            f"Window: {start.isoformat()} → {end.isoformat()}  "
            f"(DURATION_HOURS={DURATION_HOURS}, STEP_SECONDS={STEP_SECONDS})"
        ),
        model_caveat,
        "",
        "Orbit summary:",
        *summary_table(summaries),
        "",
        "Kepler elements:",
        *elements_table(elements),
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def zip_orbit_outputs(paths: list[Path]) -> Path:
    """Zip the five deliverables into OUT_DIR / satellite_orbit_outputs.zip."""
    if len(paths) != 5:
        raise ValueError(f"Expected 5 output files to zip, got {len(paths)}")
    for p in paths:
        if not p.is_file():
            raise FileNotFoundError(f"Missing output to zip: {p}")

    zip_path = OUT_DIR / "satellite_orbit_outputs.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for p in paths:
            zf.write(p, arcname=p.name)
    return zip_path


if __name__ == "__main__":
    # UTC keeps time unambiguous worldwide (no local daylight-saving surprises).
    extract_inputs()
    print_configuration()

    sats = read_gp_json(IN_DIR / "orbital_elements.json")
    with (IN_DIR / "data_manifest.json").open(encoding="utf-8") as f:
        data_manifest = json.load(f)

    source_note = (
        "Native CelesTrak GP JSON (OMM field names) retrieved_utc="
        f"{data_manifest['retrieved_utc']}"
    )
    print(source_note)
    for sat in sats:
        print(
            f"  {sat['OBJECT_NAME']}  NORAD={sat['NORAD_CAT_ID']}  "
            f"EPOCH={sat['EPOCH']}"
        )

    elements = [parse_gp_elements(s) for s in sats]
    print("Kepler elements (two-body units; GP mean elements → approximate):")
    for line in elements_table(elements):
        print(line)

    start, end, times = build_time_grid(elements)
    n_points = len(times)
    print("Common UTC time window:")
    print(f"  start          = {start.isoformat()}")
    print(f"  end            = {end.isoformat()}")
    print(f"  DURATION_HOURS = {DURATION_HOURS}")
    print(f"  STEP_SECONDS   = {STEP_SECONDS}")
    print(f"  n_points       = {n_points}")
    print_epoch_offsets(elements, start)

    tracks = [propagate(el, times) for el in elements]
    run_propagation_checks(elements, tracks)
    print_track_samples(elements, tracks)

    if len(elements) != len(tracks):
        raise ValueError("elements and tracks length mismatch")
    summaries = [orbit_summary(el, pts) for el, pts in zip(elements, tracks)]
    print("Orbit summary:")
    for line in summary_table(summaries):
        print(line)
    check_galileo_period(summaries)

    coastline = load_coastline(IN_DIR / "world_map.txt")
    ground_path = plot_ground_tracks(elements, tracks, coastline)
    speed_path = plot_speed_timeseries(elements, tracks)
    print(f"Saved ground tracks: {ground_path} ({ground_path.stat().st_size} bytes)")
    print(f"Saved speed plot:    {speed_path} ({speed_path.stat().st_size} bytes)")

    ecef_kml = write_orbit_tracks_ecef_kml(elements, tracks)
    anim_kml = write_orbit_animation_kml(elements, tracks)
    report_path = write_orbit_report(
        OUT_DIR / "orbit_report.txt",
        source_note,
        start,
        end,
        elements,
        summaries,
    )
    zip_path = zip_orbit_outputs(
        [ground_path, speed_path, ecef_kml, anim_kml, report_path]
    )
    print(f"Saved ECEF KML:      {ecef_kml} ({ecef_kml.stat().st_size} bytes)")
    print(f"Saved animation KML: {anim_kml} ({anim_kml.stat().st_size} bytes)")
    print(f"Saved report:        {report_path} ({report_path.stat().st_size} bytes)")
    print(f"Saved zip:           {zip_path} ({zip_path.stat().st_size} bytes)")
    with zipfile.ZipFile(zip_path, "r") as zf:
        print(f"Zip members: {zf.namelist()}")
