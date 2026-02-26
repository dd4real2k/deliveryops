import os
import joblib
import pandas as pd
import streamlit as st

# ----------------------------
# Page config + basic styling
# ----------------------------
st.set_page_config(page_title="DeliveryOps Intelligence", page_icon="🚚", layout="wide")

st.markdown(
    """
    <style>
        .block-container { padding-top: 1.2rem; padding-bottom: 2rem; }
        .kpi { border-radius: 16px; padding: 18px 18px; border: 1px solid rgba(49, 51, 63, 0.2); }
        .kpi-title { font-size: 0.9rem; opacity: 0.75; margin-bottom: 6px; }
        .kpi-value { font-size: 1.8rem; font-weight: 700; }
        .muted { opacity: 0.75; }
        .card { border-radius: 16px; padding: 18px; border: 1px solid rgba(49, 51, 63, 0.2); }
        .small { font-size: 0.9rem; }
        .pill { display: inline-block; padding: 2px 10px; border-radius: 999px; border: 1px solid rgba(49, 51, 63, 0.25); }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------
# Helpers
# ----------------------------
def safe_unique(series):
    """Return sorted unique values as strings, ignoring NaNs."""
    if series is None:
        return []
    vals = series.dropna().astype(str).unique().tolist()
    return sorted(vals)

def load_dropdown_options():
    """
    Try to load dropdown options from cleaned dataset to ensure
    category values match training.
    """
    cleaned_path = os.path.join("..", "data", "cleaned", "cleaned_delivery.csv")
    if os.path.exists(cleaned_path):
        d = pd.read_csv(cleaned_path)
        return {
            "traffic": safe_unique(d.get("traffic")),
            "weather": safe_unique(d.get("weather")),
            "vehicle": safe_unique(d.get("vehicle")),
            "area": safe_unique(d.get("area")),
            "category": safe_unique(d.get("category")),
        }
    # fallback defaults (still fine for demo)
    return {
        "traffic": ["Low", "Medium", "High"],
        "weather": ["Clear", "Rainy", "Foggy"],
        "vehicle": ["Bike", "Car", "Scooter"],
        "area": ["Urban", "Suburban", "Rural"],
        "category": ["Food", "Grocery", "Pharmacy", "Electronics"],
    }

# ----------------------------
# Header
# ----------------------------
left, right = st.columns([0.72, 0.28], vertical_alignment="center")
with left:
    st.title("🚚 DeliveryOps Intelligence System")
    st.caption("Predict **delivery time** and **delay risk** using operational, location, and time features.")
with right:
    st.markdown(
        """
        <div class="card">
          <div class="small"><b>Status</b></div>
          <div class="muted small">Streamlit • ML Pipelines • Real-time inference</div>
          <div style="margin-top:10px;">
            <span class="pill">Regression</span>
            <span class="pill">Classification</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

# ----------------------------
# Model presence check
# ----------------------------
reg_path = "delivery_time_model.joblib"
clf_path = "delay_risk_model.joblib"

if not (os.path.exists(reg_path) and os.path.exists(clf_path)):
    st.warning(
        "⚠️ Model files not found in the `app/` folder.\n\n"
        "Run `notebooks/02_model.ipynb` to generate:\n"
        "- `app/delivery_time_model.joblib`\n"
        "- `app/delay_risk_model.joblib`\n\n"
        "Tip: These files are intentionally not pushed to GitHub if they exceed 100MB."
    )
    st.stop()

reg_model = joblib.load(reg_path)
clf_model = joblib.load(clf_path)

# ----------------------------
# Inputs (premium layout)
# ----------------------------
options = load_dropdown_options()

st.subheader("🧾 Inputs")

colA, colB, colC = st.columns([0.34, 0.33, 0.33], gap="large")

with colA:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("**Location & Distance**")
    distance_km = st.slider("Distance (km)", 0.0, 60.0, 5.0, 0.5)
    area = st.selectbox("Area", options["area"], index=0 if options["area"] else None)
    st.markdown("</div>", unsafe_allow_html=True)

with colB:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("**Operational Factors**")
    traffic = st.selectbox("Traffic", options["traffic"], index=0 if options["traffic"] else None)
    weather = st.selectbox("Weather", options["weather"], index=0 if options["weather"] else None)
    vehicle = st.selectbox("Vehicle", options["vehicle"], index=0 if options["vehicle"] else None)
    category = st.selectbox("Category", options["category"], index=0 if options["category"] else None)
    st.markdown("</div>", unsafe_allow_html=True)

with colC:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("**Agent & Time**")
    agent_rating = st.slider("Agent rating", 0.0, 5.0, 4.5, 0.1)
    order_hour = st.slider("Order hour (0–23)", 0, 23, 12)
    day_of_week = st.selectbox(
        "Day of week",
        [0, 1, 2, 3, 4, 5, 6],
        format_func=lambda x: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][x],
        index=0,
    )
    pickup_delay = st.slider("Pickup delay (minutes)", 0.0, 180.0, 10.0, 1.0)
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
# Prediction button
# ----------------------------
st.divider()

action_col1, action_col2 = st.columns([0.78, 0.22], vertical_alignment="center")
with action_col1:
    st.markdown(
        '<div class="muted small">Tip: Use realistic values (e.g., pickup delay 5–25 mins) for best predictions.</div>',
        unsafe_allow_html=True,
    )
with action_col2:
    run = st.button("🚀 Run prediction", use_container_width=True)

# Default: run immediately on first load as well
if "ran_once" not in st.session_state:
    st.session_state["ran_once"] = True
    run = True

if run:
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
        "category": category,
    }])

    time_pred = float(reg_model.predict(X)[0])
    risk = float(clf_model.predict_proba(X)[0, 1])

    # ----------------------------
    # Outputs (KPI cards)
    # ----------------------------
    st.subheader("📈 Predictions")

    k1, k2, k3 = st.columns([0.34, 0.33, 0.33], gap="large")

    with k1:
        st.markdown(
            f"""
            <div class="kpi">
              <div class="kpi-title">Predicted delivery time</div>
              <div class="kpi-value">{time_pred:.1f} <span class="muted">mins</span></div>
              <div class="muted small">Estimated time from pickup to drop</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with k2:
        st.markdown(
            f"""
            <div class="kpi">
              <div class="kpi-title">Delay risk</div>
              <div class="kpi-value">{risk*100:.1f}<span class="muted">%</span></div>
              <div class="muted small">Probability of delay (classification)</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Simple operational guidance
    if risk >= 0.7:
        tag = "High"
        msg = "Consider proactive actions: rider reassignment, route optimisation, or priority escalation."
    elif risk >= 0.4:
        tag = "Medium"
        msg = "Monitor closely: traffic/weather and pickup delay may push this into delay."
    else:
        tag = "Low"
        msg = "Looks healthy: normal operating conditions."

    with k3:
        st.markdown(
            f"""
            <div class="kpi">
              <div class="kpi-title">Operational recommendation</div>
              <div class="kpi-value">{tag}</div>
              <div class="muted small">{msg}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    # Explain inputs summary
    st.markdown("### 🔎 Input Summary")
    summary_cols = st.columns(5)
    summary_cols[0].metric("Distance (km)", f"{distance_km:.1f}")
    summary_cols[1].metric("Traffic", str(traffic))
    summary_cols[2].metric("Weather", str(weather))
    summary_cols[3].metric("Vehicle", str(vehicle))
    summary_cols[4].metric("Pickup delay", f"{pickup_delay:.0f} min")

    with st.expander("How this works (for recruiters/interviews)"):
        st.markdown(
            """
            - **Regression model** predicts *delivery_time* using distance, time, agent rating, and operational factors.
            - **Classification model** predicts *delay_flag* as a probability (delay risk).
            - Categorical variables are **one-hot encoded** and numeric features are passed through in a **Scikit-learn pipeline**.
            - This dashboard is designed for operational decision support (capacity planning and proactive delay prevention).
            """
        )
else:
    st.info("Adjust inputs then click **Run prediction**.")
