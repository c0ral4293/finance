import yfinance as yf
import pandas as pd
import numpy as np


def fetch_data(ticker):
    stock = yf.Ticker(ticker)
    return stock.info, stock.financials, stock.balance_sheet


def get_row(df, names):
    for name in names:
        if name in df.index:
            return df.loc[name]
    return None


def calculate_ratios(info, financials, balance_sheet):
    rows = []

    # ---------------- Market ratios ----------------
    pe = info.get("trailingPE", np.nan)
    pb = info.get("priceToBook", np.nan)

    rows += [
        ("P/E Ratio (2025)", pe),
        ("P/E Ratio (2024)", np.nan),
        ("P/E Ratio YoY Change", np.nan),
        ("P/B Ratio (2025)", pb),
        ("P/B Ratio (2024)", np.nan),
        ("P/B Ratio YoY Change", np.nan),
    ]

    # ---------------- Financial statement rows ----------------
    net_income = get_row(financials, ["Net Income", "NetIncome"])
    revenue = get_row(financials, ["Total Revenue", "Revenue"])
    total_assets = get_row(balance_sheet, ["Total Assets"])
    total_liab = get_row(balance_sheet, ["Total Liab", "Total Liabilities"])
    equity = get_row(
        balance_sheet,
        ["Total Stockholder Equity", "Total Equity", "Stockholders Equity"],
    )
    current_assets = get_row(
        balance_sheet,
        ["Total Current Assets", "Current Assets"]
    )
    current_liab = get_row(
        balance_sheet,
        ["Total Current Liabilities", "Current Liabilities"]
    )

    if all(x is not None for x in [net_income, revenue, total_assets, total_liab]):
        if equity is None:
            equity = total_assets - total_liab

        # ---- Net Profit Margin ----
        npm_25 = (net_income.iloc[0] / revenue.iloc[0]) * 100
        npm_24 = (net_income.iloc[1] / revenue.iloc[1]) * 100

        rows += [
            ("Net Profit Margin (%) (2025)", npm_25),
            ("Net Profit Margin (%) (2024)", npm_24),
            ("Net Profit Margin YoY Change", npm_25 - npm_24),
        ]

        # --- ROA ---
        roa_25 = (net_income.iloc[0] / total_assets.iloc[0]) * 100
        roa_24 = (net_income.iloc[1] / total_assets.iloc[1]) * 100

        rows += [
            ("Return on Assets (%) (2025)", roa_25),
            ("Return on Assets (%) (2024)", roa_24),
            ("ROA YoY Change", roa_25 - roa_24),
        ]

        # ---- ROE ----
        roe_25 = (net_income.iloc[0] / equity.iloc[0]) * 100
        roe_24 = (net_income.iloc[1] / equity.iloc[1]) * 100

        rows += [
            ("Return on Equity (%) (2025)", roe_25),
            ("Return on Equity (%) (2024)", roe_24),
            ("ROE YoY Change", roe_25 - roe_24),
        ]

        # ---- Debt to Equity ----
        dte_25 = total_liab.iloc[0] / equity.iloc[0]
        dte_24 = total_liab.iloc[1] / equity.iloc[1]

        rows += [
            ("Debt to Equity (2025)", dte_25),
            ("Debt to Equity (2024)", dte_24),
            ("Debt to Equity YoY Change", dte_25 - dte_24),
        ]

    if current_assets is not None and current_liab is not None:
        cr_25 = current_assets.iloc[0] / current_liab.iloc[0]
        cr_24 = current_assets.iloc[1] / current_liab.iloc[1]

        rows += [
            ("Current Ratio (2025)", cr_25),
            ("Current Ratio (2024)", cr_24),
            ("Current Ratio YoY Change", cr_25 - cr_24),
        ]

    return pd.DataFrame(rows, columns=["Metric", "Value"])