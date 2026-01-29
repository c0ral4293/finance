import streamlit as st
import pandas as pd
from ratios import calculate_ratios

st.title("📊 Financial Ratios Analyzer (use .ns for indian companies)")

# Input section
ticker_symbol = st.text_input(
    "Enter Stock Ticker Symbol",
    value="AAPL",
    placeholder="Try some popular tickers: e.g., AAPL, MSFT, GOOGL, etc."
).upper()

if st.button("Analyze", type="primary"):
    try:
        with st.spinner(f"Fetching data for {ticker_symbol}..."):
            df = calculate_ratios(ticker_symbol)
        
        st.success(f"✅ Analysis complete for {ticker_symbol}")
        
        # Display the ratios table
        st.subheader("Financial Ratios")
        
        # Format the dataframe for better display
        styled_df = df.style.format({
            "2025": "{:.4f}",
            "2024": "{:.4f}",
            "YoY Change": "{:.4f}"
        })
        
        st.dataframe(styled_df, use_container_width=True)
        
        # Optional: Add some insights
        st.subheader("Key Insights")
        
        for _, row in df.iterrows():
            ratio_name = row["Ratio"]
            change = row["YoY Change"]
            
            if change > 0:
                st.metric(
                    label=ratio_name,
                    value=f"{row['2025']:.4f}",
                    delta=f"{change:.4f}"
                )
            elif change < 0:
                st.metric(
                    label=ratio_name,
                    value=f"{row['2025']:.4f}",
                    delta=f"{change:.4f}"
                )
        
    except ValueError as e:
        st.error(f"❌ {str(e)}")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.info("Please check if the ticker symbol is valid and try again.")
        
