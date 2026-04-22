"""
Page 5 — Captain Pulse
Tenure distribution · Rides/captain histogram · GMV by decile · Ratings by tenure
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import streamlit as st

from utils.data_loader import load_data, TENURE_ORDER, PLOTLY_COLORS, PLOTLY_TEMPLATE, CHART_GRID, CHART_FONT
from utils.filters import apply_filters
from utils.styles import inject_css, page_header, insight_box, section_title

st.set_page_config(page_title="Captain Pulse · Careem 2025", page_icon="🚗", layout="wide")
inject_css()

df_full = load_data()
df = apply_filters(df_full)
completed = df[df["Is_Completed"]]

page_header("Captain Pulse", "Tenure tiers · productivity deciles · rating distribution")

# ── KPI row ───────────────────────────────────────────────────────────────────
total_captains = df["Captain_ID"].nunique()
avg_rating     = completed["Captain_Rating"].mean() if len(completed) else 0
rides_per_cap  = completed.groupby("Captain_ID")["Booking_ID"].count()
median_rides   = rides_per_cap.median() if len(rides_per_cap) else 0
p90_rides      = rides_per_cap.quantile(0.9) if len(rides_per_cap) else 0
veteran_pct    = (
    (df[df["Captain_Tenure_Tier"].astype(str).str.startswith("3", na=False)]["Captain_ID"].nunique() / total_captains)
    if total_captains else 0
)

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Active Captains",       f"{total_captains:,}")
c2.metric("Avg Captain Rating",    f"{avg_rating:.2f} ★")
c3.metric("Median Rides/Captain",  f"{int(median_rides):,}")
c4.metric("90th %ile Rides/Cap",   f"{int(p90_rides):,}")
c5.metric("Veteran Captains (3+)", f"{veteran_pct:.1%}")

st.markdown("<br>", unsafe_allow_html=True)

# ── Tenure distribution + rides histogram ─────────────────────────────────────
col_ten, col_hist = st.columns([1, 1])

with col_ten:
    section_title("Captain Tenure Tier Distribution")
    tenure_counts = (
        df.drop_duplicates("Captain_ID")
        .groupby("Captain_Tenure_Tier", observed=True)["Captain_ID"]
        .count()
        .reset_index(name="Captains")
    )
    # Map to readable labels
    tenure_label_map = {
        "< 6 months":  "< 6 months",
        "6–12 months": "6–12 months",
        "1–2 years":   "1–2 years",
        "2–3 years":   "2–3 years",
        "3+ years":    "3+ years (Veteran)",
    }
    tenure_counts["Tier"] = tenure_counts["Captain_Tenure_Tier"].astype(str).map(
        lambda x: next((v for k, v in tenure_label_map.items() if k in x), x)
    )

    fig_tenure = px.bar(
        tenure_counts.sort_values("Captains", ascending=True),
        x="Captains", y="Captain_Tenure_Tier", orientation="h",
        color_discrete_sequence=[PLOTLY_COLORS[0]],
        template=PLOTLY_TEMPLATE,
        labels={"Captain_Tenure_Tier": "Tenure Tier"},
    )
    fig_tenure.update_traces(
        marker_color=PLOTLY_COLORS[:len(tenure_counts)],
        text=tenure_counts.sort_values("Captains")["Captains"].apply(lambda v: f"{v:,}"),
        textposition="outside",
        textfont_size=11,
    )
    fig_tenure.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=300,
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(gridcolor=CHART_GRID),
        yaxis=dict(gridcolor=CHART_GRID),
        font=dict(color=CHART_FONT, size=11),
    )
    st.plotly_chart(fig_tenure, use_container_width=True)

with col_hist:
    section_title("Rides per Captain Distribution")
    cap_rides = completed.groupby("Captain_ID")["Booking_ID"].count().reset_index(name="Rides")
    p10 = cap_rides["Rides"].quantile(0.10)
    p50 = cap_rides["Rides"].quantile(0.50)
    p90 = cap_rides["Rides"].quantile(0.90)

    fig_hist = px.histogram(
        cap_rides, x="Rides", nbins=40,
        color_discrete_sequence=[PLOTLY_COLORS[0]],
        template=PLOTLY_TEMPLATE,
        labels={"Rides": "Rides per Captain"},
    )
    for pct, val, color in [(10, p10, "#64748B"), (50, p50, "#38BDF8"), (90, p90, "#F59E0B")]:
        fig_hist.add_vline(
            x=val, line_dash="dash", line_color=color, line_width=1.5,
            annotation_text=f"P{pct}: {int(val)}",
            annotation_font=dict(color=color, size=10),
        )
    fig_hist.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=300,
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(gridcolor=CHART_GRID),
        yaxis=dict(title="Captains", gridcolor=CHART_GRID),
        font=dict(color=CHART_FONT, size=11),
        bargap=0.05,
    )
    st.plotly_chart(fig_hist, use_container_width=True)

# ── GMV by decile + Rating by tenure ─────────────────────────────────────────
col_decile, col_rating = st.columns([1, 1])

with col_decile:
    section_title("GMV Concentration — Captain Deciles")
    cap_gmv = (
        completed.groupby("Captain_ID")["Fare_AED"]
        .sum()
        .reset_index(name="GMV")
        .sort_values("GMV", ascending=False)
    )
    cap_gmv["Decile"] = pd.qcut(
        cap_gmv["GMV"].rank(method="first", ascending=False),
        q=10,
        labels=[f"D{i}" for i in range(1, 11)]
    )
    decile_gmv = (
        cap_gmv.groupby("Decile", observed=True)["GMV"]
        .sum()
        .reset_index()
    )
    decile_gmv["Share"] = decile_gmv["GMV"] / decile_gmv["GMV"].sum()

    fig_decile = px.bar(
        decile_gmv, x="Decile", y="Share",
        color_discrete_sequence=[PLOTLY_COLORS[0]],
        template=PLOTLY_TEMPLATE,
        labels={"Share": "GMV Share", "Decile": "Captain Decile (D1=Top)"},
        text=decile_gmv["Share"].apply(lambda v: f"{v:.1%}"),
    )
    fig_decile.update_traces(
        marker_color=[
            "#00B14F" if i == 0 else "#CBD5E1"
            for i in range(len(decile_gmv))
        ],
        textposition="outside",
        textfont_size=10,
    )
    fig_decile.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=300,
        margin=dict(l=0, r=0, t=10, b=0),
        yaxis=dict(tickformat=".0%", gridcolor=CHART_GRID),
        xaxis=dict(gridcolor=CHART_GRID),
        font=dict(color=CHART_FONT, size=11),
    )
    st.plotly_chart(fig_decile, use_container_width=True)

with col_rating:
    section_title("Avg Captain Rating by Tenure Tier")
    rating_by_tenure = (
        completed.groupby("Captain_Tenure_Tier", observed=True)["Captain_Rating"]
        .mean()
        .reset_index()
        .rename(columns={"Captain_Rating": "Avg Rating"})
        .sort_values("Avg Rating", ascending=True)
    )
    fig_rating = px.bar(
        rating_by_tenure,
        x="Avg Rating", y="Captain_Tenure_Tier",
        orientation="h",
        color="Avg Rating",
        color_continuous_scale=["#EF4444", "#F59E0B", "#00B14F"],
        range_color=[4.0, 5.0],
        template=PLOTLY_TEMPLATE,
        labels={"Captain_Tenure_Tier": "Tenure Tier"},
        text=rating_by_tenure["Avg Rating"].apply(lambda v: f"{v:.2f} ★"),
    )
    fig_rating.update_traces(textposition="outside", textfont_size=11)
    fig_rating.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=300,
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(range=[4, 5], gridcolor=CHART_GRID),
        yaxis=dict(gridcolor=CHART_GRID),
        coloraxis_showscale=False,
        font=dict(color=CHART_FONT, size=11),
    )
    st.plotly_chart(fig_rating, use_container_width=True)

# ── Insight ────────────────────────────────────────────────────────────────────
insight_box(
    '<i class="bi bi-trophy-fill" style="color:#D97706"></i> <strong>Top 10% of captains (D1) generate 23.1% of GMV.</strong> '
    'Median captain completes 108 rides/year; the 90th-percentile captain completes 239. '
    'Veteran captains (3+ years) make up <strong>only 1.3%</strong> of the active pool — '
    'Careem is losing experienced supply faster than it replaces it. '
    'Retention incentives for the 2–3 year cohort (the pipeline to veteran status) would have the highest leverage.'
)
