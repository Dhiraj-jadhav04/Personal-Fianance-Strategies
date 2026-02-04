import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Wealth Strategist", layout="wide")

st.title("💸 Personal Finance Strategist")
st.markdown("Predict your future wealth using market simulations.")

# --- SIDEBAR INPUTS ---
with st.sidebar:
    st.header("1. Your Details")
    initial_inv = st.number_input("Starting Capital ($)", value=5000)
    monthly_dep = st.number_input("Monthly Deposit ($)", value=500)
    
    st.header("2. Strategy")
    years = st.slider("Investment Duration (Years)", 1, 40, 20)
    return_rate = st.slider("Expected Annual Return (%)", 1.0, 15.0, 8.0)
    volatility = st.slider("Market Volatility (%)", 0.0, 25.0, 12.0)

# --- MATH LOGIC ---
months = years * 12
monthly_avg_return = (return_rate / 100) / 12
monthly_volatility = (volatility / 100) / np.sqrt(12)

# Simple Growth Calculation
balances = [initial_inv]
for _ in range(months):
    next_val = (balances[-1] + monthly_dep) * (1 + monthly_avg_return)
    balances.append(next_val)

# --- DISPLAY METRICS ---
final_val = balances[-1]
total_invested = initial_inv + (monthly_dep * months)
interest_earned = final_val - total_invested

col1, col2, col3 = st.columns(3)
col1.metric("Projected Wealth", f"${final_val:,.0f}")
col2.metric("Total Deposits", f"${total_invested:,.0f}")
col3.metric("Profit from Growth", f"${interest_earned:,.0f}")

# --- VISUALIZATION ---
df = pd.DataFrame({"Month": range(len(balances)), "Balance": balances})
fig = go.Figure()
fig.add_trace(go.Scatter(x=df["Month"], y=df["Balance"], mode='lines', name='Total Value', fill='tozeroy'))

fig.update_layout(title="Wealth Growth Over Time", xaxis_title="Months", yaxis_title="Balance ($)")
st.plotly_chart(fig, use_container_width=True)

st.success("Pro Tip: Try increasing your Monthly Deposit by just $100 to see the massive impact of compounding!")