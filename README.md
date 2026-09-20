# India Data Visualization Dashboard

An interactive Streamlit dashboard for exploring district-level Indian demographic and socioeconomic data.

**Live dashboard:** [dashboard-liard-seven-19.vercel.app](https://dashboard-liard-seven-19.vercel.app/)

The production deployment is a browser-native dashboard with an interactive Leaflet/OpenStreetMap district map, responsive Plotly charts, filters, KPI cards, and a searchable table. The original Streamlit implementation remains in `app.py` for local Python use.

## Features

- State-level filtering with an overall India view
- Interactive district map
- Population and internet-access visualization
- Literacy-rate and sex-ratio analysis
- Top-10 district comparisons
- District search and detail explorer
- Side-by-side district comparison
- Full dataset table
- CSV export

## Tech stack

- Python
- Streamlit
- Pandas
- Plotly
- NumPy

## Run locally

```bash
git clone https://github.com/divbytes-prog/dashboard.git
cd dashboard
pip install -r requirements.txt
streamlit run app.py
```

The dashboard expects `india.csv` in the repository root.

## Project structure

```text
app.py            Streamlit application
index.html        Vercel-ready browser dashboard
india.csv         District-level dataset
requirements.txt  Python dependencies
vercel.json       Production hosting configuration
```

## What I explored

This project focuses on turning a multidimensional dataset into an interactive interface using maps, filters, KPIs, comparisons, charts, and downloadable data.

---

Built by [Divyansh Singh](https://github.com/divbytes-prog).
