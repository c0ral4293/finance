import streamlit as st
from ratios import fetch_data, calculate_ratios

st.set_page_config(
    page_title="Financial Ratio Analyzer",
    layout="wide"
)

st.title("📊 Company Financial Health Analyzer")

ticker = st.text_input(
    "Enter company ticker (e.g. AAPL, MSFT, TSLA):"
)

if st.button("Analyze"):
    if ticker:
        try:
            with st.spinner("Fetching financial data..."):
                info, financials, balance_sheet = fetch_data(ticker.upper())
                ratios_df = calculate_ratios(info, financials, balance_sheet)

            st.subheader(f"Financial Ratios for {ticker.upper()}")
            st.dataframe(ratios_df, use_container_width=True)

            st.subheader("Company Overview")
            st.write(f"**Industry:** {info.get('industry', 'N/A')}")
            st.write(f"**Market Cap:** {info.get('marketCap', 'N/A')}")
            st.write(f"**Beta:** {info.get('beta', 'N/A')}")

        except Exception as e:
            st.error(f"Error fetching data: {e}")
    else:
        st.warning("Please enter a ticker symbol.")