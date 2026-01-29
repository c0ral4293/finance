import yfinance as yf
import pandas as pd
import numpy as np


def get_value(df, possible_names, col):
    for name in possible_names:
        if name in df.index:
            return df.loc[name].iloc[col]
    return np.nan


def calculate_ratios(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)

    info = ticker.info
    fin = ticker.financials
    bs = ticker.balance_sheet

    if fin.empty or bs.empty:
        raise ValueError("Financial data not available")

    # column 0 = latest (2025), column 1 = previous (2024)
    YEARS = {"2025": 0, "2024": 1}

    data = {}

    for year, col in YEARS.items():
        revenue = get_value(fin, ["Total Revenue", "Revenue"], col)
        net_income = get_value(fin, ["Net Income"], col)

        current_assets = get_value(bs, ["Current Assets"], col)
        current_liab = get_value(bs, ["Current Liabilities"], col)

        total_assets = get_value(bs, ["Total Assets"], col)
        total_liab = get_value(bs, ["Total Liabilities", "Total Liab"], col)
        equity = total_assets - total_liab if not np.isnan(total_assets) else np.nan

        data[year] = {
            "Net Profit Margin": net_income / revenue,
            "Return on Assets": net_income / total_assets,
            "Return on Equity": net_income / equity,
            "Current Ratio": current_assets / current_liab,
            "Debt to Equity": total_liab / equity,
        }

    # Market ratios (same for both years)
    pe = info.get("trailingPE", np.nan)
    pb = info.get("priceToBook", np.nan)

    rows = []

    for ratio in data["2025"]:
        rows.append([
            ratio,
            data["2025"][ratio],
            data["2024"][ratio],
            data["2025"][ratio] - data["2024"][ratio]
        ])

    rows.extend([
        ["P/E Ratio", pe, pe, 0],
        ["P/B Ratio", pb, pb, 0],
    ])

    return pd.DataFrame(
        rows,
        columns=["Ratio", "2025", "2024", "YoY Change"]
    )