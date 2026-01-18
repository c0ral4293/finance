import yfinance as yf
import pandas as pd
import numpy as np

def fetch_data(ticker):
    stock = yf.Ticker(ticker)

    info = stock.info
    financials = stock.financials
    balance_sheet = stock.balance_sheet

    return info, financials, balance_sheet


def calculate_ratios(info, financials, balance_sheet):
    ratios = {}

    ratios["P/E Ratio"] = info.get("trailingPE", np.nan)
    ratios["P/B Ratio"] = info.get("priceToBook", np.nan)

    try:
        net_income = financials.loc["Net Income"].iloc[0]
        revenue = financials.loc["Total Revenue"].iloc[0]
        ratios["Net Profit Margin (%)"] = (net_income / revenue) * 100
    except:
        ratios["Net Profit Margin (%)"] = np.nan

    try:
        total_assets = balance_sheet.loc["Total Assets"].iloc[0]
        total_liabilities = balance_sheet.loc["Total Liab"].iloc[0]
        ratios["Debt to Equity"] = total_liabilities / total_assets
    except:
        ratios["Debt to Equity"] = np.nan

    return pd.DataFrame(
        list(ratios.items()),
        columns=["Metric", "Value"]
    )