import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Price Tracker Dashboard", layout="wide")

st.title("📊 Amazon Price Tracker Dashboard")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("price_data.csv")
        df["Date"] = pd.to_datetime(df["Date"])
        return df
    except:
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("⚠️ No data available. Run price_tracker.py first.")
else:
    st.sidebar.header("🔍 Filters")
    products = df["Product"].unique()
    selected_product = st.sidebar.selectbox("Select Product", products)

    filtered_df = df[df["Product"] == selected_product]

    st.subheader(f"📦 {selected_product}")

    col1, col2, col3 = st.columns(3)

    col1.metric("📉 Min Price", f"₹{filtered_df['Price'].min():,.0f}")
    col2.metric("📈 Max Price", f"₹{filtered_df['Price'].max():,.0f}")
    col3.metric("📊 Avg Price", f"₹{filtered_df['Price'].mean():,.0f}")

    st.subheader("📈 Price Trend")

    fig, ax = plt.subplots()
    ax.plot(filtered_df["Date"], filtered_df["Price"], marker='o')
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.set_title("Price Over Time")
    plt.xticks(rotation=45)

    st.pyplot(fig)

    st.subheader("📄 Data Table")
    st.dataframe(filtered_df.sort_values("Date", ascending=False))
