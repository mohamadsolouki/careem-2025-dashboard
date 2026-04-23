"""
Cached data loader for careem_rides_2025.csv.
Adds all derived columns matching the Power Query logic.
"""

from __future__ import annotations
import pathlib
import pandas as pd
import streamlit as st

# Absolute path to the CSV relative to this file
_CSV = pathlib.Path(__file__).parent.parent / "dataset" / "careem_rides_2025.csv"

# City geo coordinates (from planning doc)
CITY_COORDS = {
    "Dubai":     {"lat": 25.2048, "lon": 55.2708, "country": "UAE"},
    "Abu Dhabi": {"lat": 24.4539, "lon": 54.3773, "country": "UAE"},
    "Riyadh":    {"lat": 24.7136, "lon": 46.6753, "country": "KSA"},
    "Jeddah":    {"lat": 21.4858, "lon": 39.1925, "country": "KSA"},
    "Cairo":     {"lat": 30.0444, "lon": 31.2357, "country": "Egypt"},
}

PRODUCT_ORDER = [
    "Careem Go", "Careem Go+", "Careem Business", "Careem MAX",
    "Hala Taxi", "Hala EV", "Careem eBike", "Careem Bike",
]

TIER_ORDER = ["Regular", "Silver", "Gold", "Platinum", "Careem Plus"]

TENURE_ORDER = ["< 6 months", "6–12 months", "1–2 years", "2–3 years", "3+ years"]

# Re-exported so pages only need to import from data_loader
from utils.styles import PLOTLY_COLORS, PLOTLY_TEMPLATE, CHART_GRID, CHART_FONT, CHART_FONT_FAMILY  # noqa: E402


@st.cache_data(show_spinner="Loading dataset…")
def load_data(_mtime: float = 0.0) -> pd.DataFrame:
    """Load and enrich the dataset. Cache busts automatically when the CSV is modified."""
    df = pd.read_csv(
        _CSV,
        parse_dates=["Date"],
        dtype={
            "Booking_ID": "string",
            "City": "category",
            "Product": "category",
            "Booking_Status": "category",
            "Cancellation_Reason": "string",
            "Customer_ID": "string",
            "Captain_ID": "string",
            "Captain_Tenure_Tier": "category",
            "Customer_Tier": "category",
            "Trip_Purpose": "category",
            "Payment_Method": "category",
            "Day_of_Week": "category",
            "Month": "category",
        },
        low_memory=False,
    )

    # ── Derived boolean columns ──────────────────────────────────────────
    df["Is_Completed"] = df["Booking_Status"] == "Completed"
    df["Is_Cancelled"] = df["Booking_Status"].str.startswith("Cancelled", na=False)

    # Convert Yes/No/True/False/1/0 flag columns to proper bool
    _TRUTHY  = {"yes", "true", "1"}
    _FALSY   = {"no", "false", "0"}
    for flag_col in ["Is_Peak_Hour", "Is_Weekend", "Is_Ramadan", "Is_Airport_Ride"]:
        raw = df[flag_col].astype(str).str.strip().str.lower()
        df[flag_col] = raw.map(
            lambda v: True if v in _TRUTHY else (False if v in _FALSY else False)
        ).astype(bool)

    # ── Surge bucket ─────────────────────────────────────────────────────
    def _surge_bucket(s):
        if pd.isna(s):
            return None
        if s <= 1.0:
            return "1.0× (No surge)"
        if s <= 1.3:
            return "1.0–1.3× (Light)"
        if s <= 1.7:
            return "1.3–1.7× (Moderate)"
        if s <= 2.2:
            return "1.7–2.2× (High)"
        return "2.2×+ (Extreme)"

    df["Surge_Bucket"] = df["Surge_Multiplier"].apply(_surge_bucket).astype("category")

    # ── Distance bucket ──────────────────────────────────────────────────
    bins   = [0, 3, 7, 15, 25, float("inf")]
    labels = ["0–3 km (Short)", "3–7 km (Medium)", "7–15 km (Long)",
              "15–25 km (Airport)", "25+ km (Intercity)"]
    df["Distance_Bucket"] = pd.cut(
        df["Ride_Distance_km"], bins=bins, labels=labels, right=False
    )

    # ── VTAT bucket ──────────────────────────────────────────────────────
    vbins   = [0, 3, 5, 8, 12, float("inf")]
    vlabels = ["<3 min (Excellent)", "3–5 min (Good)", "5–8 min (Acceptable)",
               "8–12 min (Slow)", "12+ min (Poor)"]
    df["VTAT_Bucket"] = pd.cut(
        df["Avg_VTAT_mins"], bins=vbins, labels=vlabels, right=False
    )

    # ── YearMonth for time-series ────────────────────────────────────────
    df["YearMonth"]     = df["Date"].dt.to_period("M").astype(str)
    df["MonthNum"]      = df["Date"].dt.month
    df["WeekNumber"]    = df["Date"].dt.isocalendar().week.astype(int)

    # ── Day-of-week number (for sorting Mon=0..Sun=6) ────────────────────
    df["DayOfWeekNum"]  = df["Date"].dt.dayofweek

    # ── Geo lat/lon + Country (derived — Country removed from CSV) ───────────
    df["Latitude"]  = df["City"].map(lambda c: CITY_COORDS.get(c, {}).get("lat"))
    df["Longitude"] = df["City"].map(lambda c: CITY_COORDS.get(c, {}).get("lon"))
    df["Country"]   = df["City"].map(lambda c: CITY_COORDS.get(c, {}).get("country"))

    return df


def get_data() -> pd.DataFrame:
    """Thin wrapper that auto-passes the CSV mtime so the cache busts on any file change."""
    mtime = _CSV.stat().st_mtime
    return load_data(mtime)


def gmv(df: pd.DataFrame) -> float:
    return df.loc[df["Is_Completed"], "Fare_AED"].sum()


def completion_rate(df: pd.DataFrame) -> float:
    total = len(df)
    return df["Is_Completed"].sum() / total if total else 0.0


def avg_fare(df: pd.DataFrame) -> float:
    completed = df.loc[df["Is_Completed"], "Fare_AED"]
    return completed.mean() if len(completed) else 0.0


def avg_surge(df: pd.DataFrame) -> float:
    completed = df.loc[df["Is_Completed"], "Surge_Multiplier"]
    return completed.mean() if len(completed) else 1.0


def avg_vtat(df: pd.DataFrame) -> float:
    completed = df.loc[df["Is_Completed"], "Avg_VTAT_mins"]
    return completed.mean() if len(completed) else 0.0
