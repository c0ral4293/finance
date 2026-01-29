import yfinance as yf
import pandas as pd

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)

def key_items():
    names = {
        "current_assets": ["Total Current Assets", "Current Assets", "Total Current Asset"],
        "current_liab": ["Total Current Liabilities", "Current Liabilities", "Total Current Liability"],
        "total_liab": ["Total Liabilities Net Minority Interest", "Total Liabilities"],
        "equity": ["Stockholders Equity", "Total Stockholders Equity", "Total Equity", "Common Stock Equity"],
        "revenue": ["Total Revenue", "Net Sales", "Net Revenue", "Revenue"],
        "net_income": ["Net Income", "Net Income Common Stockholders", "Net Income From Continuing Ops", "Net Earnings", "Net Profit"],
        "average_assets": ["Total Assets", "Total Combined Assets", "Net Assets", "Total Assets Net Minority Interest"],
        "average_inventory": ["Inventory", "Total Inventory", "Finished Goods", "Work In Process", "Raw Materials", "Inventories"],
        "cost_of_revenue": ["Cost Of Revenue", "Cost Of Goods Sold", "Cost Of Sales", "COGS", "Cost Of Services"],
        "operating_revenue": ["Operating Revenue", "Total Operating Profit"],
        "operating_expenses": ["Operating Expense", "Total Operating Expenses", "Operating Expenses"],
        "interest_expense": ["Interest Expense", "Interest Expense Non Operating", "Total Interest Expense"],
        "tax_provision": ["Tax Provision", "Provision For Income Tax", "Income Tax Expense"]
    }
    return list(names.keys()), list(names.values())


def data(df, items):
    for i in items:
        if i in df.index:
            return df.loc[i].iloc[0], df.loc[i].iloc[1]
    return None, None


def averagecalculations(key, df, items):
    a = b = c = 0
    for i in items:
        if i in df.index:
            a += df.loc[i].iloc[0]
            b += df.loc[i].iloc[1]
            c += df.loc[i].iloc[2]
    return (a + b) / 2, (b + c) / 2


# ✅ ONLY CHANGE: wrap everything into a function
def calculate_all_ratios(ticker_object):
    ticker = yf.Ticker(ticker_object)
    bs = ticker.balance_sheet
    financials = ticker.financials

    keys, items = key_items()
    dic2024, dic2025 = {}, {}

    for i in range(len(keys)):
        key = keys[i]
        if key in ["current_assets", "current_liab", "total_liab", "equity"]:
            a, b = data(bs, items[i])
            dic2024[key] = a
            dic2025[key] = b

        elif key in ["average_assets", "average_inventory"]:
            a, b = averagecalculations(key, bs, items[i])
            dic2024[key] = a
            dic2025[key] = b

        else:
            a, b = data(financials, items[i])
            dic2024[key] = a
            dic2025[key] = b

    ratios = {
        "Current Ratio 2024": dic2024["current_assets"] / dic2024["current_liab"],
        "Current Ratio 2025": dic2025["current_assets"] / dic2025["current_liab"],
        "Debt to Equity 2024": dic2024["total_liab"] / dic2024["equity"],
        "Debt to Equity 2025": dic2025["total_liab"] / dic2025["equity"],
        "Net Profit Margin 2024": dic2024["net_income"] / dic2024["revenue"],
        "Net Profit Margin 2025": dic2025["net_income"] / dic2025["revenue"],
    }

    return pd.DataFrame(ratios.items(), columns=["Metric", "Value"])