# 📈 Stock Market Data Pipeline

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=flat&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)
![Polars](https://img.shields.io/badge/Polars-CD792C?style=flat&logo=polars&logoColor=white)
![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=flat&logo=chartdotjs&logoColor=white)

A full **ETL data pipeline** that extracts live stock market data, transforms it with financial indicators, stores it in SQLite, and visualizes it in a real-time Chart.js dashboard — served via a Flask REST API.

---

## 🏗️ Architecture
```
yfinance API
     ↓
[Extract] → raw OHLCV data
     ↓
[Transform] → moving averages, % change, volatility
     ↓
[Load] → SQLite database
     ↓
[Flask API] → REST endpoints
     ↓
[Chart.js Dashboard] → live visualization
```

---

## 🚀 Features

- **Extract** — pulls 3 months of daily OHLCV data for 5 tickers via `yfinance`
- **Transform** — calculates SMA 20, SMA 50, daily % change, and 20-day volatility using `polars`
- **Load** — stores cleaned data in a local `SQLite` database
- **API** — Flask REST API with `/api/tickers`, `/api/latest`, `/api/stock/<ticker>` endpoints
- **Dashboard** — dark-themed Chart.js frontend with price charts, moving averages, and % change bars

---

## 🗂️ Project Structure
```
stock-pipeline/
├── etl/
│   ├── extract.py       # yfinance data pull
│   ├── transform.py     # polars transformations
│   └── load.py          # SQLite loader
├── static/
│   ├── css/style.css    # dashboard styles
│   └── js/dashboard.js  # Chart.js frontend
├── templates/
│   └── index.html       # dashboard HTML
├── app.py               # Flask API
├── config.py            # settings (tickers, DB path)
├── run_pipeline.py      # single command ETL runner
├── pyproject.toml       # editable package config
└── requirements.txt
```

---

## ⚙️ Setup
```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/stock-pipeline.git
cd stock-pipeline

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
pip install -e .

# 4. Run the ETL pipeline
python run_pipeline.py

# 5. Start the dashboard
python app.py
```

Then open `http://127.0.0.1:5000` in your browser.

---

## 📡 API Endpoints

| Endpoint | Description |
|---|---|
| `GET /` | Dashboard UI |
| `GET /api/tickers` | List of all tracked tickers |
| `GET /api/latest` | Latest price + % change for all tickers |
| `GET /api/stock/<ticker>` | Full historical data for a ticker |

---

## 🛠️ Stack

| Layer | Technology |
|---|---|
| Data extraction | `yfinance` |
| Data transformation | `polars` |
| Database | `SQLite` |
| Backend API | `Flask` |
| Frontend | `Chart.js` |

---

## 💡 How to refresh data
```bash
python run_pipeline.py
```

Re-run this any time to pull the latest market data and update the database.
