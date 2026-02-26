import streamlit as st
import pandas as pd
import joblib
import os

st.set_page_config(page_title="DeliveryOps Intelligence", layout="centered")

st.title("🚚 DeliveryOps Intelligence System")
st.caption("Predict delivery time and delay risk")

# Check models exist
if not os.path.exists("delivery_time_model.joblib") or not os.path.exists("delay_risk_model.joblib"):
    st.warning("⚠️ Run the notebook (02_model.ipynb) to generate model files.")
    st.stop()

# Load models
reg_model = joblib.load("delivery_time_model.joblib")
clf_model = joblib.load("delay_risk_model.joblib")

# Inputs
st.header("Enter Delivery Details")

distance_km = st.slider("Distance (km)", 0.0, 50.0, 5.0)
agent_rating = st.slider("Agent Rating", 0.0, 5.0, 4.5)
order_hour = st.slider("Order Hour", 0, 23, 12)
day_of_week = st.selectbox("Day of Week", list(range(7)))
pickup_delay = st.slider("Pickup Delay (minutes)", 0.0, 120.0, 10.0)

traffic = st.selectbox("Traffic", ["Low", "Medium", "High"])
weather = st.selectbox("Weather", ["Clear", "Rainy", "Foggy"])
vehicle = st.selectbox("Vehicle", ["Bike", "Car", "Scooter"])
area = st.text_input("Area", "Urban")
category = st.text_input("Category", "Food")

# Create dataframe
X = pd.DataFrame([{
    "distance_km": distance_km,
    "agent_rating": agent_rating,
    "order_hour": order_hour,
    "day_of_week": day_of_week,
    "pickup_delay": pickup_delay,
    "traffic": traffic,
    "weather": weather,
    "vehicle": vehicle,
    "area": area,
    "category": category
}])

# Predict
time_pred = reg_model.predict(X)[0]
risk = clf_model.predict_proba(X)[0, 1]

# Output
st.header("Predictions")

st.metric("Delivery Time (minutes)", f"{time_pred:.1f}")
st.metric("Delay Risk", f"{risk*100:.1f}%")
