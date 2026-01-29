import yfinance as yf
import pandas as pd
pd.set_option("display.max_rows",None)
pd.set_option("display.max_columns",None)
def key_items():
    names={"current_assets":["Total Current Assets", "Current Assets", "Total Current Asset"],"current_liab": ["Total Current Liabilities", "Current Liabilities", "Total Current Liability"],"total_liab": ["Total Liabilities Net Minority Interest", "Total Liabilities"],"equity": ["Stockholders Equity", "Total Stockholders Equity", "Total Equity", "Common Stock Equity"],"revenue": ["Total Revenue", "Net Sales","Net Revenue","Revenue"],"net_income": ["Net Income", "Net Income Common Stockholders", "Net Income From Continuing Ops","Net Earnings","Net Profit"],"average_assets":["Total Assets", "Total Combined Assets", "Net Assets", "Total Assets Net Minority Interest"],"average_inventory":["Inventory","Total Inventory","Finished Goods","Work In Process","Raw Materials","Inventories"],"cost_of_revenue":["Cost Of Revenue","Cost Of Goods Sold","Cost Of Sales","COGS","Cost Of Services"],"operating_revenue":["Operating Revenue","Total Operating Profit"],"operating_expenses": ["Operating Expense","Total Operating Expenses","Operating Expenses"],"interest_expense": ["Interest Expense","Interest Expense Non Operating","Total Interest Expense"],"tax_provision": ["Tax Provision","Provision For Income Tax","Income Tax Expense"]}
    key=[]
    items=[]
    for i,j in names.items():
        key.append(i)
        items.append(j)
    return (key,items)
def data(df,items):
    for i in items:
        if i in df.index:
            wow=df.loc[i].iloc[0]
            wow1=df.loc[i].iloc[1]
    return(wow,wow1)
def averagecalculations(key,df,items):
    a,b,c=0,0,0
    for i in items:
        if key!="average_inventory":
            if i in df.index:
                a=df.loc[i].iloc[0]
                b=df.loc[i].iloc[1]
                c=df.loc[i].iloc[2]
        if key=="average_inventory":
            if i in df.index:
                a+=df.loc[i].iloc[0]
                b+=df.loc[i].iloc[1]
                c+=df.loc[i].iloc[2]
    ava25=(a+b)/2
    ava24=(b+c)/2
    return(ava25,ava24)
ticker_object=input("Enter ticker object")
ticker=yf.Ticker(ticker_object)
bs=ticker.balance_sheet
financials=ticker.financials
(a,b)=key_items()
key=a
items=b
dic2024=dict()
dic2025=dict()
for i in range(len(key)):
    if key[i]in ["current_assets", "current_liab", "total_liab", "equity",]:
        tup=data(bs,items[i])
        dic2024[key[i]]=tup[0]
        dic2025[key[i]]=tup[1]
    elif key[i] in ["average_assets","average_inventory"]:
        tup1=averagecalculations(key[i],bs,items[i])
        dic2024[key[i]]=tup1[0]
        dic2025[key[i]]=tup1[1]
    elif key[i] in ["revenue", "net_income","cost_of_revenue","tax_provision","interest_expense","operating_expenses","operating_revenue"]:
        tup2=data(financials,items[i])
        dic2024[key[i]]=tup2[0]
        dic2025[key[i]]=tup2[1]
ratio1=[float(dic2024['current_assets']/dic2024['current_liab']),float(dic2025['current_assets']/dic2025['current_liab'])] #Current Ratio
ratio2=[float((dic2024['current_assets']-dic2024['current_liab'])),float((dic2025['current_assets']-dic2025['current_liab']))]#Working Capital
ratio3=[float(dic2024['total_liab']/dic2024['equity']),float(dic2025['total_liab']/dic2025['equity'])]#Debt-to-Equity Ratio
ratio4=[float(dic2024['net_income']/dic2024['revenue']),float(dic2025['net_income']/dic2025['revenue'])]#Net Profit Ratio
ratio5=[float(dic2024['net_income']/dic2024['equity']),float(dic2025['net_income']/dic2025['equity'])]#Return on Investment Ratio
ratio6=[float(dic2024["revenue"]/dic2024["average_assets"]),float(dic2025["revenue"]/dic2025["average_assets"])]#Asset Turnover Ratio
ratio7=[float(dic2024["cost_of_revenue"]/dic2024["average_inventory"]),float(dic2025["cost_of_revenue"]/dic2025["average_inventory"])]#Inventory Turnover Ratio
ratio8=[float((dic2024["operating_revenue"]-dic2024["operating_expenses"])/dic2024["operating_revenue"]),float((dic2024["operating_revenue"]-dic2024["operating_expenses"])/dic2024["operating_revenue"])]#Operating Margin
ratio9=[float((dic2024["revenue"]-dic2024["cost_of_revenue"])/dic2024['revenue']),float((dic2025["revenue"]-dic2025["cost_of_revenue"])/dic2025['revenue'])]#Gross Profit Margin
ratio10=[float(dic2024["net_income"]/dic2024["average_assets"]),float(dic2025["net_income"]/dic2025["average_assets"])]#Return on Assets Ratio

print("2024","      \t","     2025")
print(ratio1[0]," ",ratio1[1])
print(ratio2[0]," ",ratio2[1])#This is just for basic back end presentation, to be removed later. 
print(ratio3[0]," ",ratio3[1])
print(ratio4[0]," ",ratio4[1])
print(ratio5[0]," ",ratio5[1])
print(ratio6[0]," ",ratio6[1])
print(ratio7[0]," ",ratio7[1])
#Ratios that are requiered 
def get_ratios(ticker_object):
    import yfinance as yf

    ticker = yf.Ticker(ticker_object)
    bs = ticker.balance_sheet
    financials = ticker.financials

    (a, b) = key_items()
    key = a
    items = b

    dic2024 = {}
    dic2025 = {}

    for i in range(len(key)):
        if key[i] in ["current_assets", "current_liab", "total_liab", "equity"]:
            tup = data(bs, items[i])
            dic2025[key[i]] = tup[0]
            dic2024[key[i]] = tup[1]

        elif key[i] in ["average_assets", "average_inventory"]:
            tup1 = averagecalculations(key[i], bs, items[i])
            dic2025[key[i]] = tup1[0]
            dic2024[key[i]] = tup1[1]

        elif key[i] in ["revenue", "net_income", "cost_of_revenue",
                        "tax_provision", "interest_expense",
                        "operating_expenses", "operating_revenue"]:
            tup2 = data(financials, items[i])
            dic2025[key[i]] = tup2[0]
            dic2024[key[i]] = tup2[1]

    ratios = {
        "Current Ratio": (
            dic2025["current_assets"] / dic2025["current_liab"],
            dic2024["current_assets"] / dic2024["current_liab"]
        ),
        "Working Capital": (
            dic2025["current_assets"] - dic2025["current_liab"],
            dic2024["current_assets"] - dic2024["current_liab"]
        ),
        "Debt to Equity": (
            dic2025["total_liab"] / dic2025["equity"],
            dic2024["total_liab"] / dic2024["equity"]
        ),
        "Net Profit Margin": (
            dic2025["net_income"] / dic2025["revenue"],
            dic2024["net_income"] / dic2024["revenue"]
        ),
        "Return on Equity": (
            dic2025["net_income"] / dic2025["equity"],
            dic2024["net_income"] / dic2024["equity"]
        ),
        "Asset Turnover": (
            dic2025["revenue"] / dic2025["average_assets"],
            dic2024["revenue"] / dic2024["average_assets"]
        ),
        "Inventory Turnover": (
            dic2025["cost_of_revenue"] / dic2025["average_inventory"],
            dic2024["cost_of_revenue"] / dic2024["average_inventory"]
        ),
        "Gross Profit Margin": (
            (dic2025["revenue"] - dic2025["cost_of_revenue"]) / dic2025["revenue"],
            (dic2024["revenue"] - dic2024["cost_of_revenue"]) / dic2024["revenue"]
        ),
    }

    df = pd.DataFrame(
        [
            [k, v[0], v[1], v[0] - v[1]]
            for k, v in ratios.items()
        ],
        columns=["Metric", "2025", "2024", "YoY Change"]
    )

    return df 
