import yfinance as yf
import math
ticker_object=input("enter Company's Ticker to see Analysis:")
ticker=yf.Ticker(ticker_object)
df=ticker.history(period="2y")
def top_company():
    finder_US={
    "technology": "XLK",
    "financial Services": "XLF",
    "healthcare": "XLV",
    "energy": "XLE",
    "consumer Defensive": "XLP",
    "consumer Cyclical": "XLY",
    "industrials": "XLI",
    "utilities": "XLU",
    "materials": "XLB",
    "real-estate": "XLRE",
    "communication Services": "XLC"}
    info=ticker.info
    sector=info['sectorKey']
    ETF=""
    comlst=[]
    if sector in finder_US:
        ETF=finder_US[sector]
    else:
        print("The sector is not included")
    if ETF!="":
        et=yf.Ticker(ETF)   
        top_company=et.funds_data.top_holdings
        for i in range(10):
            symbol=top_company.index[i]
            comlst.append(symbol)
    else:
        print("Error in Function top_company()")
    return comlst
def history(df):
    t2024=df.loc["2024"].iloc[-1].iloc[3]
    t2025=df.loc["2025"].iloc[-1].iloc[3]
    return([t2024,t2025])
def key_items():
    names={"current_assets":["Total Current Assets", "Current Assets", "Total Current Asset"],"current_liab": ["Total Current Liabilities", "Current Liabilities", "Total Current Liability"],"total_liab": ["Total Liabilities Net Minority Interest", "Total Liabilities"],"equity": ["Stockholders Equity", "Total Stockholders Equity", "Total Equity", "Common Stock Equity"],"revenue": ["Total Revenue", "Net Sales","Net Revenue","Revenue"],"net_income": ["Net Income", "Net Income Common Stockholders", "Net Income From Continuing Ops","Net Earnings","Net Profit"],"average_assets":["Total Assets", "Total Combined Assets", "Net Assets", "Total Assets Net Minority Interest"],"average_inventory":["Inventory","Total Inventory","Finished Goods","Work In Process","Raw Materials","Inventories"],"cost_of_revenue":["Cost Of Revenue","Cost Of Goods Sold","Cost Of Sales","COGS","Cost Of Services"],"operating_revenue":["Operating Revenue","Total Operating Profit"],"operating_expenses": ["Operating Expense","Total Operating Expenses","Operating Expenses"],"interest_expense": ["Interest Expense","Interest Expense Non Operating","Total Interest Expense"],"tax_provision": ["Tax Provision","Provision For Income Tax","Income Tax Expense"],"Earningpershare":["Basic EPS","Diluted EPS","BasicEPS","DilutedEPS","trailingEps","forwardEps","Earnings Per Share","EPS Basic","EPS Diluted"]}
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
def comp_ratio(a):
    avg=[]
    for i in a:
        dic2024=dict()
        dic2025=dict()
        ticker1=yf.Ticker(i)
        bs=ticker1.balance_sheet
        financials=ticker1.financials
        hist=ticker1.history(period="2y")
        #hist=ticker1.history(period="2y")
        (key,items)=key_items()
        key=key
        items=items
        for i in range(len(key)):
            if key[i]in ["current_assets", "current_liab", "total_liab", "equity"]:
                tup=data(bs,items[i])
                dic2024[key[i]]=tup[0]
                dic2025[key[i]]=tup[1]
            elif key[i] in ["average_assets","average_inventory"]:
                tup1=averagecalculations(key[i],bs,items[i])
                dic2024[key[i]]=tup1[0]
                dic2025[key[i]]=tup1[1]
            elif key[i] in ["revenue", "net_income","cost_of_revenue","tax_provision","interest_expense","operating_expenses","operating_revenue","Earningpershare"]:
                tup2=data(financials,items[i])
                dic2024[key[i]]=tup2[0]
                dic2025[key[i]]=tup2[1]
            ob=history(hist)        
        # Check both years for zero or nan before calculating the ratio
        if float(dic2024['current_liab'])!=0 and str(dic2024['current_liab'])!='nan':
            ratio12024=float(dic2024['current_assets']/dic2024['current_liab'])
        else:
            ratio12024=0
        if float(dic2025['current_liab'])!=0 and str(dic2025['current_liab'])!='nan':
            ratio12025=float(dic2025['current_assets']/dic2025['current_liab'])
        else:
            ratio12025=0
        ratio1=[ratio12024,ratio12025] #Current Ratio
        ratio2=[float((dic2024['current_assets']-dic2024['current_liab'])),float((dic2025['current_assets']-dic2025['current_liab']))]#Working Capital
        if float(dic2024['equity'])!=0 and str(dic2024['equity'])!='nan':
            ratio32024=float(dic2024['total_liab']/dic2024['equity'])
        else:
            ratio32024=0
        if float(dic2025['equity'])!=0 and str(dic2025['equity'])!='nan':
            ratio32025=float(dic2025['total_liab']/dic2025['equity'])
        else:
            ratio32025=0
        ratio3=[ratio32024,ratio32025]#Debt-to-Equity Ratio
        if float(dic2024['revenue'])!=0 and str(dic2024['revenue'])!='nan':
            ratio42024=float(dic2024['net_income']/dic2024['revenue'])
        else:
            ratio42024=0
        if float(dic2025['revenue'])!=0 and str(dic2025['revenue'])!='nan':
            ratio42025=float(dic2025['net_income']/dic2025['revenue'])
        else:
            ratio42025=0
        ratio4=[ratio42024,ratio42025]#Net Profit Ratio
        if float(dic2024['equity'])!=0 and str(dic2024['equity'])!='nan':
            ratio52024=float(dic2024['net_income']/dic2024['equity'])
        else:
            ratio52024=0
        if float(dic2025['equity'])!=0 and str(dic2025['equity'])!='nan':
            ratio52025=float(dic2025['net_income']/dic2025['equity'])
        else:
            ratio52025=0
        ratio5=[ratio52024,ratio52025] #Investment Turnover Ratio
        if float(dic2024['average_assets'])!=0 and str(dic2024['average_assets'])!='nan':
            ratio62024=float(dic2024["revenue"]/dic2024["average_assets"])
        else:
            ratio62024=0
        if float(dic2025['average_assets'])!=0 and str(dic2025['average_assets'])!='nan':
            ratio62025=float(dic2025["revenue"]/dic2025["average_assets"])#Asset Turnover Ratio
        else:
            ratio62025=0
        ratio6=[ratio62024,ratio62025]
        if float(dic2024["average_inventory"])!=0 and str(dic2024["average_inventory"])!='nan':
            ratio72024=float(dic2024["cost_of_revenue"]/dic2024["average_inventory"])
        else:
            ratio72024=0
        if float(dic2025["average_inventory"])!=0 and str(dic2025["average_inventory"])!='nan':
            ratio72025=float(dic2025["cost_of_revenue"]/dic2025["average_inventory"])
        else:
            rayio72025=0
        ratio7=[ratio72024,ratio72025]#Inventory Turnover Ratio
        if float(dic2024["operating_revenue"])!=0 and str(dic2024["operating_revenue"])!='nan':
            ratio82024=float((dic2024["operating_revenue"]-dic2024["operating_expenses"])/dic2024["operating_revenue"])
        else:
            ratio82024=0
        if float(dic2025["operating_revenue"])!=0 and str(dic2025["operating_revenue"])!='nan':
            ratio82025=float((dic2024["operating_revenue"]-dic2024["operating_expenses"])/dic2024["operating_revenue"])
        else:
            ratio82025=0
        ratio8=[ratio82024,ratio82025] #Operating Ratio
        if float(dic2024['revenue'])!=0 and str(dic2024['revenue'])!='nan':
            ratio92024=float((dic2024["revenue"]-dic2024["cost_of_revenue"])/dic2024['revenue'])
        if float(dic2025['revenue'])!=0 and str(dic2025['revenue'])!='nan':
            ratio92025=float((dic2025["revenue"]-dic2025["cost_of_revenue"])/dic2025['revenue'])
        else:
            ratio92025=0
        ratio9=[ratio92024,ratio92025]#Gross Profit Margin
        if float(dic2024["average_assets"])!=0 and str(dic2024["average_assets"])!='nan':
            ratio102024=float(dic2024["net_income"]/dic2024["average_assets"])
        else:
            ratio102024=0
        if float(dic2025["average_assets"])!=0 and str(dic2025["average_assets"])!='nan':
            ratio102025=float(dic2025["net_income"]/dic2025["average_assets"])#Return on Assets Ratio
        else:
            ratio102025=0
        ratio10=[ratio102024,ratio102025]
        if float(dic2024["Earningpershare"])!=0 and str(dic2024["Earningpershare"])!='nan':
            ratio112024=float(ob[0]/dic2024["Earningpershare"])
        else:
            ratio112024=0
        if float(dic2025["Earningpershare"])!=0 and str(dic2025["Earningpershare"])!='nan':
            ratio112025=float(ob[1]/dic2025["Earningpershare"]) #P/E Ratio
        else:
            ratio112025=0
        ratio11=[ratio112024,ratio112025]
        avg.append([ratio1,ratio2,ratio3,ratio4,ratio5,ratio6,ratio7,ratio8,ratio9,ratio10,ratio11])
    mainlst=[[],[],[],[],[],[],[],[],[],[],[]]
    for k in avg:
        for n in range(11):
            mainlst[n].append(k[n])
    ohmygwad=[]
    for m in range(11):
        sum2024=0 
        sum2025=0
        ele=mainlst[m]
        count2024=0
        count2025=0
        for o in ele: #[[2024,2025],[2024,2025],[2024,2025]]                #There might be logical error, other than that the code should work
            if isinstance(o[0], (int,float)) and not math.isnan(o[0]):
                sum2024+=o[0]
                count2024+=1
            if isinstance(o[1], (int,float)) and not math.isnan(o[1]):
                sum2025+=o[1]
                count2025+=1
        avg2024=sum2024/count2024 if count2024 >0 else 0
        avg2025=sum2025/count2025 if count2025>0 else 0
        ohmygwad.append([avg2024,avg2025])
    return ohmygwad
def original_company(a):
    dic2024=dict()
    dic2025=dict()
    ticker2=yf.Ticker(a)
    bs=ticker2.balance_sheet
    financials=ticker2.financials
    hist=ticker.history(period="2y")
    (key,items)=key_items()
    key=key
    items=items
    finallst=[]
    for i in range(len(key)):
        if key[i]in ["current_assets", "current_liab", "total_liab", "equity"]:
            tup=data(bs,items[i])
            dic2024[key[i]]=tup[0]
            dic2025[key[i]]=tup[1]
        elif key[i] in ["average_assets","average_inventory"]:
            tup1=averagecalculations(key[i],bs,items[i])
            dic2024[key[i]]=tup1[0]
            dic2025[key[i]]=tup1[1]
        elif key[i] in ["revenue", "net_income","cost_of_revenue","tax_provision","interest_expense","operating_expenses","operating_revenue","Earningpershare"]:
            tup2=data(financials,items[i])
            dic2024[key[i]]=tup2[0]
            dic2025[key[i]]=tup2[1]
        ob=history(hist)
    # Check both years for zero or nan before calculating the ratio
    if float(dic2024['current_liab'])!=0 and str(dic2024['current_liab'])!='nan':
        ratio12024=float(dic2024['current_assets']/dic2024['current_liab'])
    else:
        ratio12024=0
    if float(dic2025['current_liab'])!=0 and str(dic2025['current_liab'])!='nan':
        ratio12025=float(dic2025['current_assets']/dic2025['current_liab'])
    else:
        ratio12025=0
    ratio1=[ratio12024,ratio12025] #Current Ratio
    if float(dic2024['current_liab'])!=0 and str(dic2024['current_liab'])!='nan':
        ratio22024=float(dic2024['current_assets']/dic2024['current_liab'])
    else:
        ratio22024=0
    if float(dic2025['current_liab'])!=0 and str(dic2025['current_liab'])!='nan':
        ratio22025=float(dic2025['current_assets']/dic2025['current_liab'])#Working Capital Ratio
    else:
        ratio22025=0
    ratio22025=0
    ratio2=[ratio12025,ratio22025]
    if float(dic2024['equity'])!=0 and str(dic2024['equity'])!='nan':
         ratio32024=float(dic2024['total_liab']/dic2024['equity'])
    else:
        ratio32024=0
    if float(dic2025['equity'])!=0 and str(dic2025['equity'])!='nan':
        ratio32025=float(dic2025['total_liab']/dic2025['equity'])
    else:
        ratio32025=0
    ratio3=[ratio32024,ratio32025]#Debt-to-Equity Ratio
    if float(dic2024['revenue'])!=0 and str(dic2024['revenue'])!='nan':
        ratio42024=float(dic2024['net_income']/dic2024['revenue'])
    else:
        ratio42024=0
    if float(dic2025['revenue'])!=0 and str(dic2025['revenue'])!='nan':
        ratio42025=float(dic2025['net_income']/dic2025['revenue'])
    else:
        ratio42025=0
    ratio4=[ratio42024,ratio42025]#Net Profit Ratio
    if float(dic2024['equity'])!=0 and str(dic2024['equity'])!='nan':
        ratio52024=float(dic2024['net_income']/dic2024['equity'])
    else:
        ratio52024=0
    if float(dic2025['equity'])!=0 and str(dic2025['equity'])!='nan':
        ratio52025=float(dic2025['net_income']/dic2025['equity'])
    else:
        ratio52025=0
    ratio5=[ratio52024,ratio52025] #Investment Turnover Ratio
    if float(dic2024['average_assets'])!=0 and str(dic2024['average_assets'])!='nan':
        ratio62024=float(dic2024["revenue"]/dic2024["average_assets"])
    else:
        ratio62024=0
    if float(dic2025['average_assets'])!=0 and str(dic2025['average_assets'])!='nan':
        ratio62025=float(dic2025["revenue"]/dic2025["average_assets"])#Asset Turnover Ratio
    else:
        ratio62025=0
    ratio6=[ratio62024,ratio62025]
    if float(dic2024["average_inventory"])!=0 and str(dic2024["average_inventory"])!='nan':
        ratio72024=float(dic2024["cost_of_revenue"]/dic2024["average_inventory"])
    else:
        ratio72024=0
    if float(dic2025["average_inventory"])!=0 and str(dic2025["average_inventory"])!='nan':
        ratio72025=float(dic2025["cost_of_revenue"]/dic2025["average_inventory"])
    else:
        rayio72025=0
    ratio7=[ratio72024,ratio72025]#Inventory Turnover Ratio
    if float(dic2024["operating_revenue"])!=0 and str(dic2024["operating_revenue"])!='nan':
          ratio82024=float((dic2024["operating_revenue"]-dic2024["operating_expenses"])/dic2024["operating_revenue"])
    else:
        ratio82024=0
    if float(dic2025["operating_revenue"])!=0 and str(dic2025["operating_revenue"])!='nan':
        ratio82025=float((dic2024["operating_revenue"]-dic2024["operating_expenses"])/dic2024["operating_revenue"])
    else:
        ratio82025=0
    ratio8=[ratio82024,ratio82025] #Operating Ratio
    if float(dic2024['revenue'])!=0 and str(dic2024['revenue'])!='nan':
        ratio92024=float((dic2024["revenue"]-dic2024["cost_of_revenue"])/dic2024['revenue'])
    if float(dic2025['revenue'])!=0 and str(dic2025['revenue'])!='nan':
        ratio92025=float((dic2025["revenue"]-dic2025["cost_of_revenue"])/dic2025['revenue'])
    else:
        ratio92025=0
    ratio9=[ratio92024,ratio92025]#Gross Profit Margin
    if float(dic2024["average_assets"])!=0 and str(dic2024["average_assets"])!='nan':
        ratio102024=float(dic2024["net_income"]/dic2024["average_assets"])
    else:
        ratio102024=0
    if float(dic2025["average_assets"])!=0 and str(dic2025["average_assets"])!='nan':
        ratio102025=float(dic2025["net_income"]/dic2025["average_assets"])#Return on Assets Ratio
    else:
        ratio102025=0
    ratio10=[ratio102024,ratio102025]
    if float(dic2024["Earningpershare"])!=0 and str(dic2024["Earningpershare"])!='nan':
        ratio112024=float(ob[0]/dic2024["Earningpershare"])
    else:
        ratio112024=0
    if float(dic2025["Earningpershare"])!=0 and str(dic2025["Earningpershare"])!='nan':
        ratio112025=float(ob[1]/dic2025["Earningpershare"]) #P/E Ratio
    else:
        ratio112025=0
    ratio11=[ratio112024,ratio112025]
    finallst.append([ratio1,ratio2,ratio3,ratio4,ratio5,ratio6,ratio7,ratio8,ratio9,ratio10,ratio11])
    return finallst
listofcompanies=top_company()
comparision_lst=comp_ratio(listofcompanies)
original_lst=original_company(ticker_object)
print("Orginal Ratios")
for i in original_lst:
    print(i)
print("Competitors average")
for j in comparision_lst:
    print(j)