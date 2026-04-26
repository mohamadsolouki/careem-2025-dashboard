"""
Page 4 — Pricing Lab (Prescriptive)
What-if sliders: Surge Adjustment · Target Completion · Fare Adjustment
Live-computed simulated GMV + completion recovery estimate
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import streamlit as st

from utils.data_loader import get_data, PLOTLY_COLORS, PLOTLY_TEMPLATE, CHART_GRID, CHART_FONT, CHART_FONT_FAMILY, CHART_FONT_FAMILY
from utils.filters import apply_filters
from utils.styles import inject_css, page_header, insight_box, section_title

st.set_page_config(page_title="Pricing Lab · Careem 2025", page_icon="🔬", layout="wide")
inject_css()

df_full = get_data()
df = apply_filters(df_full)

completed = df[df["Is_Completed"]]
baseline_gmv        = completed["Fare_AED"].sum()
baseline_rides      = len(df)
baseline_comp       = df["Is_Completed"].mean()
baseline_comp_count = df["Is_Completed"].sum()

# ── Slider controls ────────────────────────────────────────────────────────────
st.markdown(
    '<div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:20px 28px;margin-bottom:24px;">',
    unsafe_allow_html=True,
)
st.markdown('<p style="font-size:13px;font-weight:600;color:#64748B;margin:0 0 16px 0;">Adjust the parameters below and see the simulated impact update instantly.</p>', unsafe_allow_html=True)

ctrl_a, ctrl_b, ctrl_c = st.columns(3)

with ctrl_a:
    surge_adj = st.slider(
        "Surge Adjustment ×",
        min_value=0.80, max_value=2.00,
        value=1.00, step=0.05,
        help="Multiply all surge values by this factor. <1 = reduce surge; >1 = increase surge.",
    )
with ctrl_b:
    target_comp = st.slider(
        "Target Completion Rate (%)",
        min_value=80, max_value=95,
        value=int(round(baseline_comp * 100)),
        step=1,
        help="What completion rate are you targeting? Simulates ride recovery.",
    )
with ctrl_c:
    fare_adj = st.slider(
        "Fare Adjustment (%)",
        min_value=-20, max_value=20,
        value=0, step=1,
        help="Percentage change to all fares (e.g. +5 = 5% fare increase).",
    )
st.markdown("</div>", unsafe_allow_html=True)

# ── Simulate ──────────────────────────────────────────────────────────────────
fare_factor   = 1 + fare_adj / 100
sim_gmv       = baseline_gmv * surge_adj * fare_factor

target_rate   = target_comp / 100
avg_fare_base = completed["Fare_AED"].mean() if len(completed) else 60

# Surge effect on completion: calibrated from dataset.
# Real data shows completion drops from 85.1% (surge ≤1.0) to ~81.5% (surge 1.3–1.6),
# implying ~7% drop per 1.0× increase in surge multiplier.
# Fare drag: customers cancel slightly more when fares rise (~25% pass-through).
SURGE_COMPLETION_SENSITIVITY = 0.07
fare_completion_drag = max(0.0, (fare_adj / 100) * 0.25)

surge_penalty   = (surge_adj - 1.0) * SURGE_COMPLETION_SENSITIVITY

# Target slider is integer (step=1). To avoid a rounding-induced non-zero delta
# at the default position, we treat it as a lift above the rounded baseline so
# that slider_default → lift = 0 → sim_comp = baseline_comp exactly.
slider_baseline = int(round(baseline_comp * 100))   # e.g. 84 when baseline is 84.03%
target_lift     = (target_comp - slider_baseline) / 100  # 0 at default, +0.06 at 90%
sim_comp        = float(np.clip(baseline_comp + target_lift - surge_penalty - fare_completion_drag, 0.50, 1.0))

delta_comp      = sim_comp - baseline_comp
recovered_rides = int(baseline_rides * delta_comp)   # negative when sim_comp < baseline_comp
recovered_gmv   = recovered_rides * avg_fare_base * surge_adj * fare_factor
total_sim_gmv   = sim_gmv + recovered_gmv

# ── KPI comparison row ─────────────────────────────────────────────────────────
section_title("Simulated Outcome vs Baseline")
k1, k2, k3, k4, k5 = st.columns(5)

k1.metric(
    "Baseline GMV",
    f"AED {baseline_gmv/1e6:.2f}M",
)
k2.metric(
    "Simulated GMV",
    f"AED {total_sim_gmv/1e6:.2f}M",
    delta=f"{(total_sim_gmv - baseline_gmv)/1e6:+.2f}M AED",
    delta_color="normal",
)
k3.metric(
    "Recovered Rides",
    f"{recovered_rides:,}",
    delta=f"{delta_comp:+.1%} completion shift",
    delta_color="normal",
)
k4.metric(
    "Monthly Recovery Est.",
    f"AED {recovered_gmv/12/1e3:.0f}K/mo",
)
k5.metric(
    "Simulated Completion",
    f"{sim_comp:.1%}",
    delta=f"{sim_comp - baseline_comp:+.1%} vs actual",
    delta_color="normal",
)

st.markdown("<br>", unsafe_allow_html=True)

# ── Two charts: GMV waterfall + Surge-fare scatter ──────────────────────────────
col_wf, col_sc = st.columns([1, 1])

with col_wf:
    section_title("GMV Waterfall — Baseline → Simulated")
    waterfall_vals = [
        baseline_gmv / 1e6,
        (sim_gmv - baseline_gmv) / 1e6,
        recovered_gmv / 1e6,
        total_sim_gmv / 1e6,
    ]
    waterfall_text = [
        f"AED {baseline_gmv/1e6:.2f}M",
        f"AED {(sim_gmv - baseline_gmv)/1e6:+.2f}M",
        f"AED {recovered_gmv/1e6:+.2f}M",
        f"AED {total_sim_gmv/1e6:.2f}M",
    ]
    fig_wf = go.Figure(go.Waterfall(
        name="GMV",
        orientation="v",
        measure=["absolute", "relative", "relative", "total"],
        x=["Baseline GMV", "Surge/Fare Effect", "Ride Recovery", "Simulated GMV"],
        y=waterfall_vals,
        text=waterfall_text,
        textposition="outside",
        connector=dict(line=dict(color="#CBD5E1")),
        decreasing=dict(marker_color="#EF4444"),
        increasing=dict(marker_color="#00B14F"),
        totals=dict(marker_color="#38BDF8"),
        textfont=dict(size=11),
    ))
    fig_wf.update_layout(
        template=PLOTLY_TEMPLATE,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=340,
        margin=dict(l=0, r=0, t=20, b=0),
        yaxis=dict(title="GMV (AED M)", gridcolor=CHART_GRID),
        font=dict(family=CHART_FONT_FAMILY, color=CHART_FONT, size=11),
    )
    st.plotly_chart(fig_wf, use_container_width=True)

with col_sc:
    section_title("Surge × Fare — Actual Rides (Completed)")
    sample = completed.sample(min(5000, len(completed)), random_state=42)
    sim_fare_col  = sample["Fare_AED"] * fare_factor * surge_adj

    fig_sc = go.Figure()
    fig_sc.add_scatter(
        x=sample["Surge_Multiplier"],
        y=sample["Fare_AED"],
        mode="markers",
        name="Actual Rides",
        marker=dict(color="#CBD5E1", size=3, opacity=0.6),
    )
    # Simulated point: avg scenario
    sim_surge_pt = completed["Surge_Multiplier"].mean() * surge_adj
    sim_fare_pt  = avg_fare_base * fare_factor * surge_adj
    fig_sc.add_scatter(
        x=[sim_surge_pt], y=[sim_fare_pt],
        mode="markers",
        name="Simulated Avg",
        marker=dict(color="#F59E0B", size=16, symbol="star"),
    )
    fig_sc.update_layout(
        template=PLOTLY_TEMPLATE,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=340,
        margin=dict(l=0, r=0, t=20, b=0),
        xaxis=dict(title="Surge Multiplier ×", gridcolor=CHART_GRID),
        yaxis=dict(title="Fare (AED)", gridcolor=CHART_GRID),
        legend=dict(font_size=11),
        font=dict(family=CHART_FONT_FAMILY, color=CHART_FONT, size=11),
    )
    st.plotly_chart(fig_sc, use_container_width=True)

# ── Strategic insight ──────────────────────────────────────────────────────────
insight_box(
    '<i class="bi bi-graph-up-arrow" style="color:#00B14F"></i> <strong>Prescriptive finding:</strong> A <strong>3 percentage-point</strong> completion lift '
    '(84.2% → 87.2%) by directing captain incentives to supply-gap windows would recover '
    '~<strong>15,000 rides/month</strong> — approximately <strong>AED 0.9M of incremental monthly GMV</strong> '
    'on the 2025 baseline, worth ~<strong>AED 11M annually</strong>. '
    'This requires no fare increase — only better captain supply allocation during peak and Ramadan windows.'
)
