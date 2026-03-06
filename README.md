# ◈ CareerIQ — Job Market Intelligence System

> Real-time job market analytics for Data, AI, ML & Cloud roles across India.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app.streamlit.app)

---

## What is CareerIQ?

CareerIQ turns raw LinkedIn job listing data into structured career intelligence. It helps students understand hiring demand, professionals identify skill gaps, and researchers observe market trends — all from a single unified platform.

---

## Features

| Page | What it does |
|---|---|
| 🏠 Home | KPI overview with live data freshness indicator |
| 📊 Dashboard | Hiring trends, role demand, city distribution, experience breakdown |
| 🔧 Skills Intelligence | Top skills per role with frequency charts & recommendations |
| 📂 Data Explorer | Browse, filter and export the full job dataset as CSV |
| 📲 WhatsApp Insight | Generate & send market reports via Twilio |
| 🔄 Data Refresh | Fetch fresh LinkedIn job listings on demand via JSearch API |

---

## Project Structure

```
CareerIQ/
├── app/
│   ├── app.py                  # Single-file Streamlit app (all pages)
│   ├── .streamlit/
│   │   ├── config.toml         # Dark theme config
│   │   └── secrets.toml        # API keys — NOT committed to git
│   └── utils/
│       ├── data_loader.py      # CSV loading, caching, staleness check
│       ├── data_processing.py  # Role mapping, location cleanup, experience bands
│       ├── scraper.py          # JSearch API integration
│       ├── ui_components.py    # Shared CSS design system & components
│       └── whatsapp_utils.py   # Twilio WhatsApp sender
├── Data/
│   ├── Processed/
│   │   ├── jobs_master.csv     # Main dataset
│   │   └── scrape_log.csv      # Fetch history log
│   └── Raw/                    # Original source datasets
├── ml/                         # EDA & preprocessing scripts
├── requirements.txt
└── README.md
```

---

## Setup & Run Locally

### 1. Clone & install

```bash
git clone https://github.com/nadeem12-cloud/CareerIQ.git
cd CareerIQ
pip install -r requirements.txt
```

### 2. Get a free JSearch API key

1. Go to [rapidapi.com → JSearch](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch)
2. Sign up and subscribe to the **Basic plan** (free — 200 requests/month)
3. Copy your `X-RapidAPI-Key`

### 3. Configure secrets

Create `app/.streamlit/secrets.toml`:

```toml
RAPIDAPI_KEY = "your_key_here"

# Optional — for WhatsApp features
TWILIO_SID   = "your_sid"
TWILIO_TOKEN = "your_token"
TWILIO_FROM  = "whatsapp:+14155238886"
TWILIO_TO    = "whatsapp:+91xxxxxxxxxx"
```

### 4. Run

```bash
cd app
streamlit run app.py
```

---

## Deploy on Streamlit Cloud

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) → New app
3. Set main file path to `app/app.py`
4. Go to **Settings → Secrets** and paste your `secrets.toml` contents
5. Deploy

---

## Data Refresh

Navigate to **🔄 Data Refresh** in the app:

- Click **🔬 Run API Test** to verify your key
- Click **🚀 Fetch Latest Jobs** to pull fresh listings
- Each fetch pulls ~100 jobs (5 queries × 2 pages × ~10 jobs/page)
- Free tier = 200 requests/month ≈ 5 full refreshes/month

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Data Processing | Pandas |
| Visualisation | Plotly Express |
| Live Job Data | JSearch API (RapidAPI) |
| WhatsApp | Twilio Sandbox |
| Styling | Custom CSS — Space Mono + DM Sans |

---

## Architecture

```
JSearch API → scraper.py → jobs_master.csv → data_loader.py → app.py
```

- All pages rendered inside a single `app.py` using `st.session_state` for navigation
- No sidebar — dropdown nav is immune to Streamlit re-run issues
- Data staleness auto-detected with optional auto-refresh on load

---

*CareerIQ — Mini Project · 2026*
