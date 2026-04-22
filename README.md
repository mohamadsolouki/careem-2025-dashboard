# Careem 2025 — Supply–Demand Intelligence Cockpit

**MIT622 Data Analytics for Managers · Group 1**
Mohammadsadegh Solouki · Artin Fateh Basharzad · Fatema Alblooshi
Dr. Zaher Al-Sai · 24 April 2026

---

A production-quality Streamlit web dashboard built on 500,000 Careem ride records across 5 MENAP cities in 2025. Mirrors the 8-page Power BI cockpit with full interactive filtering.

## Pages

| # | Page | Key visuals |
|---|------|-------------|
| Home | Navigation hub | KPI strip, 8 nav tiles, dataset info |
| 1 | Executive Overview | GMV trend, product & city donuts, city leaderboard |
| 2 | Completion & Cancellations | Funnel, cancel reasons, city supply-gap table |
| 3 | Demand & Surge | Hour×day heatmap, Ramadan comparison, surge distribution |
| 4 | Pricing Lab | What-if sliders (surge, fare, completion), live GMV waterfall |
| 5 | Captain Pulse | Tenure tiers, rides/captain histogram, GMV deciles, ratings |
| 6 | Customer Lens | Loyalty tier donut, payment mix, spend per tier, repeat rate |
| 7 | Quality & Ratings | ETA deviation, VTAT buckets, captain & customer ratings |
| 8 | Geo Map | City bubble map, full leaderboard, AED/km by city |

## Run locally

```bash
pip install -r requirements.txt
streamlit run Home.py
```

## Deploy to Streamlit Community Cloud

1. Push this repo to GitHub (public)
2. Go to [share.streamlit.io](https://share.streamlit.io) → New app
3. Select repo → Main file path: `Home.py` → Deploy

## Dataset

`dataset/careem_rides_2025.csv` — 500,000 rows · 33 columns · AED-normalized fares
Cities: Dubai · Abu Dhabi · Riyadh · Jeddah · Cairo
Products: Go · Go+ · Business · MAX · Hala Taxi · Hala EV · eBike · Bike
