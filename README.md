# 📈 Stock Market Data Pipeline

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=flat&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)
![Polars](https://img.shields.io/badge/Polars-CD792C?style=flat&logo=polars&logoColor=white)
![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=flat&logo=chartdotjs&logoColor=white)

A full ETL pipeline that pulls live stock data, runs some financial calculations on it, stores everything in a database, and displays it in a dashboard. Built this to actually understand what a data pipeline looks like end to end — not just a script that prints stuff.

---

## Why I built this

I kept seeing "ETL pipeline" on job descriptions and didn't really know what it meant beyond "extract transform load". So I built one. Wanted something that felt like a real project a company might actually use, not just another tutorial clone.

Also wanted to get comfortable with the full stack side of data — most data projects I'd seen just ended at a jupyter notebook. This one goes all the way from raw API data to a live dashboard with a proper backend.

---

## What it does

- **Extracts** daily OHLCV stock data for 5 tickers (AAPL, MSFT, GOOGL, NVDA, TSLA) from yfinance
- **Transforms** it with Polars — calculates 20/50 day moving averages, daily % change, and rolling volatility
- **Loads** the cleaned data into a SQLite database
- **Serves** it via a Flask REST API
- **Visualizes** it in a Chart.js dashboard with price charts and % change bars

---

## What I learned

Honestly this project taught me more than I expected:

- **How Python imports actually work** — ran into module resolution issues early on and had to learn about editable installs with `pyproject.toml` properly instead of just hacking `sys.path`
- **Polars vs Pandas** — hadn't used Polars before. It's faster and the syntax is cleaner once you get used to it. The `.over()` for window functions is really nice
- **Docker** — understood the concept before but actually containerizing a real app with a database and making it work was a different thing
- **CI/CD** — setting up GitHub Actions to test the pipeline on every push felt like a big step up from just pushing code and hoping it works
- **Why separation of concerns matters** — keeping extract, transform, and load in separate files made debugging so much easier than if it was all in one script

---

## Stack

| Layer | Tech |
|---|---|
| Data extraction | `yfinance` |
| Data transformation | `polars` |
| Database | `SQLite` |
| Backend | `Flask` |
| Frontend | `Chart.js` |
| Container | `Docker` |
| CI/CD | `GitHub Actions` |
| Hosting | `Railway` |

---

## Live demo

🔗 [your-railway-url.railway.app](https://your-railway-url.railway.app)

---

## Run it locally
```bash
git clone https://github.com/YOUR_USERNAME/stock-pipeline.git
cd stock-pipeline

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
pip install -e .

python run_pipeline.py
python app.py
```

Then open `http://localhost:5000`.

Or with Docker:
```bash
docker compose up
```
