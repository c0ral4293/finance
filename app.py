import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from ratios import calculate_ratios

st.title("📊 Financial Ratios Analyzer (.ns for indian tickers)")

ticker_symbol = st.text_input(
    "Enter Stock Ticker Symbol",
     placeholder="Here are some popular tickers: e.g., AAPL, MSFT, GOOGL, AMZN, TSLA, etc."
).upper()

if st.button("Analyze", type="primary"):
    try:
        with st.spinner(f"Fetching data for {ticker_symbol}..."):
            df = calculate_ratios(ticker_symbol)
        
        st.success(f"✅ Analysis complete for {ticker_symbol}")
        
        # Display the table
        st.subheader("Financial Ratios")
        st.dataframe(df, use_container_width=True)
        
        # Add metrics with arrows
        st.subheader("Key Insights")
        
        cols = st.columns(3)  # Create 3 columns for better layout
        
        for idx, (_, row) in enumerate(df.iterrows()):
            ratio_name = row["Ratio"]
            change = row["YoY Change"]
            
            with cols[idx % 3]:  # Distribute metrics across 3 columns
                st.metric(
                    label=ratio_name,
                    value=f"{row['2025']:.4f}",
                    delta=f"{change:.4f}"
                )
        
        # Add visualization
        st.subheader("📈 Year-over-Year Comparison")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        x = range(len(df))
        width = 0.35
        
        ax.bar([i - width/2 for i in x], df['2024'], width, label='2024', alpha=0.8)
        ax.bar([i + width/2 for i in x], df['2025'], width, label='2025', alpha=0.8)
        
        ax.set_xlabel('Ratios')
        ax.set_ylabel('Values')
        ax.set_title(f'{ticker_symbol} Financial Ratios Comparison')
        ax.set_xticks(x)
        ax.set_xticklabels(df['Ratio'], rotation=45, ha='right')
        ax.legend()
        
        plt.tight_layout()
        st.pyplot(fig)
        
    except ValueError as e:
        st.error(f"❌ {str(e)}")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")