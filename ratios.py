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
        net_income = financials.loc["Net Income"]
        revenue = financials.loc["Total Revenue"]
        total_assets = balance_sheet.loc["Total Assets"]
        total_liabilities = balance_sheet.loc["Total Liab"]
        current_assets = balance_sheet.loc["Current Assets"]
        current_liabilities = balance_sheet.loc["Current Liabilities"]

#ratios for 2025
        ratios["Net Profit Margin (%)"] = (net_income.iloc[0] / revenue.iloc[0]) * 100
        ratios["Return on Assets (%)"] = (net_income.iloc[0] / total_assets.iloc[0]) * 100
        ratios["Return on Equity (%)"] = (net_income.iloc[0] / (total_assets.iloc[0] - total_liabilities.iloc[0])) * 100
        ratios["Current Ratio"] = current_assets.iloc[0] / current_liabilities.iloc[0]
        ratios["Debt to Equity"] = total_liabilities.iloc[0] / (total_assets.iloc[0] - total_liabilities.iloc[0])
 #ratios for 2024
        ratios["Net Profit Margin 2024 (%)"] = (net_income.iloc[1] / revenue.iloc[1]) * 100
        ratios["Return on Assets 2024 (%)"] = (net_income.iloc[1] / total_assets.iloc[1]) * 100
        ratios["Return on Equity 2024 (%)"] = (net_income.iloc[1] / (total_assets.iloc[1] - total_liabilities.iloc[1])) * 100
        ratios["Current Ratio 2024"] = current_assets.iloc[1] / current_liabilities.iloc[1]
        ratios["Debt to Equity 2024"] = total_liabilities.iloc[1] / (total_assets.iloc[1] - total_liabilities.iloc[1])
#YOY comparision for the ratios
        ratios["Net Profit Margin (%) YoY Change"] = ratios["Net Profit Margin (%)"] - ratios["Net Profit Margin 2024 (%)"]
        ratios["Return on Assets (%) YoY Change"] = ratios["Return on Assets (%)"] - ratios["Return on Assets 2024 (%)"]
        ratios["Return on Equity (%) YoY Change"] = ratios["Return on Equity (%)"] - ratios["Return on Equity 2024 (%)"]
        ratios["Current Ratio YoY Change"] = ratios["Current Ratio"] - ratios["Current Ratio 2024"]
        ratios["Debt to Equity YoY Change"] = ratios["Debt to Equity"] - ratios["Debt to Equity 2024"]
    except Exception as e:
      ratios["Error"] = str(e)


    return pd.DataFrame(
        list(ratios.items()),
        columns=["Metric", "Value"]
    )

