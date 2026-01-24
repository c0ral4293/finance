import yfinance as yf
import pandas as pd
import numpy as np


def fetch_data(ticker):
    stock = yf.Ticker(ticker)
    return stock.info, stock.financials, stock.balance_sheet


def calculate_ratios(info, financials, balance_sheet):
    ratios = {}

    # ---------- Valuation Ratios (single value) ----------
    ratios["P/E Ratio"] = info.get("trailingPE", np.nan)
    ratios["P/B Ratio"] = info.get("priceToBook", np.nan)

    try:
        # ---------- Required rows ----------
        net_income = financials.loc["Net Income"]
        revenue = financials.loc["Total Revenue"]
        total_assets = balance_sheet.loc["Total Assets"]
        total_equity = balance_sheet.loc["Total Stockholder Equity"]
        current_assets = balance_sheet.loc["Current Assets"]
        current_liabilities = balance_sheet.loc["Current Liabilities"]

        # ---------- Latest Year (2025) ----------
        npm_2025 = (net_income.iloc[0] / revenue.iloc[0]) * 100
        roa_2025 = (net_income.iloc[0] / total_assets.iloc[0]) * 100
        roe_2025 = (net_income.iloc[0] / total_equity.iloc[0]) * 100
        current_ratio_2025 = current_assets.iloc[0] / current_liabilities.iloc[0]
        debt_to_equity_2025 = (total_assets.iloc[0] - total_equity.iloc[0]) / total_equity.iloc[0]

        # ---------- Previous Year (2024) ----------
        npm_2024 = (net_income.iloc[1] / revenue.iloc[1]) * 100
        roa_2024 = (net_income.iloc[1] / total_assets.iloc[1]) * 100
        roe_2024 = (net_income.iloc[1] / total_equity.iloc[1]) * 100
        current_ratio_2024 = current_assets.iloc[1] / current_liabilities.iloc[1]
        debt_to_equity_2024 = (total_assets.iloc[1] - total_equity.iloc[1]) / total_equity.iloc[1]

        # ---------- Store Ratios ----------
        ratios["Net Profit Margin 2025 (%)"] = npm_2025
        ratios["Net Profit Margin 2024 (%)"] = npm_2024

        ratios["Return on Assets 2025 (%)"] = roa_2025
        ratios["Return on Assets 2024 (%)"] = roa_2024

        ratios["Return on Equity 2025 (%)"] = roe_2025
        ratios["Return on Equity 2024 (%)"] = roe_2024

        ratios["Current Ratio 2025"] = current_ratio_2025
        ratios["Current Ratio 2024"] = current_ratio_2024

        ratios["Debt to Equity 2025"] = debt_to_equity_2025
        ratios["Debt to Equity 2024"] = debt_to_equity_2024

        # ---------- YoY Comparisons ----------
        ratios["Net Profit Margin YoY Change"] = npm_2025 - npm_2024
        ratios["Return on Assets YoY Change"] = roa_2025 - roa_2024
        ratios["Return on Equity YoY Change"] = roe_2025 - roe_2024
        ratios["Current Ratio YoY Change"] = current_ratio_2025 - current_ratio_2024
        ratios["Debt to Equity YoY Change"] = debt_to_equity_2025 - debt_to_equity_2024

    except Exception as e:
        ratios["Error"] = str(e)

    return pd.DataFrame(ratios.items(), columns=["Metric", "Value"])