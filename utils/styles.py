"""
Custom CSS + brand theming for the Careem 2025 Supply–Demand Intelligence Cockpit.
Inject with inject_css() at the top of every page.
"""

CAREEM_GREEN  = "#00B14F"
CAREEM_NAVY   = "#0F172A"
CAREEM_CARD   = "#1E293B"
CAREEM_BORDER = "#2D3F55"
CAREEM_AMBER  = "#F59E0B"
CAREEM_RED    = "#EF4444"
CAREEM_SLATE  = "#94A3B8"
CAREEM_WHITE  = "#F1F5F9"

PLOTLY_COLORS = [
    "#00B14F", "#38BDF8", "#F59E0B", "#EF4444",
    "#8B5CF6", "#EC4899", "#14B8A6", "#FB923C",
]

PLOTLY_TEMPLATE = "plotly_dark"

_CSS = """
<style>
/* ── Reset & base ── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #0F172A !important;
    color: #F1F5F9 !important;
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%) !important;
    border-right: 1px solid #2D3F55 !important;
}
[data-testid="stSidebar"] .stMarkdown p { color: #94A3B8; font-size: 12px; }
[data-testid="stSidebar"] hr { border-color: #2D3F55; }

/* ── Sidebar navigation links ── */
[data-testid="stSidebarNav"] a {
    background: transparent;
    border-radius: 8px;
    padding: 8px 12px;
    color: #94A3B8 !important;
    font-size: 13px;
    font-weight: 500;
    transition: all 0.2s ease;
    border-left: 3px solid transparent;
}
[data-testid="stSidebarNav"] a:hover {
    background: #1E293B !important;
    color: #00B14F !important;
    border-left-color: #00B14F;
}
[data-testid="stSidebarNav"] a[aria-current="page"] {
    background: rgba(0,177,79,0.12) !important;
    color: #00B14F !important;
    border-left: 3px solid #00B14F;
    font-weight: 600;
}

/* ── Page container ── */
.block-container {
    padding: 1.5rem 2rem 2rem 2rem !important;
    max-width: 1400px !important;
}

/* ── Page header banner ── */
.page-header {
    background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
    border: 1px solid #2D3F55;
    border-left: 4px solid #00B14F;
    border-radius: 12px;
    padding: 20px 28px;
    margin-bottom: 24px;
}
.page-header h1 {
    font-size: 26px;
    font-weight: 700;
    color: #F1F5F9;
    margin: 0 0 4px 0;
    letter-spacing: -0.3px;
}
.page-header p {
    font-size: 13px;
    color: #94A3B8;
    margin: 0;
}

/* ── KPI Metric cards ── */
.kpi-card {
    background: #1E293B;
    border: 1px solid #2D3F55;
    border-top: 3px solid #00B14F;
    border-radius: 12px;
    padding: 18px 20px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(135deg, rgba(0,177,79,0.05) 0%, transparent 60%);
    pointer-events: none;
}
.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.4);
}
.kpi-label {
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #94A3B8;
    margin-bottom: 8px;
}
.kpi-value {
    font-size: 28px;
    font-weight: 700;
    color: #F1F5F9;
    letter-spacing: -0.5px;
    line-height: 1;
}
.kpi-value.green  { color: #00B14F; }
.kpi-value.amber  { color: #F59E0B; }
.kpi-value.red    { color: #EF4444; }
.kpi-delta {
    font-size: 12px;
    color: #94A3B8;
    margin-top: 4px;
}
.kpi-delta.pos { color: #00B14F; }
.kpi-delta.neg { color: #EF4444; }

/* ── Insight / callout box ── */
.insight-box {
    background: rgba(245,158,11,0.08);
    border: 1px solid rgba(245,158,11,0.35);
    border-left: 4px solid #F59E0B;
    border-radius: 10px;
    padding: 14px 18px;
    margin: 16px 0;
    font-size: 13px;
    color: #F1F5F9;
    line-height: 1.6;
}
.insight-box strong { color: #F59E0B; }

/* ── Section sub-headers ── */
.section-title {
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #64748B;
    padding: 12px 0 8px 0;
    border-bottom: 1px solid #2D3F55;
    margin-bottom: 16px;
}

/* ── Chart containers ── */
.stPlotlyChart {
    border: 1px solid #2D3F55;
    border-radius: 12px;
    overflow: hidden;
    background: #1E293B;
}

/* ── Streamlit Metric overrides ── */
[data-testid="metric-container"] {
    background: #1E293B;
    border: 1px solid #2D3F55;
    border-top: 3px solid #00B14F;
    border-radius: 12px;
    padding: 16px;
}
[data-testid="metric-container"] label {
    color: #94A3B8 !important;
    font-size: 11px !important;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #F1F5F9 !important;
    font-size: 28px !important;
    font-weight: 700 !important;
}
[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    font-size: 12px !important;
}

/* ── Streamlit selectbox / multiselect ── */
[data-testid="stMultiSelect"] > div,
[data-testid="stSelectbox"] > div > div {
    background: #1E293B !important;
    border-color: #2D3F55 !important;
    border-radius: 8px;
    color: #F1F5F9 !important;
}
.stMultiSelect [data-baseweb="tag"] {
    background: rgba(0,177,79,0.25) !important;
    color: #00B14F !important;
    border: 1px solid rgba(0,177,79,0.5) !important;
}

/* ── Sliders ── */
[data-testid="stSlider"] [role="slider"] { background: #00B14F !important; }
[data-testid="stSlider"] [data-baseweb="slider"] div[style] { background: #00B14F !important; }

/* ── Date input ── */
[data-testid="stDateInput"] input {
    background: #1E293B !important;
    border-color: #2D3F55 !important;
    color: #F1F5F9 !important;
    border-radius: 8px;
}

/* ── Tables ── */
.stDataFrame { border-radius: 12px; overflow: hidden; }
.stDataFrame table { background: #1E293B; color: #F1F5F9; }
.stDataFrame thead th { background: #0F172A; color: #94A3B8; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; }
.stDataFrame tbody tr:hover { background: rgba(0,177,79,0.06); }

/* ── Divider ── */
hr { border-color: #2D3F55 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0F172A; }
::-webkit-scrollbar-thumb { background: #2D3F55; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #00B14F; }

/* ── Navigation tiles on Home ── */
.nav-tile {
    background: #1E293B;
    border: 1px solid #2D3F55;
    border-radius: 14px;
    padding: 24px 20px;
    text-align: center;
    cursor: pointer;
    transition: all 0.25s ease;
    height: 100%;
}
.nav-tile:hover {
    border-color: #00B14F;
    background: rgba(0,177,79,0.08);
    transform: translateY(-3px);
    box-shadow: 0 12px 32px rgba(0,0,0,0.4);
}
.nav-tile .nav-icon { font-size: 32px; margin-bottom: 12px; }
.nav-tile h3 { font-size: 14px; font-weight: 600; color: #F1F5F9; margin: 0 0 6px 0; }
.nav-tile p  { font-size: 12px; color: #64748B; margin: 0; }

/* ── Completion target badge ── */
.target-badge {
    display: inline-block;
    background: rgba(0,177,79,0.15);
    color: #00B14F;
    border: 1px solid rgba(0,177,79,0.4);
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 11px;
    font-weight: 600;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: #1E293B;
    border: 1px solid #2D3F55;
    border-radius: 10px;
}

/* ── Success / warning / error Alerts ── */
[data-testid="stAlert"] {
    border-radius: 10px;
}
</style>
"""

def inject_css():
    """Call at the top of every page to apply full custom theme."""
    import streamlit as st
    st.markdown(_CSS, unsafe_allow_html=True)


def page_header(title: str, subtitle: str = ""):
    """Render a branded page header banner."""
    import streamlit as st
    sub_html = f'<p>{subtitle}</p>' if subtitle else ""
    st.markdown(
        f'<div class="page-header"><h1>{title}</h1>{sub_html}</div>',
        unsafe_allow_html=True,
    )


def kpi_card(label: str, value: str, delta: str = "", color: str = ""):
    """Render a custom KPI card (use inside st.columns)."""
    import streamlit as st
    color_cls = f" {color}" if color else ""
    delta_cls = "pos" if delta.startswith("+") else ("neg" if delta.startswith("-") else "")
    delta_html = f'<div class="kpi-delta {delta_cls}">{delta}</div>' if delta else ""
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value{color_cls}">{value}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def insight_box(text: str):
    """Render an amber insight callout box."""
    import streamlit as st
    st.markdown(f'<div class="insight-box">{text}</div>', unsafe_allow_html=True)


def section_title(text: str):
    """Render a small section header."""
    import streamlit as st
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)
