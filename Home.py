"""
Careem 2025 — Supply–Demand Intelligence Cockpit
Home / Navigation page
"""

import base64
from pathlib import Path

import streamlit as st

from utils.data_loader import load_data, gmv, completion_rate, avg_fare
from utils.styles import inject_css, insight_box

st.set_page_config(
    page_title="Careem 2025 · Intelligence Cockpit",
    page_icon="🟢",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()

# ── Load data (cached) ───────────────────────────────────────────────────────
df = load_data()

# ── Sidebar logo only on Home ────────────────────────────────────────────────
logo_path = Path(__file__).parent / "assets" / "careem-logo.png"
with st.sidebar:
    if logo_path.exists():
        logo_data = base64.b64encode(logo_path.read_bytes()).decode()
        st.markdown(
            f'<img src="data:image/png;base64,{logo_data}" style="width:130px;margin-bottom:8px;">',
            unsafe_allow_html=True,
        )
    st.markdown(
        '<p style="font-size:10px;color:#64748B;margin-top:-4px;">MIT622 · 2025 · Group 1</p>',
        unsafe_allow_html=True,
    )
    st.markdown('<hr style="border-color:#E2E8F0;margin:8px 0 12px 0;">', unsafe_allow_html=True)
    st.markdown(
        '<p style="font-size:11px;color:#64748B;line-height:1.9;">'
        '<i class="bi bi-database" style="color:#00B14F;"></i> 500,000 ride records<br>'
        '<i class="bi bi-buildings" style="color:#00B14F;"></i> 5 MENAP cities<br>'
        '<i class="bi bi-calendar3" style="color:#00B14F;"></i> Jan – Dec 2025<br>'
        '<i class="bi bi-currency-exchange" style="color:#00B14F;"></i> AED-normalized fares</p>',
        unsafe_allow_html=True,
    )
    st.markdown('<hr style="border-color:#E2E8F0;margin:12px 0;">', unsafe_allow_html=True)
    st.markdown(
        '<p style="font-size:10px;color:#475569;">Mohammadsadegh Solouki<br>'
        'Artin Fateh Basharzad<br>'
        'Fatema Alblooshi</p>',
        unsafe_allow_html=True,
    )

# ── Hero section ─────────────────────────────────────────────────────────────
col_logo, col_title = st.columns([1, 5])
with col_logo:
    if logo_path.exists():
        st.image(str(logo_path), width=110)

with col_title:
    st.markdown(
        """
        <div style="padding-top:6px;">
            <h1 style="font-size:32px;font-weight:800;color:#0F172A;margin:0;letter-spacing:-0.5px;">
                Supply–Demand Intelligence Cockpit
            </h1>
            <p style="font-size:14px;color:#64748B;margin:6px 0 0 0;">
                MIT622 Data Analytics for Managers &nbsp;·&nbsp;
                Group Case Study &nbsp;·&nbsp;
                Dr. Zaher Al-Sai &nbsp;·&nbsp;
                24 April 2026
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<hr style="border-color:#E2E8F0;margin:16px 0 24px 0;">', unsafe_allow_html=True)

# ── KPI strip ────────────────────────────────────────────────────────────────
total    = len(df)
g        = gmv(df)
cr       = completion_rate(df)
af       = avg_fare(df)
uniq_cust = df["Customer_ID"].nunique()

k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.metric("Total Rides", f"{total:,}")
with k2:
    st.metric("Gross Bookings (GMV)", f"AED {g/1e6:.2f}M")
with k3:
    cr_color = "normal" if cr >= 0.85 else ("off" if cr >= 0.80 else "inverse")
    st.metric("Completion Rate", f"{cr:.1%}", delta=f"Target 87%+", delta_color="off")
with k4:
    st.metric("Avg Fare", f"AED {af:.2f}")
with k5:
    st.metric("Unique Customers", f"{uniq_cust:,}")

st.markdown("<br>", unsafe_allow_html=True)

# ── Insight callout ───────────────────────────────────────────────────────────
insight_box(
    '<i class="bi bi-bullseye" style="color:#D97706;"></i> <strong>Business Goal:</strong> Lift completion from <strong>84.2% → 87%+</strong> by directing '
    'captain incentives to supply-gap windows. A 3pp improvement recovers ~15,000 rides/month — '
    'approximately <strong>AED 0.9M incremental monthly GMV</strong>.'
)

# ── Navigation tiles ──────────────────────────────────────────────────────────
st.markdown(
    '<div class="section-title" style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#94A3B8;padding:12px 0 8px 0;border-bottom:1px solid #E2E8F0;margin-bottom:20px;"><i class="bi bi-grid" style="color:#00B14F;margin-right:6px;"></i>Dashboard Pages</div>',
    unsafe_allow_html=True,
)

pages = [
    ("bi-graph-up-arrow",   "1 · Executive Overview",       "Top-line KPIs, monthly trend, city & product mix",           "pages/1_Executive_Overview"),
    ("bi-funnel",            "2 · Completion & Cancellations","Funnel, failure reasons, supply-gap per city",               "pages/2_Completion_Cancellations"),
    ("bi-lightning-charge",  "3 · Demand & Surge",            "Hour × day heatmap, Ramadan overlay, surge distribution",    "pages/3_Demand_Surge"),
    ("bi-sliders",           "4 · Pricing Lab",               "What-if surge, fare & completion simulators",                "pages/4_Pricing_Lab"),
    ("bi-steering2",         "5 · Captain Pulse",             "Tenure tiers, productivity deciles, rating distribution",    "pages/5_Captain_Pulse"),
    ("bi-person-heart",      "6 · Customer Lens",             "Loyalty tiers, payment mix, spend per tier",                 "pages/6_Customer_Lens"),
    ("bi-star-half",         "7 · Quality & Ratings",         "ETA accuracy, VTAT buckets, captain & customer ratings",     "pages/7_Quality_Ratings"),
    ("bi-map",               "8 · Geo Map",                  "City bubble map: GMV × completion, full leaderboard",        "pages/8_Geo_Map"),
]

row1 = st.columns(4)
row2 = st.columns(4)
rows = [row1, row2]

for i, (icon, title, desc, _) in enumerate(pages):
    row_idx  = i // 4
    col_idx  = i % 4
    with rows[row_idx][col_idx]:
        st.markdown(
            f"""
            <div class="nav-tile">
                <span class="nav-icon"><i class="bi {icon}"></i></span>
                <h3>{title}</h3>
                <p>{desc}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("<br>", unsafe_allow_html=True)

# ── Data coverage footer ──────────────────────────────────────────────────────
st.markdown(
    f"""
    <div class="footer-strip">
        <div><div class="fs-label"><i class="bi bi-calendar3"></i> Date Coverage</div><div class="fs-value">Jan 1 – Dec 31, 2025</div></div>
        <div><div class="fs-label"><i class="bi bi-buildings"></i> Cities</div><div class="fs-value">Dubai · Abu Dhabi · Riyadh · Jeddah · Cairo</div></div>
        <div><div class="fs-label"><i class="bi bi-car-front"></i> Products</div><div class="fs-value">Go · Go+ · Business · MAX · Hala · Hala EV · eBike · Bike</div></div>
        <div><div class="fs-label"><i class="bi bi-database"></i> Rows</div><div class="fs-value">{total:,} rides</div></div>
        <div><div class="fs-label"><i class="bi bi-currency-exchange"></i> Currency</div><div class="fs-value">AED-normalized (1 SAR ≈ 1.02 AED · 1 EGP ≈ 0.076 AED)</div></div>
    </div>
    """,
    unsafe_allow_html=True,
)
