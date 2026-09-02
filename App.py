import os
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from groq import Groq

# Page configuration
st.set_page_config(page_title="Trading Terminal & AI Assistant", layout="wide")

st.title("📈 Trading Terminal & AI Assistant")

# Initialize Groq Client safely (supports local environment variables and Streamlit/Hugging Face secrets)
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        api_key = None

# Create tabs for layout
tab_dashboard, tab_ai = st.tabs(["📊 Market Dashboard", "🤖 AI Assistant"])

with tab_dashboard:
    st.header("Market Data & Charts")
    ticker_symbol = st.text_input("Enter Ticker Symbol (e.g., AAPL, TSLA, BTC-USD):", "AAPL")
    
    if ticker_symbol:
        try:
            data = yf.download(ticker_symbol, period="1mo")
            if not data.empty:
                st.subheader(f"Recent Data for {ticker_symbol.upper()}")
                st.dataframe(data.tail())
                
                # Plotly Chart
                fig = px.line(data, y="Close", title=f"{ticker_symbol.upper()} Closing Prices")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No data found for this ticker.")
        except Exception as e:
            st.error(f"Error fetching data: {e}")

with tab_ai:
    st.header("Groq-Powered AI Assistant")
    
    system_context = "You are a professional financial trading assistant. Provide clear, concise, and accurate financial and technical insights."
    
    prompt = st.text_area("Ask the AI a question about trading, stocks, or your portfolio:", "What are the key technical indicators to watch for momentum trading?")
    
    if st.button("Generate Response"):
        if not api_key:
            st.error("Groq API Key not found! Please set it in your environment variables or Hugging Face/Streamlit Secrets.")
        elif not prompt.strip():
            st.warning("Please enter a prompt.")
        else:
            with st.spinner("Thinking... (Powered by Groq)"):
                try:
                    client = Groq(api_key=api_key)
                    completion = client.chat.completions.create(
                        model="llama3-8b-8192",
                        messages=[
                            {"role": "system", "content": system_context},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.7,
                    )
                    response_text = completion.choices[0].message.content
                    st.markdown("### Response:")
                    st.write(response_text)
                except Exception as e:
                    st.error(f"Error generating AI response: {e}")