"""
Shared sidebar filter component.
Call apply_filters(df) at the top of every page to get a filtered DataFrame.
"""

from __future__ import annotations
import datetime
import pandas as pd
import streamlit as st
from pathlib import Path
import base64


def _logo_html() -> str:
    logo_path = Path(__file__).parent.parent / "assets" / "careem-logo.png"
    if logo_path.exists():
        data = base64.b64encode(logo_path.read_bytes()).decode()
        return f'<img src="data:image/png;base64,{data}" style="width:130px;margin-bottom:8px;">'
    return '<span style="font-size:22px;font-weight:700;color:#00B14F;">careem</span>'


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Render sidebar filters and return the filtered slice of df.
    Must be called after st.set_page_config() and inject_css().
    """
    with st.sidebar:
        # ── Logo ────────────────────────────────────────────────────────
        st.markdown(_logo_html(), unsafe_allow_html=True)
        st.markdown(
            '<p style="font-size:10px;color:#64748B;margin-top:-4px;">MIT622 · 2025 · Group 1</p>',
            unsafe_allow_html=True,
        )
        st.markdown('<hr style="border-color:#E2E8F0;margin:8px 0 16px 0;">', unsafe_allow_html=True)

        # ── Date range ──────────────────────────────────────────────────
        st.markdown('<p style="font-size:11px;color:#94A3B8;font-weight:600;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:4px;"><i class="bi bi-calendar3" style="color:#00B14F;margin-right:4px;"></i>Date Range</p>', unsafe_allow_html=True)
        min_date = df["Date"].min().date()
        max_date = df["Date"].max().date()
        date_from = st.date_input("From", value=min_date, min_value=min_date, max_value=max_date, key="filter_date_from", label_visibility="collapsed")
        date_to   = st.date_input("To",   value=max_date, min_value=min_date, max_value=max_date, key="filter_date_to",   label_visibility="collapsed")

        # ── City ────────────────────────────────────────────────────────
        st.markdown('<hr style="border-color:#E2E8F0;margin:12px 0;">', unsafe_allow_html=True)
        st.markdown('<p style="font-size:11px;color:#94A3B8;font-weight:600;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:4px;"><i class="bi bi-buildings" style="color:#00B14F;margin-right:4px;"></i>City</p>', unsafe_allow_html=True)
        all_cities  = sorted(df["City"].dropna().unique().tolist())
        sel_cities  = st.multiselect("City", all_cities, default=all_cities, key="filter_city", label_visibility="collapsed")

        # ── Product ─────────────────────────────────────────────────────
        st.markdown('<hr style="border-color:#E2E8F0;margin:12px 0;">', unsafe_allow_html=True)
        st.markdown('<p style="font-size:11px;color:#94A3B8;font-weight:600;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:4px;"><i class="bi bi-car-front" style="color:#00B14F;margin-right:4px;"></i>Product</p>', unsafe_allow_html=True)
        all_products = df["Product"].dropna().unique().tolist()
        sel_products = st.multiselect("Product", all_products, default=all_products, key="filter_product", label_visibility="collapsed")

        # ── Customer Tier ────────────────────────────────────────────────
        st.markdown('<hr style="border-color:#E2E8F0;margin:12px 0;">', unsafe_allow_html=True)
        st.markdown('<p style="font-size:11px;color:#94A3B8;font-weight:600;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:4px;"><i class="bi bi-person-badge" style="color:#00B14F;margin-right:4px;"></i>Customer Tier</p>', unsafe_allow_html=True)
        all_tiers = df["Customer_Tier"].dropna().unique().tolist()
        sel_tiers = st.multiselect("Customer Tier", all_tiers, default=all_tiers, key="filter_tier", label_visibility="collapsed")

        # ── Trip Purpose ─────────────────────────────────────────────────
        st.markdown('<hr style="border-color:#E2E8F0;margin:12px 0;">', unsafe_allow_html=True)
        st.markdown('<p style="font-size:11px;color:#94A3B8;font-weight:600;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:4px;"><i class="bi bi-signpost-2" style="color:#00B14F;margin-right:4px;"></i>Trip Purpose</p>', unsafe_allow_html=True)
        all_purposes = sorted(df["Trip_Purpose"].dropna().unique().tolist())
        sel_purposes = st.multiselect("Trip Purpose", all_purposes, default=all_purposes, key="filter_purpose", label_visibility="collapsed")

        # ── Dataset info ──────────────────────────────────────────────────
        st.markdown('<hr style="border-color:#E2E8F0;margin:16px 0 8px 0;">', unsafe_allow_html=True)
        st.markdown(
            '<p style="font-size:10px;color:#475569;line-height:1.9;">'
            '<i class="bi bi-database" style="color:#00B14F;"></i> 500,000 ride records<br>'
            '<i class="bi bi-geo-alt" style="color:#00B14F;"></i> Dubai · Abu Dhabi · Riyadh · Jeddah · Cairo<br>'
            '<i class="bi bi-calendar3" style="color:#00B14F;"></i> Jan – Dec 2025<br>'
            '<i class="bi bi-currency-exchange" style="color:#00B14F;"></i> AED-normalized fares</p>',
            unsafe_allow_html=True,
        )

    # ── Apply filters ────────────────────────────────────────────────────
    mask = (
        (df["Date"].dt.date >= date_from) &
        (df["Date"].dt.date <= date_to)
    )
    if sel_cities:
        mask &= df["City"].isin(sel_cities)
    if sel_products:
        mask &= df["Product"].isin(sel_products)
    if sel_tiers:
        mask &= df["Customer_Tier"].isin(sel_tiers)
    if sel_purposes:
        mask &= df["Trip_Purpose"].isin(sel_purposes)

    return df[mask].copy()
