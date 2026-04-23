"""
Page 8 — Geo Map
City bubble map (GMV × Completion) · Full city leaderboard · Revenue per km by city
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st

from utils.data_loader import get_data, CITY_COORDS, PLOTLY_COLORS, PLOTLY_TEMPLATE, CHART_GRID, CHART_FONT, CHART_FONT_FAMILY, CHART_FONT_FAMILY
from utils.filters import apply_filters
from utils.styles import inject_css, page_header, insight_box, section_title

st.set_page_config(page_title="Geo Map · Careem 2025", page_icon="🗺️", layout="wide")
inject_css()

df_full = get_data()
df = apply_filters(df_full)
completed = df[df["Is_Completed"]]

page_header("Geo Map", "City bubble map · GMV concentration · revenue per km")

# ── Build city-level aggregation ──────────────────────────────────────────────
city_agg = (
    df.groupby("City", observed=True)
    .agg(
        Rides=("Booking_ID", "count"),
        Completed_Rides=("Is_Completed", "sum"),
        GMV=("Fare_AED", lambda x: x[df.loc[x.index, "Is_Completed"]].sum()),
        Avg_Fare=("Fare_AED", lambda x: x[df.loc[x.index, "Is_Completed"]].mean()),
        Avg_Surge=("Surge_Multiplier", lambda x: x[df.loc[x.index, "Is_Completed"]].mean()),
        Avg_VTAT=("Avg_VTAT_mins", lambda x: x[df.loc[x.index, "Is_Completed"]].mean()),
        Avg_Captain_Rating=("Captain_Rating", lambda x: x[df.loc[x.index, "Is_Completed"]].mean()),
        Total_Distance=("Ride_Distance_km", lambda x: x[df.loc[x.index, "Is_Completed"]].sum()),
    )
    .reset_index()
)
city_agg["Completion_Rate"] = city_agg["Completed_Rides"] / city_agg["Rides"]
city_agg["Fare_per_km"]     = city_agg["GMV"] / city_agg["Total_Distance"]
city_agg["GMV_M"]           = city_agg["GMV"] / 1e6

# Add coordinates
city_agg["Lat"] = city_agg["City"].map(lambda c: CITY_COORDS.get(c, {}).get("lat"))
city_agg["Lon"] = city_agg["City"].map(lambda c: CITY_COORDS.get(c, {}).get("lon"))
city_agg["Country"] = city_agg["City"].map(lambda c: CITY_COORDS.get(c, {}).get("country"))

# ── Map ───────────────────────────────────────────────────────────────────────
section_title("Where Does GMV Live? — City Bubble Map")
col_map, col_tbl = st.columns([3, 2])

with col_map:
    if city_agg["Lat"].notna().any():
        fig_map = px.scatter_geo(
            city_agg,
            lat="Lat", lon="Lon",
            size="GMV_M",
            color="Completion_Rate",
            color_continuous_scale=[
                [0.0, "#EF4444"],
                [0.4, "#F59E0B"],
                [0.7, "#38BDF8"],
                [1.0, "#00B14F"],
            ],
            range_color=[0.78, 0.90],
            hover_name="City",
            hover_data={
                "GMV_M": ":.2f",
                "Completion_Rate": ":.1%",
                "Avg_Fare": ":.1f",
                "Avg_VTAT": ":.2f",
                "Lat": False, "Lon": False,
            },
            size_max=45,
            template=PLOTLY_TEMPLATE,
            scope="world",
            center=dict(lat=25.5, lon=42),
            labels={
                "GMV_M": "GMV (AED M)",
                "Completion_Rate": "Completion Rate",
                "Avg_Fare": "Avg Fare (AED)",
                "Avg_VTAT": "Avg VTAT (min)",
            },
        )
        fig_map.update_geos(
            projection_type="natural earth",
            showland=True,         landcolor="#E2E8F0",
            showocean=True,        oceancolor="#DBEAFE",
            showlakes=False,
            showcountries=True,    countrycolor="#CBD5E1",
            showcoastlines=True,   coastlinecolor="#CBD5E1",
            bgcolor="#F8FAFC",
            lataxis_range=[15, 40],
            lonaxis_range=[25, 70],
        )
        fig_map.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            height=460,
            margin=dict(l=0, r=0, t=10, b=0),
            coloraxis_colorbar=dict(
                title=dict(
                    text="Completion",
                    font=dict(family=CHART_FONT_FAMILY, color=CHART_FONT, size=10),
                ),
                tickformat=".0%",
                thickness=10,
                len=0.6,
                tickfont=dict(family=CHART_FONT_FAMILY, color=CHART_FONT, size=10),
            ),
            font=dict(family=CHART_FONT_FAMILY, color=CHART_FONT, size=11),
        )
        st.plotly_chart(fig_map, use_container_width=True)

with col_tbl:
    section_title("City Leaderboard — Full Detail")
    display = city_agg.sort_values("GMV_M", ascending=False).copy()
    display["GMV"]           = display["GMV_M"].apply(lambda v: f"AED {v:.2f}M")
    display["Completion"]    = display["Completion_Rate"].apply(lambda v: f"{v:.1%}")
    display["Rides"]         = display["Rides"].apply(lambda v: f"{v:,}")
    display["Avg Fare"]      = display["Avg_Fare"].apply(lambda v: f"AED {v:.0f}")
    display["Avg Surge"]     = display["Avg_Surge"].apply(lambda v: f"{v:.3f}×")
    display["Avg VTAT"]      = display["Avg_VTAT"].apply(lambda v: f"{v:.2f} min")
    display["Rating ★"]      = display["Avg_Captain_Rating"].apply(lambda v: f"{v:.2f}")
    display["AED/km"]        = display["Fare_per_km"].apply(lambda v: f"{v:.2f}")

    st.dataframe(
        display[["City", "Country", "Rides", "GMV", "Completion", "Avg Fare", "Avg Surge", "Avg VTAT", "Rating ★", "AED/km"]],
        use_container_width=True,
        hide_index=True,
        height=440,
    )

# ── Fare per km bar ────────────────────────────────────────────────────────────
section_title("Revenue Intensity — AED per km by City")
farekm = city_agg.sort_values("Fare_per_km", ascending=True)

fig_farekm = go.Figure(go.Bar(
    x=farekm["Fare_per_km"],
    y=farekm["City"].astype(str),
    orientation="h",
    marker_color=PLOTLY_COLORS[:len(farekm)],
    text=farekm["Fare_per_km"].apply(lambda v: f"AED {v:.2f}/km"),
    textposition="outside",
    textfont=dict(size=12),
))
fig_farekm.update_layout(
    template=PLOTLY_TEMPLATE,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    height=220,
    margin=dict(l=0, r=0, t=10, b=0),
    xaxis=dict(title="AED per km", gridcolor=CHART_GRID),
    yaxis=dict(gridcolor=CHART_GRID),
    font=dict(family=CHART_FONT_FAMILY, color=CHART_FONT, size=12),
)
st.plotly_chart(fig_farekm, use_container_width=True)

# ── Insight ────────────────────────────────────────────────────────────────────
insight_box(
    '<i class="bi bi-globe-americas" style="color:#3B82F6"></i> <strong>Dubai</strong> is the highest-revenue-intensity city (AED/km), driven by Business and Hala EV. '
    '<strong>Cairo</strong> delivers the lowest AED/km but the highest raw ride count — '
    'a volume-vs-margin tradeoff that caps its GMV contribution despite large demand. '
    'The two Saudi cities (Riyadh + Jeddah) have the worst completion rates in the network, '
    'signalling the highest ROI for supply-side interventions.'
)
