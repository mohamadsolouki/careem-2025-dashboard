"""
Page 3 — Demand & Surge
Hour×Day heatmap · Ramadan comparison · Surge distribution · Peak vs Off-peak KPIs
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import streamlit as st

from utils.data_loader import get_data, PLOTLY_COLORS, PLOTLY_TEMPLATE, CHART_GRID, CHART_FONT, CHART_FONT_FAMILY, CHART_FONT_FAMILY
from utils.filters import apply_filters
from utils.styles import inject_css, page_header, insight_box, section_title

st.set_page_config(page_title="Demand & Surge · Careem 2025", page_icon="⚡", layout="wide")
inject_css()

df_full = get_data()
df = apply_filters(df_full)

page_header("Demand & Surge", "Hour × day heatmap · Ramadan overlay · surge distribution")

# ── Peak vs Off-peak KPIs ─────────────────────────────────────────────────────
peak    = df[df["Is_Peak_Hour"] & df["Is_Completed"]]
offpeak = df[~df["Is_Peak_Hour"] & df["Is_Completed"]]
ramadan = df[df["Is_Ramadan"] & df["Is_Completed"]]

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Peak Hour Rides",      f"{df['Is_Peak_Hour'].sum():,}")
c2.metric("Peak Avg Surge",       f"{peak['Surge_Multiplier'].mean():.3f}×" if len(peak) else "—",
           delta=f"vs {offpeak['Surge_Multiplier'].mean():.3f}× off-peak" if len(offpeak) else "")
c3.metric("Peak Avg VTAT",        f"{peak['Avg_VTAT_mins'].mean():.2f} min" if len(peak) else "—")
c4.metric("Ramadan Rides",        f"{df['Is_Ramadan'].sum():,}")
c5.metric("Ramadan Avg Surge",    f"{ramadan['Surge_Multiplier'].mean():.3f}×" if len(ramadan) else "—")

st.markdown("<br>", unsafe_allow_html=True)

# ── Heatmap + Surge distribution ──────────────────────────────────────────────
col_heat, col_surge = st.columns([3, 2])

with col_heat:
    section_title("Demand Heatmap — Rides by Hour × Day of Week")
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    heat_data = (
        df.groupby(["Day_of_Week", "Hour"], observed=True)["Booking_ID"]
        .count()
        .reset_index(name="Rides")
    )
    heat_pivot = heat_data.pivot(index="Day_of_Week", columns="Hour", values="Rides").fillna(0)
    # Reorder rows
    heat_pivot = heat_pivot.reindex([d for d in day_order if d in heat_pivot.index])

    fig_heat = go.Figure(go.Heatmap(
        z=heat_pivot.values,
        x=heat_pivot.columns.tolist(),
        y=heat_pivot.index.tolist(),
        colorscale=[
            [0.0,  "#F0FDF4"],
            [0.25, "#BBF7D0"],
            [0.5,  "#4ADE80"],
            [0.75, "#00B14F"],
            [1.0,  "#166534"],
        ],
        hovertemplate="Hour: %{x}<br>Day: %{y}<br>Rides: %{z:,}<extra></extra>",
        showscale=True,
        colorbar=dict(
            thickness=10, len=0.8,
            tickfont=dict(family=CHART_FONT_FAMILY, color=CHART_FONT, size=10),
            title=dict(text="Rides", font=dict(family=CHART_FONT_FAMILY, color=CHART_FONT, size=10)),
        ),
    ))
    fig_heat.update_layout(
        template=PLOTLY_TEMPLATE,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=320,
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(title="Hour of Day", tickmode="linear", dtick=2, gridcolor=CHART_GRID),
        yaxis=dict(title="", gridcolor=CHART_GRID),
        font=dict(family=CHART_FONT_FAMILY, color=CHART_FONT, size=11),
    )
    st.plotly_chart(fig_heat, use_container_width=True)

with col_surge:
    section_title("Surge Multiplier Distribution")
    surge_data = df[df["Is_Completed"]]["Surge_Bucket"].value_counts().reset_index()
    surge_data.columns = ["Bucket", "Count"]
    bucket_order = ["1.0× (No surge)", "1.0–1.3× (Light)", "1.3–1.7× (Moderate)", "1.7–2.2× (High)", "2.2×+ (Extreme)"]
    surge_data["Sort"] = surge_data["Bucket"].map(lambda b: bucket_order.index(b) if b in bucket_order else 99)
    surge_data = surge_data.sort_values("Sort")

    fig_surge = px.bar(
        surge_data, x="Count", y="Bucket", orientation="h",
        color="Bucket",
        color_discrete_sequence=["#00B14F", "#38BDF8", "#F59E0B", "#FB923C", "#EF4444"],
        template=PLOTLY_TEMPLATE,
    )
    fig_surge.update_traces(texttemplate="%{x:,}", textposition="outside", textfont_size=10)
    fig_surge.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=320,
        margin=dict(l=0, r=0, t=10, b=0),
        showlegend=False,
        xaxis=dict(gridcolor=CHART_GRID),
        yaxis=dict(gridcolor=CHART_GRID, categoryorder="array", categoryarray=list(reversed(bucket_order))),
        font=dict(family=CHART_FONT_FAMILY, color=CHART_FONT, size=11),
    )
    st.plotly_chart(fig_surge, use_container_width=True)

# ── Ramadan comparison bar ─────────────────────────────────────────────────────
section_title("Ramadan vs Non-Ramadan — Key Metrics Comparison")
metrics_compare = []
for is_ram, label in [(True, "Ramadan"), (False, "Non-Ramadan")]:
    subset = df[df["Is_Ramadan"] == is_ram]
    comp   = subset[subset["Is_Completed"]]
    metrics_compare.append({
        "Period":     label,
        "Avg Surge":  comp["Surge_Multiplier"].mean() if len(comp) else 0,
        "Avg VTAT":   comp["Avg_VTAT_mins"].mean()    if len(comp) else 0,
        "Completion": subset["Is_Completed"].mean()   if len(subset) else 0,
        "Avg Fare":   comp["Fare_AED"].mean()         if len(comp) else 0,
    })
cmp_df = pd.DataFrame(metrics_compare)

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
for col, metric, fmt, label in [
    (col_m1, "Avg Surge",  ".3f", "Avg Surge ×"),
    (col_m2, "Avg VTAT",   ".2f", "Avg VTAT (min)"),
    (col_m3, "Completion", ".1%", "Completion Rate"),
    (col_m4, "Avg Fare",   ".2f", "Avg Fare (AED)"),
]:
    ram_val = cmp_df.loc[cmp_df["Period"] == "Ramadan", metric].values[0]
    non_val = cmp_df.loc[cmp_df["Period"] == "Non-Ramadan", metric].values[0]
    delta   = ram_val - non_val

    fig_cmp = go.Figure(go.Bar(
        x=cmp_df["Period"], y=cmp_df[metric],
        marker_color=["#F59E0B", "#CBD5E1"],
        text=[f"{v:{fmt}}" for v in cmp_df[metric]],
        textposition="outside",
        textfont=dict(size=12),
    ))
    fig_cmp.update_layout(
        template=PLOTLY_TEMPLATE,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title=dict(text=label, font=dict(size=12, color="#94A3B8"), x=0),
        height=200,
        margin=dict(l=0, r=0, t=30, b=0),
        showlegend=False,
        yaxis=dict(gridcolor=CHART_GRID, tickformat=fmt if "%" in fmt else None),
        xaxis=dict(gridcolor=CHART_GRID),
        font=dict(family=CHART_FONT_FAMILY, color=CHART_FONT, size=11),
    )
    col.plotly_chart(fig_cmp, use_container_width=True)

# ── Insight ────────────────────────────────────────────────────────────────────
insight_box(
    '<i class="bi bi-moon-stars-fill" style="color:#3B82F6"></i> <strong>Ramadan 2025 (Mar 1–30)</strong>: surge rises to <strong>1.24×</strong> and '
    'rider wait climbs to <strong>7.24 min</strong> (vs 5.48 min off-peak). '
    'The 17:00–18:00 pre-Iftar window is the sharpest supply stress — captain incentives '
    'during this window in Riyadh and Jeddah would have the highest ROI. '
    'Peak-hour rides carry a <strong>1.289×</strong> surge vs <strong>1.050×</strong> off-peak.'
)
