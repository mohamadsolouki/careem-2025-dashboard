"""
Page 6 — Customer Lens
Loyalty tiers · Payment mix · Spend per tier · Repeat rate
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st

from utils.data_loader import load_data, TIER_ORDER, PLOTLY_COLORS, PLOTLY_TEMPLATE, CHART_GRID, CHART_FONT, CHART_FONT_FAMILY, CHART_FONT_FAMILY
from utils.filters import apply_filters
from utils.styles import inject_css, page_header, insight_box, section_title

st.set_page_config(page_title="Customer Lens · Careem 2025", page_icon="👤", layout="wide")
inject_css()

df_full = load_data()
df = apply_filters(df_full)
completed = df[df["Is_Completed"]]

page_header("Customer Lens", "Loyalty tiers · payment mix · spend & repeat behaviour")

# ── KPIs ─────────────────────────────────────────────────────────────────────
total_cust     = df["Customer_ID"].nunique()
rides_per_cust = completed.groupby("Customer_ID")["Booking_ID"].count()
avg_rides_pc   = rides_per_cust.mean()
median_rides   = rides_per_cust.median()
plus_share     = (df["Customer_Tier"].astype(str).str.contains("Plus", na=False)).mean()
avg_fare_comp  = completed["Fare_AED"].mean() if len(completed) else 0

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Unique Customers",       f"{total_cust:,}")
c2.metric("Avg Rides/Customer",     f"{avg_rides_pc:.1f}")
c3.metric("Median Rides/Customer",  f"{int(median_rides)}")
c4.metric("Careem Plus Share",      f"{plus_share:.1%}")
c5.metric("Avg Fare (Completed)",   f"AED {avg_fare_comp:.2f}")

st.markdown("<br>", unsafe_allow_html=True)

# ── Tier donut + payment mix ──────────────────────────────────────────────────
col_tier, col_pay, col_spend = st.columns([1, 1, 2])

with col_tier:
    section_title("Customer Tier Mix")
    tier_mix = (
        df.groupby("Customer_Tier", observed=True)["Customer_ID"]
        .nunique()
        .reset_index(name="Customers")
        .sort_values("Customers", ascending=False)
    )
    tier_colors = {
        "Regular":     "#CBD5E1",
        "Silver":      "#94A3B8",
        "Gold":        "#F59E0B",
        "Platinum":    "#38BDF8",
        "Careem Plus": "#00B14F",
    }
    fig_tier = px.pie(
        tier_mix, names="Customer_Tier", values="Customers",
        hole=0.55,
        color="Customer_Tier",
        color_discrete_map=tier_colors,
        template=PLOTLY_TEMPLATE,
    )
    fig_tier.update_traces(textinfo="percent+label", textfont_size=10)
    fig_tier.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=300,
        margin=dict(l=0, r=0, t=10, b=0),
        showlegend=False,
        font=dict(family=CHART_FONT_FAMILY, color=CHART_FONT, size=10),
    )
    st.plotly_chart(fig_tier, use_container_width=True)

with col_pay:
    section_title("Payment Method Mix")
    pay_mix = (
        completed["Payment_Method"]
        .value_counts()
        .reset_index()
        .rename(columns={"Payment_Method": "Method", "count": "Rides"})
    )
    fig_pay = px.pie(
        pay_mix, names="Method", values="Rides",
        hole=0.55,
        color_discrete_sequence=PLOTLY_COLORS,
        template=PLOTLY_TEMPLATE,
    )
    fig_pay.update_traces(textinfo="percent+label", textfont_size=10)
    fig_pay.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=300,
        margin=dict(l=0, r=0, t=10, b=0),
        showlegend=False,
        font=dict(family=CHART_FONT_FAMILY, color=CHART_FONT, size=10),
    )
    st.plotly_chart(fig_pay, use_container_width=True)

with col_spend:
    section_title("Avg Fare & Rides per Customer — by Tier")
    tier_spend = (
        completed.groupby("Customer_Tier", observed=True)
        .agg(
            Avg_Fare=("Fare_AED", "mean"),
            Avg_Rides=("Customer_ID", lambda x: len(x) / x.nunique() if x.nunique() else 0),
        )
        .reset_index()
    )

    fig_spend = go.Figure()
    fig_spend.add_bar(
        x=tier_spend["Customer_Tier"].astype(str),
        y=tier_spend["Avg_Fare"],
        name="Avg Fare (AED)",
        marker_color=PLOTLY_COLORS[0],
        yaxis="y1",
        text=tier_spend["Avg_Fare"].apply(lambda v: f"AED {v:.0f}"),
        textposition="outside",
        textfont=dict(size=10),
    )
    fig_spend.add_scatter(
        x=tier_spend["Customer_Tier"].astype(str),
        y=tier_spend["Avg_Rides"],
        name="Avg Rides/Customer",
        mode="lines+markers",
        line=dict(color=PLOTLY_COLORS[1], width=2),
        marker=dict(size=8),
        yaxis="y2",
    )
    fig_spend.update_layout(
        template=PLOTLY_TEMPLATE,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=300,
        margin=dict(l=0, r=0, t=10, b=0),
        yaxis=dict(title="Avg Fare (AED)", gridcolor=CHART_GRID),
        yaxis2=dict(title="Avg Rides/Customer", overlaying="y", side="right", gridcolor=CHART_GRID),
        xaxis=dict(gridcolor=CHART_GRID),
        legend=dict(orientation="h", x=0, y=1.1, font_size=11),
        font=dict(family=CHART_FONT_FAMILY, color=CHART_FONT, size=11),
        bargap=0.35,
    )
    st.plotly_chart(fig_spend, use_container_width=True)

# ── Rides per customer histogram ───────────────────────────────────────────────
section_title("Rides per Customer — Distribution")
rides_dist = completed.groupby("Customer_ID")["Booking_ID"].count().reset_index(name="Rides")
p50 = rides_dist["Rides"].quantile(0.5)
p90 = rides_dist["Rides"].quantile(0.9)

fig_rdist = px.histogram(
    rides_dist, x="Rides", nbins=35,
    color_discrete_sequence=[PLOTLY_COLORS[0]],
    template=PLOTLY_TEMPLATE,
    labels={"Rides": "Rides per Customer"},
)
for pct, val, color in [(50, p50, "#38BDF8"), (90, p90, "#F59E0B")]:
    fig_rdist.add_vline(
        x=val, line_dash="dash", line_color=color, line_width=1.5,
        annotation_text=f"P{pct}: {int(val)}",
        annotation_font=dict(color=color, size=10),
    )
fig_rdist.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    height=220,
    margin=dict(l=0, r=0, t=10, b=0),
    xaxis=dict(gridcolor=CHART_GRID),
    yaxis=dict(title="Customers", gridcolor=CHART_GRID),
    font=dict(family=CHART_FONT_FAMILY, color=CHART_FONT, size=11),
    bargap=0.05,
)
st.plotly_chart(fig_rdist, use_container_width=True)

# ── Insight ────────────────────────────────────────────────────────────────────
insight_box(
    '<i class="bi bi-exclamation-triangle-fill" style="color:#D97706"></i> <strong>Loyalty tiers are not shifting behaviour.</strong> Regular, Silver, Gold, Platinum, and '
    'Careem Plus customers all spend within <strong>3% of each other per ride (AED 59–60)</strong> and '
    'take almost the same number of rides per year (~33). The loyalty programme is not yet '
    'driving meaningful incremental spend or frequency — a material revenue opportunity that '
    'targeted offers and Careem Plus incentives could capture.'
)
