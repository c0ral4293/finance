import yfinance as yf
import pandas as pd
import numpy as np


def fetch_data(ticker):
    stock = yf.Ticker(ticker)
    return stock.info, stock.financials, stock.balance_sheet


def safe_row(df, name):
    return df.loc[name] if name in df.index else None


def calculate_ratios(info, financials, balance_sheet):
    rows = []

    # -------------------------
    # Market ratios (ONLY current year available)
    # -------------------------
    pe = info.get("trailingPE", np.nan)
    pb = info.get("priceToBook", np.nan)

    rows.append(("P/E Ratio (2025)", pe))
    rows.append(("P/E Ratio (2024)", np.nan))
    rows.append(("P/E Ratio YoY Change", np.nan))

    rows.append(("P/B Ratio (2025)", pb))
    rows.append(("P/B Ratio (2024)", np.nan))
    rows.append(("P/B Ratio YoY Change", np.nan))

    # -------------------------
    # Financial statement data
    # -------------------------
    net_income = safe_row(financials, "Net Income")
    revenue = safe_row(financials, "Total Revenue")
    total_assets = safe_row(balance_sheet, "Total Assets")
    total_liab = safe_row(balance_sheet, "Total Liab")
    current_assets = safe_row(balance_sheet, "Total Current Assets")
    current_liab = safe_row(balance_sheet, "Total Current Liabilities")

    if all(x is not None for x in [net_income, revenue, total_assets, total_liab]):
        equity = total_assets - total_liab

        # ---- Net Profit Margin ----
        npm_2025 = (net_income.iloc[0] / revenue.iloc[0]) * 100
        npm_2024 = (net_income.iloc[1] / revenue.iloc[1]) * 100

        rows += [
            ("Net Profit Margin (%) (2025)", npm_2025),
            ("Net Profit Margin (%) (2024)", npm_2024),
            ("Net Profit Margin YoY Change", npm_2025 - npm_2024),
        ]

        # ---- ROA ----
        roa_2025 = (net_income.iloc[0] / total_assets.iloc[0]) * 100
        roa_2024 = (net_income.iloc[1] / total_assets.iloc[1]) * 100

        rows += [
            ("Return on Assets (%) (2025)", roa_2025),
            ("Return on Assets (%) (2024)", roa_2024),
            ("ROA YoY Change", roa_2025 - roa_2024),
        ]

        # ---- ROE ----
        roe_2025 = (net_income.iloc[0] / equity.iloc[0]) * 100
        roe_2024 = (net_income.iloc[1] / equity.iloc[1]) * 100

        rows += [
            ("Return on Equity (%) (2025)", roe_2025),
            ("Return on Equity (%) (2024)", roe_2024),
            ("ROE YoY Change", roe_2025 - roe_2024),
        ]

        # ---- Debt to Equity ----
        dte_2025 = total_liab.iloc[0] / equity.iloc[0]
        dte_2024 = total_liab.iloc[1] / equity.iloc[1]

        rows += [
            ("Debt to Equity (2025)", dte_2025),
            ("Debt to Equity (2024)", dte_2024),
            ("Debt to Equity YoY Change", dte_2025 - dte_2024),
        ]

    # -------------------------
    # Liquidity ratios
    # -------------------------
    if current_assets is not None and current_liab is not None:
        cr_2025 = current_assets.iloc[0] / current_liab.iloc[0]
        cr_2024 = current_assets.iloc[1] / current_liab.iloc[1]

        rows += [
            ("Current Ratio (2025)", cr_2025),
            ("Current Ratio (2024)", cr_2024),
            ("Current Ratio YoY Change", cr_2025 - cr_2024),
        ]

    return pd.DataFrame(rows, columns=["Metric", "Value"])