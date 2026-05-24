# Indian Mutual Fund Analyzer

Production-ready Flask + Jinja mutual fund analyzer that fetches live data on every request path and only caches in-memory for short durations.

## Features
- Live mutual fund list/search/detail from MFapi.in
- Portfolio tracker and watchlist persisted in MongoDB
- Fund analytics (CAGR, volatility, drawdown) computed in real time with Pandas/NumPy
- Responsive Bootstrap UI with dark/light mode
- Chart.js NAV history graph
- Retry-aware API abstraction service

## Run
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Environment
- `MONGO_URI` (e.g. `mongodb://localhost:27017` or Atlas URI)
- `MONGO_DB_NAME` (e.g. `mf_analyzer`)

## Production
```bash
gunicorn -w 4 -b 0.0.0.0:8000 'app:create_app()'
```

## Data policy
- Stored in MongoDB: users, auth, watchlist, portfolio transactions.
- Never stored: fund master data, NAV history, holdings, live market metrics.
