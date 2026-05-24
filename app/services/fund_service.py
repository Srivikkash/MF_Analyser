from datetime import datetime
import numpy as np
import pandas as pd
import yfinance as yf
from flask import current_app
from mftool import Mftool

from app import cache
from app.services.api_client import APIClient


class FundService:
    def __init__(self):
        self.client = APIClient()
        self.mftool = Mftool()

    @cache.memoize(timeout=120)
    def list_funds(self):
        return self.client.get_json(f"{current_app.config['MFAPI_BASE_URL']}/mf")

    @cache.memoize(timeout=120)
    def fund_detail(self, scheme_code):
        return self.client.get_json(f"{current_app.config['MFAPI_BASE_URL']}/mf/{scheme_code}")

    def search(self, query):
        return self.client.get_json(f"{current_app.config['MFAPI_BASE_URL']}/mf/search", params={"q": query})

    def nav_dataframe(self, scheme_code):
        detail = self.fund_detail(scheme_code)
        df = pd.DataFrame(detail.get("data", []))
        if df.empty:
            return df
        df["date"] = pd.to_datetime(df["date"], dayfirst=True)
        df["nav"] = pd.to_numeric(df["nav"], errors="coerce")
        return df.sort_values("date")

    def analytics(self, scheme_code):
        df = self.nav_dataframe(scheme_code)
        if df.empty:
            return {}
        latest = df.iloc[-1]["nav"]
        ret_1y = self._cagr(df, 1)
        ret_3y = self._cagr(df, 3)
        ret_5y = self._cagr(df, 5)
        daily = df["nav"].pct_change().dropna()
        volatility = float(daily.std() * np.sqrt(252)) if not daily.empty else 0
        drawdown = ((df["nav"] / df["nav"].cummax()) - 1).min()
        return {
            "latest_nav": float(latest),
            "cagr_1y": ret_1y,
            "cagr_3y": ret_3y,
            "cagr_5y": ret_5y,
            "volatility": volatility,
            "std_dev": float(daily.std()) if not daily.empty else 0,
            "drawdown": float(drawdown),
            "dates": df["date"].dt.strftime("%Y-%m-%d").tolist(),
            "nav": df["nav"].round(2).tolist(),
        }

    def _cagr(self, df, years):
        cutoff = df["date"].max() - pd.DateOffset(years=years)
        subset = df[df["date"] >= cutoff]
        if subset.empty:
            return None
        start = subset.iloc[0]["nav"]
        end = subset.iloc[-1]["nav"]
        if start <= 0:
            return None
        return float((end / start) ** (1 / years) - 1)

    def fmp_etf_info(self, symbol):
        return self.client.get_json(f"{current_app.config['FMP_BASE_URL']}/etf-info/{symbol}", params={"apikey": current_app.config["FMP_API_KEY"]})

    def yf_info(self, ticker):
        t = yf.Ticker(ticker)
        return {"info": t.info, "fast_info": dict(t.fast_info)}
