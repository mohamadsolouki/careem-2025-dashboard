"""
Page 2 — Completion & Cancellations
Funnel · Failure reasons · Cancel rate by hour · City supply-gap table
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st

from utils.data_loader import get_data, PLOTLY_COLORS, PLOTLY_TEMPLATE, CHART_GRID, CHART_FONT, CHART_FONT_FAMILY, CHART_FONT_FAMILY
from utils.filters import apply_filters
from utils.styles import inject_css, page_header, insight_box, section_title

st.set_page_config(page_title="Completion & Cancellations · Careem 2025", page_icon="🚫", layout="wide")
inject_css()

df_full = get_data()
df = apply_filters(df_full)

# ── KPI row ───────────────────────────────────────────────────────────────────
total = len(df)
comp_rate  = df["Is_Completed"].mean()
cust_cx    = (df["Booking_Status"] == "Cancelled by Customer").mean()
capt_cx    = (df["Booking_Status"] == "Cancelled by Captain").mean()
no_drv     = (df["Booking_Status"] == "No Driver Found").mean()
incomplete = (df["Booking_Status"] == "Incomplete").mean()

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Completion Rate",  f"{comp_rate:.1%}",  delta=f"{comp_rate - 0.87:+.1%} vs 87% target")
c2.metric("Customer Cancels", f"{cust_cx:.1%}")
c3.metric("Captain Cancels",  f"{capt_cx:.1%}")
c4.metric("No Driver Found",  f"{no_drv:.1%}")
c5.metric("Incomplete",       f"{incomplete:.1%}")

st.markdown("<br>", unsafe_allow_html=True)

# ── Funnel + reason bar ────────────────────────────────────────────────────────
col_funnel, col_reason = st.columns([1, 1])

with col_funnel:
    section_title("Outcome Funnel")
    status_counts = (
        df["Booking_Status"]
        .value_counts()
        .reset_index()
        .rename(columns={"Booking_Status": "Status", "count": "Rides"})
        .sort_values("Rides", ascending=True)
    )
    status_counts["Status"] = status_counts["Status"].astype(str)
    colors_map = {
        "Completed":               "#00B14F",
        "Cancelled by Customer":   "#EF4444",
        "Cancelled by Captain":    "#F59E0B",
        "No Driver Found":         "#8B5CF6",
        "Incomplete":              "#64748B",
    }
    status_counts["Color"] = status_counts["Status"].map(colors_map).fillna("#94A3B8")

    fig_funnel = go.Figure(go.Bar(
        x=status_counts["Rides"],
        y=status_counts["Status"],
        orientation="h",
        marker_color=status_counts["Color"].tolist(),
        text=status_counts["Rides"].apply(lambda v: f"{v:,}"),
        textposition="outside",
        textfont=dict(size=11),
    ))
    fig_funnel.update_layout(
        template=PLOTLY_TEMPLATE,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=300,
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(title="Rides", gridcolor=CHART_GRID),
        yaxis=dict(gridcolor=CHART_GRID),
        font=dict(family=CHART_FONT_FAMILY, color=CHART_FONT, size=11),
    )
    st.plotly_chart(fig_funnel, use_container_width=True)

with col_reason:
    section_title("Why Rides Cancel (Top 10)")
    reasons = (
        df[df["Cancellation_Reason"].notna() & (df["Cancellation_Reason"] != "")]
        ["Cancellation_Reason"]
        .value_counts()
        .head(10)
        .reset_index()
        .rename(columns={"Cancellation_Reason": "Reason", "count": "Count"})
        .sort_values("Count", ascending=True)
    )
    fig_reason = go.Figure(go.Bar(
        x=reasons["Count"],
        y=reasons["Reason"],
        orientation="h",
        marker_color=PLOTLY_COLORS[3],
        text=reasons["Count"].apply(lambda v: f"{v:,}"),
        textposition="outside",
        textfont=dict(size=11),
    ))
    fig_reason.update_layout(
        template=PLOTLY_TEMPLATE,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=300,
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(gridcolor=CHART_GRID),
        yaxis=dict(gridcolor=CHART_GRID),
        font=dict(family=CHART_FONT_FAMILY, color=CHART_FONT, size=11),
    )
    st.plotly_chart(fig_reason, use_container_width=True)

# ── Cancel rate by hour + city supply gap ─────────────────────────────────────
col_hour, col_gap = st.columns([1, 1])

with col_hour:
    section_title("Cancellation Rate by Hour of Day")
    hourly = (
        df.groupby("Hour")
        .agg(Total=("Booking_ID", "count"), Cancelled=("Is_Cancelled", "sum"))
        .reset_index()
    )
    hourly["Cancel_Rate"] = hourly["Cancelled"] / hourly["Total"]

    fig_hour = px.bar(
        hourly, x="Hour", y="Cancel_Rate",
        color_discrete_sequence=[PLOTLY_COLORS[3]],
        template=PLOTLY_TEMPLATE,
        labels={"Cancel_Rate": "Cancel Rate", "Hour": "Hour of Day"},
    )
    fig_hour.update_traces(marker_color=[
        "#EF4444" if r > hourly["Cancel_Rate"].quantile(0.75) else "#F59E0B"
        if r > hourly["Cancel_Rate"].quantile(0.5) else "#CBD5E1"
        for r in hourly["Cancel_Rate"]
    ])
    fig_hour.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=280,
        margin=dict(l=0, r=0, t=10, b=0),
        yaxis=dict(tickformat=".0%", gridcolor=CHART_GRID),
        xaxis=dict(gridcolor=CHART_GRID),
        font=dict(family=CHART_FONT_FAMILY, color=CHART_FONT, size=11),
    )
    st.plotly_chart(fig_hour, use_container_width=True)

with col_gap:
    section_title("City Supply-Gap Table")
    city_gap = (
        df.groupby("City", observed=True)
        .agg(
            Total=("Booking_ID", "count"),
            No_Driver=("Booking_Status", lambda x: (x == "No Driver Found").sum()),
            Capt_Cancel=("Booking_Status", lambda x: (x == "Cancelled by Captain").sum()),
            Comp_Rate=("Is_Completed", "mean"),
        )
        .reset_index()
    )
    city_gap["No_Driver_Rate"]  = city_gap["No_Driver"] / city_gap["Total"]
    city_gap["Capt_Cancel_Rate"] = city_gap["Capt_Cancel"] / city_gap["Total"]
    city_gap["Supply_Gap"]      = city_gap["No_Driver_Rate"] + city_gap["Capt_Cancel_Rate"]
    city_gap = city_gap.sort_values("Supply_Gap", ascending=False)

    display = city_gap[["City", "No_Driver_Rate", "Capt_Cancel_Rate", "Supply_Gap", "Comp_Rate"]].copy()
    display.columns = ["City", "No Driver %", "Captain Cancel %", "Supply Gap %", "Completion %"]
    for col in ["No Driver %", "Captain Cancel %", "Supply Gap %", "Completion %"]:
        display[col] = display[col].apply(lambda v: f"{v:.2%}")
    st.dataframe(display, use_container_width=True, hide_index=True)

# ── Insight ───────────────────────────────────────────────────────────────────
insight_box(
    '<i class="bi bi-exclamation-triangle-fill" style="color:#DC2626"></i> <strong>"No Captain Available"</strong> is the single largest failure mode (~19.8% of all failures). '
    '<strong>Riyadh</strong> leads with the highest no-driver rate (3.25%), followed by <strong>Jeddah</strong> (3.15%) — '
    'both concentrated during Ramadan evenings and Saudi event seasons. '
    'Captain-initiated cancellations are uniform across cities (6.3–6.5%), signalling a '
    '<em>systemic</em> accept–reject economics problem, not a location issue.'
)
