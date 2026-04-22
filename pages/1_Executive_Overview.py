"""
Page 1 — Executive Overview
Top-line KPIs · Monthly trend · Product & City mix · City leaderboard
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st

from utils.data_loader import load_data, CITY_COORDS, PLOTLY_COLORS, PLOTLY_TEMPLATE, CHART_GRID, CHART_FONT
from utils.filters import apply_filters
from utils.styles import inject_css, page_header, insight_box, section_title

st.set_page_config(page_title="Executive Overview · Careem 2025", page_icon="📊", layout="wide")
inject_css()

df_full = load_data()
df = apply_filters(df_full)

page_header(
    "Executive Overview",
    "2025 top-line KPIs · monthly trend · product & city mix",
)

# ── KPI row ───────────────────────────────────────────────────────────────────
completed = df[df["Is_Completed"]]
total_rides   = len(df)
gmv_val       = completed["Fare_AED"].sum()
comp_rate     = df["Is_Completed"].mean()
avg_fare_val  = completed["Fare_AED"].mean() if len(completed) else 0
avg_surge_val = completed["Surge_Multiplier"].mean() if len(completed) else 0
cust_rating   = completed["Customer_Rating"].mean() if len(completed) else 0

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Total Rides",      f"{total_rides:,}")
c2.metric("GMV (AED)",        f"{gmv_val/1e6:.2f}M")
c3.metric("Completion Rate",  f"{comp_rate:.1%}", delta=f"{comp_rate - 0.85:+.1%} vs 85% target")
c4.metric("Avg Fare",         f"AED {avg_fare_val:.2f}")
c5.metric("Avg Surge",        f"{avg_surge_val:.3f}×")
c6.metric("Customer Rating",  f"{cust_rating:.2f} ★")

st.markdown("<br>", unsafe_allow_html=True)

# ── Monthly trend ────────────────────────────────────────────────────────────
section_title("Monthly Trend — GMV vs Rides")
monthly = (
    df.groupby("YearMonth")
    .agg(
        GMV=("Fare_AED", lambda x: x[df.loc[x.index, "Is_Completed"]].sum()),
        Rides=("Booking_ID", "count"),
    )
    .reset_index()
    .sort_values("YearMonth")
)
monthly["GMV_M"] = monthly["GMV"] / 1e6

fig_trend = go.Figure()
fig_trend.add_bar(
    x=monthly["YearMonth"], y=monthly["GMV_M"],
    name="GMV (AED M)", marker_color=PLOTLY_COLORS[0],
    yaxis="y1",
)
fig_trend.add_scatter(
    x=monthly["YearMonth"], y=monthly["Rides"],
    name="Total Rides", mode="lines+markers",
    line=dict(color=PLOTLY_COLORS[1], width=2),
    marker=dict(size=5),
    yaxis="y2",
)
fig_trend.update_layout(
    template=PLOTLY_TEMPLATE,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    height=300,
    margin=dict(l=0, r=0, t=10, b=0),
    legend=dict(orientation="h", x=0, y=1.12, font_size=11),
    yaxis=dict(title="GMV (AED M)", gridcolor=CHART_GRID),
    yaxis2=dict(title="Rides", overlaying="y", side="right", gridcolor=CHART_GRID),
    xaxis=dict(gridcolor=CHART_GRID),
    font=dict(color=CHART_FONT, size=11),
    bargap=0.25,
)
st.plotly_chart(fig_trend, use_container_width=True)

# ── Donuts + leaderboard ──────────────────────────────────────────────────────
col_prod, col_city, col_tbl = st.columns([1, 1, 2])

with col_prod:
    section_title("Product Mix (Rides)")
    prod_mix = (
        df[df["Is_Completed"]]
        .groupby("Product", observed=True)["Booking_ID"]
        .count()
        .reset_index(name="Rides")
        .sort_values("Rides", ascending=False)
    )
    fig_prod = px.pie(
        prod_mix, names="Product", values="Rides",
        hole=0.55,
        color_discrete_sequence=PLOTLY_COLORS,
        template=PLOTLY_TEMPLATE,
    )
    fig_prod.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=280,
        margin=dict(l=0, r=0, t=10, b=0),
        showlegend=True,
        legend=dict(font_size=10, x=0, y=-0.15, orientation="h"),
        font=dict(color=CHART_FONT, size=10),
    )
    fig_prod.update_traces(textinfo="percent", textfont_size=10)
    st.plotly_chart(fig_prod, use_container_width=True)

with col_city:
    section_title("City Mix (GMV)")
    city_mix = (
        df[df["Is_Completed"]]
        .groupby("City", observed=True)["Fare_AED"]
        .sum()
        .reset_index(name="GMV")
        .sort_values("GMV", ascending=False)
    )
    fig_city = px.pie(
        city_mix, names="City", values="GMV",
        hole=0.55,
        color_discrete_sequence=PLOTLY_COLORS,
        template=PLOTLY_TEMPLATE,
    )
    fig_city.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=280,
        margin=dict(l=0, r=0, t=10, b=0),
        showlegend=True,
        legend=dict(font_size=10, x=0, y=-0.15, orientation="h"),
        font=dict(color=CHART_FONT, size=10),
    )
    fig_city.update_traces(textinfo="percent", textfont_size=10)
    st.plotly_chart(fig_city, use_container_width=True)

with col_tbl:
    section_title("City Leaderboard")
    city_tbl = (
        df.groupby("City", observed=True)
        .agg(
            Rides=("Booking_ID", "count"),
            GMV=("Fare_AED", lambda x: x[df.loc[x.index, "Is_Completed"]].sum()),
            Completion=("Is_Completed", "mean"),
            Avg_Surge=("Surge_Multiplier", lambda x: x[df.loc[x.index, "Is_Completed"]].mean()),
            Avg_Rating=("Customer_Rating", lambda x: x[df.loc[x.index, "Is_Completed"]].mean()),
        )
        .reset_index()
        .sort_values("GMV", ascending=False)
    )
    city_tbl["GMV_M"]      = city_tbl["GMV"].apply(lambda v: f"AED {v/1e6:.2f}M")
    city_tbl["Completion"] = city_tbl["Completion"].apply(lambda v: f"{v:.1%}")
    city_tbl["Avg_Surge"]  = city_tbl["Avg_Surge"].apply(lambda v: f"{v:.3f}×")
    city_tbl["Avg_Rating"] = city_tbl["Avg_Rating"].apply(lambda v: f"{v:.2f} ★")
    city_tbl["Rides"]      = city_tbl["Rides"].apply(lambda v: f"{v:,}")
    display_tbl = city_tbl[["City", "Rides", "GMV_M", "Completion", "Avg_Surge", "Avg_Rating"]]
    display_tbl.columns = ["City", "Rides", "GMV", "Completion", "Avg Surge", "Avg Rating"]
    st.dataframe(display_tbl, use_container_width=True, hide_index=True)

# ── Insight box ───────────────────────────────────────────────────────────────
insight_box(
    '<i class="bi bi-geo-alt-fill" style="color:#3B82F6"></i> <strong>Dubai</strong> leads GMV (34% of total) while <strong>Cairo</strong> delivers '
    'the highest volume of Go rides at the lowest fare per km — a high-volume, low-margin corridor. '
    '<strong>Careem Business</strong> generates the highest avg fare (AED 112) but has the '
    'lowest completion rate at 82.5%.'
)
