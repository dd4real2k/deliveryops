import os
import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="DeliveryOps Intelligence", layout="centered")

st.title("🚚 DeliveryOps Intelligence System")
st.caption("Predict delivery time and delay risk using operational + location + time features.")

if not (os.path.exists("delivery_time_model.joblib") and os.path.exists("delay_risk_model.joblib")):
    st.warning("Models not found. Please run `notebooks/02_model.ipynb` to generate the .joblib files in the app/ folder.")
    st.stop()


st.markdown("""
**Inputs:** distance, traffic, weather, vehicle, area, category, agent rating, order time, pickup delay  
**Outputs:** predicted delivery time (minutes) + delay risk (%)
""")

reg_model = joblib.load("delivery_time_model.joblib")
clf_model = joblib.load("delay_risk_model.joblib")
