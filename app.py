import streamlit as st
import yfinance as yf
import plotly.express as px

st.title("India Macro Dashboard")

# Label shown to user -> ticker symbol Yahoo Finance understands
options = {"USD/INR": "INR=X", "Nifty 50": "^NSEI", "Sensex": "^BSESN"}
choice = st.sidebar.selectbox("Pick an indicator", list(options))

@st.cache_data(ttl=3600)  # remember results for an hour so it loads fast
def load(ticker):
    df = yf.download(ticker, period="2y", auto_adjust=True)
    df.columns = df.columns.get_level_values(0)
    return df.reset_index()

df = load(options[choice])

st.plotly_chart(px.line(df, x="Date", y="Close", title=choice),
                use_container_width=True)

latest = df["Close"].iloc[-1]
month_ago = df["Close"].iloc[-22]  # ~22 trading days = 1 month
st.metric(choice, f"{latest:,.2f}",
          f"{(latest / month_ago - 1) * 100:.2f}% vs 1 month ago")
