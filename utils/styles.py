"""
Custom CSS + brand theming — LIGHT THEME — Careem 2025 Intelligence Cockpit.
Inject with inject_css() at the top of every page.
"""

CAREEM_GREEN  = "#00B14F"
CAREEM_NAVY   = "#0F172A"   # primary text colour on light bg
CAREEM_CARD   = "#FFFFFF"
CAREEM_BORDER = "#E2E8F0"
CAREEM_AMBER  = "#D97706"   # darker amber for legibility on white
CAREEM_RED    = "#DC2626"
CAREEM_SLATE  = "#64748B"
CAREEM_WHITE  = "#F8FAFC"   # page background

PLOTLY_COLORS = [
    "#00B14F", "#3B82F6", "#F59E0B", "#EF4444",
    "#8B5CF6", "#EC4899", "#14B8A6", "#FB923C",
]

PLOTLY_TEMPLATE = "plotly_white"

# Chart axis / grid colours — import in pages instead of hardcoding
CHART_GRID = "#E2E8F0"
CHART_FONT = "#64748B"
CHART_FONT_FAMILY = "'Inter', 'DM Sans', -apple-system, sans-serif"

_CSS = """
<style>
/* ── Google Fonts — Inter ── */
@import url("https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap");
/* ── Bootstrap Icons (CDN) ── */
@import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css");

/* ── Reset & base ── */
html, body, [data-testid="stAppViewContainer"],
[data-testid="stSidebar"],
.stMarkdown, .stText, button, input, select, textarea {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}
html, body, [data-testid="stAppViewContainer"] {
    background-color: #F8FAFC !important;
    color: #0F172A !important;
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%) !important;
    border-right: 1px solid #E2E8F0 !important;
}
[data-testid="stSidebar"] .stMarkdown p { color: #64748B; font-size: 12px; }
[data-testid="stSidebar"] hr { border-color: #E2E8F0; }

/* ── Sidebar navigation links ── */
[data-testid="stSidebarNav"] a {
    background: transparent;
    border-radius: 8px;
    padding: 8px 12px;
    color: #475569 !important;
    font-size: 13px;
    font-weight: 500;
    transition: all 0.2s ease;
    border-left: 3px solid transparent;
}
[data-testid="stSidebarNav"] a:hover {
    background: #F0FDF4 !important;
    color: #00B14F !important;
    border-left-color: #00B14F;
}
[data-testid="stSidebarNav"] a[aria-current="page"] {
    background: rgba(0,177,79,0.10) !important;
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
    background: linear-gradient(135deg, #F0FDF4 0%, #FFFFFF 100%);
    border: 1px solid #E2E8F0;
    border-left: 4px solid #00B14F;
    border-radius: 12px;
    padding: 20px 28px;
    margin-bottom: 24px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.page-header h1 {
    font-size: 26px;
    font-weight: 700;
    color: #0F172A;
    margin: 0 0 4px 0;
    letter-spacing: -0.3px;
}
.page-header p {
    font-size: 13px;
    color: #64748B;
    margin: 0;
}
.page-header .bi {
    color: #00B14F;
    margin-right: 10px;
    font-size: 22px;
    vertical-align: middle;
}

/* ── KPI Metric cards ── */
.kpi-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-top: 3px solid #00B14F;
    border-radius: 12px;
    padding: 18px 20px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    position: relative;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.kpi-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(135deg, rgba(0,177,79,0.03) 0%, transparent 60%);
    pointer-events: none;
}
.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.10);
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
    color: #0F172A;
    letter-spacing: -0.5px;
    line-height: 1;
}
.kpi-value.green  { color: #00B14F; }
.kpi-value.amber  { color: #D97706; }
.kpi-value.red    { color: #DC2626; }
.kpi-delta {
    font-size: 12px;
    color: #94A3B8;
    margin-top: 4px;
}
.kpi-delta.pos { color: #00B14F; }
.kpi-delta.neg { color: #DC2626; }

/* ── Insight / callout box ── */
.insight-box {
    background: #FFFBEB;
    border: 1px solid #FCD34D;
    border-left: 4px solid #D97706;
    border-radius: 10px;
    padding: 14px 18px;
    margin: 16px 0;
    font-size: 13px;
    color: #0F172A;
    line-height: 1.6;
}
.insight-box strong { color: #92400E; }
.insight-box .bi { font-size: 15px; vertical-align: middle; margin-right: 5px; color: #D97706; }

/* ── Section sub-headers ── */
.section-title {
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #94A3B8;
    padding: 12px 0 8px 0;
    border-bottom: 1px solid #E2E8F0;
    margin-bottom: 16px;
}
.section-title .bi { color: #00B14F; margin-right: 6px; font-size: 13px; vertical-align: middle; }

/* ── Chart containers ── */
.stPlotlyChart {
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    overflow: hidden;
    background: #FFFFFF;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

/* ── Streamlit Metric overrides ── */
[data-testid="metric-container"] {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-top: 3px solid #00B14F;
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
[data-testid="metric-container"] label {
    color: #94A3B8 !important;
    font-size: 11px !important;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #0F172A !important;
    font-size: 28px !important;
    font-weight: 700 !important;
}
[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    font-size: 12px !important;
}

/* ── Streamlit selectbox / multiselect ── */
[data-testid="stMultiSelect"] > div,
[data-testid="stSelectbox"] > div > div {
    background: #FFFFFF !important;
    border-color: #E2E8F0 !important;
    border-radius: 8px;
    color: #0F172A !important;
}
.stMultiSelect [data-baseweb="tag"] {
    background: rgba(0,177,79,0.12) !important;
    color: #00B14F !important;
    border: 1px solid rgba(0,177,79,0.4) !important;
}

/* ── Sliders ── */
[data-testid="stSlider"] [role="slider"] { background: #00B14F !important; }
[data-testid="stSlider"] [data-baseweb="slider"] div[style] { background: #00B14F !important; }

/* ── Date input ── */
[data-testid="stDateInput"] input {
    background: #FFFFFF !important;
    border-color: #E2E8F0 !important;
    color: #0F172A !important;
    border-radius: 8px;
}

/* ── Tables ── */
.stDataFrame { border-radius: 12px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
.stDataFrame table { background: #FFFFFF; color: #0F172A; }
.stDataFrame thead th { background: #F8FAFC; color: #64748B; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 2px solid #E2E8F0; }
.stDataFrame tbody tr:hover { background: rgba(0,177,79,0.04); }

/* ── Divider ── */
hr { border-color: #E2E8F0 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #F8FAFC; }
::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #00B14F; }

/* ── Navigation tiles on Home ── */
.nav-tile {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 24px 20px;
    text-align: center;
    cursor: pointer;
    transition: all 0.25s ease;
    height: 100%;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.nav-tile:hover {
    border-color: #00B14F;
    background: #F0FDF4;
    transform: translateY(-3px);
    box-shadow: 0 12px 32px rgba(0,177,79,0.15);
}
.nav-tile .nav-icon {
    font-size: 30px;
    margin-bottom: 12px;
    color: #00B14F;
    display: block;
}
.nav-tile .nav-icon .bi { font-size: 30px; }
.nav-tile h3 { font-size: 14px; font-weight: 600; color: #0F172A; margin: 0 0 6px 0; }
.nav-tile p  { font-size: 12px; color: #64748B; margin: 0; }

/* ── Completion target badge ── */
.target-badge {
    display: inline-block;
    background: rgba(0,177,79,0.10);
    color: #00B14F;
    border: 1px solid rgba(0,177,79,0.35);
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 11px;
    font-weight: 600;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
}

/* ── Footer data strip ── */
.footer-strip {
    background: #F1F5F9;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 16px 24px;
    display: flex;
    gap: 48px;
    flex-wrap: wrap;
}
.footer-strip .fs-label {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #94A3B8;
    margin-bottom: 4px;
}
.footer-strip .fs-value {
    font-size: 13px;
    color: #0F172A;
}
.footer-strip .bi { color: #00B14F; margin-right: 4px; }
</style>
"""


def inject_css() -> None:
    """Inject light-theme CSS + Bootstrap Icons CDN into the current page."""
    import streamlit as st
    st.markdown(_CSS, unsafe_allow_html=True)


def page_header(title: str, subtitle: str = "", icon: str = "bi-bar-chart-line-fill") -> None:
    """Branded page header with a Bootstrap Icon accent."""
    import streamlit as st
    sub = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(
        f'<div class="page-header"><h1><i class="bi {icon}"></i>{title}</h1>{sub}</div>',
        unsafe_allow_html=True,
    )


def kpi_card(label: str, value: str, delta: str = "", color: str = "") -> None:
    """Custom KPI card (use inside st.columns)."""
    import streamlit as st
    color_cls = f" {color}" if color else ""
    delta_cls = "pos" if delta.startswith("+") else ("neg" if delta.startswith("-") else "")
    delta_html = f'<div class="kpi-delta {delta_cls}">{delta}</div>' if delta else ""
    st.markdown(
        f'<div class="kpi-card"><div class="kpi-label">{label}</div>'
        f'<div class="kpi-value{color_cls}">{value}</div>{delta_html}</div>',
        unsafe_allow_html=True,
    )


def insight_box(text: str) -> None:
    """Amber insight/callout box — supports HTML + Bootstrap Icon <i> tags."""
    import streamlit as st
    st.markdown(f'<div class="insight-box">{text}</div>', unsafe_allow_html=True)


def section_title(text: str, icon: str = "") -> None:
    """Small uppercase section header, optionally with a Bootstrap icon class."""
    import streamlit as st
    icon_html = f'<i class="bi {icon}"></i>' if icon else ""
    st.markdown(f'<div class="section-title">{icon_html}{text}</div>', unsafe_allow_html=True)
