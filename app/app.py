<<<<<<< HEAD
import os
import joblib
import pandas as pd
import streamlit as st

# ------------------------------------------------
# Resolve project paths safely
# ------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

REG_MODEL_PATH = os.path.join(BASE_DIR, "delivery_time_model.joblib")
CLF_MODEL_PATH = os.path.join(BASE_DIR, "delay_risk_model.joblib")

DATA_PATH = os.path.abspath(
    os.path.join(BASE_DIR, "..", "data", "cleaned", "cleaned_delivery.csv")
)

# ------------------------------------------------
# Page Config
# ------------------------------------------------
st.set_page_config(
    page_title="DeliveryOps Intelligence",
    page_icon="🚚",
    layout="wide"
)

# ------------------------------------------------
# Styling
# ------------------------------------------------
st.markdown("""
<style>
.block-container {
    padding-top: 1.5rem;
}

.kpi {
    border-radius: 16px;
    padding: 18px;
    border: 1px solid rgba(49,51,63,0.2);
}

.kpi-title {
    font-size: 0.9rem;
    opacity: 0.7;
}

.kpi-value {
    font-size: 1.9rem;
    font-weight: 700;
}

.card {
    border-radius: 16px;
    padding: 16px;
    border: 1px solid rgba(49,51,63,0.2);
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# Utility Functions
# ------------------------------------------------
def safe_unique(series):
    if series is None:
        return []
    vals = series.dropna().astype(str).unique().tolist()
    return sorted(vals)


def load_dropdown_options():

    if os.path.exists(DATA_PATH):

        df = pd.read_csv(DATA_PATH)

        return {
            "traffic": safe_unique(df.get("traffic")),
            "weather": safe_unique(df.get("weather")),
            "vehicle": safe_unique(df.get("vehicle")),
            "area": safe_unique(df.get("area")),
            "category": safe_unique(df.get("category"))
        }

    # fallback defaults
    return {
        "traffic": ["Low", "Medium", "High"],
        "weather": ["Clear", "Rainy", "Foggy"],
        "vehicle": ["Bike", "Car", "Scooter"],
        "area": ["Urban", "Suburban", "Rural"],
        "category": ["Food", "Grocery", "Pharmacy", "Electronics"]
    }


# ------------------------------------------------
# Header
# ------------------------------------------------
left, right = st.columns([0.7,0.3])

with left:
    st.title("🚚 DeliveryOps Intelligence System")
    st.caption("Predict delivery time and delay risk using machine learning")

with right:
    st.markdown("""
    <div class="card">
    <b>System Status</b><br>
    ML Pipelines Active<br><br>
    <span>Regression + Classification</span>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ------------------------------------------------
# Check model existence
# ------------------------------------------------
if not (os.path.exists(REG_MODEL_PATH) and os.path.exists(CLF_MODEL_PATH)):

    st.warning("""
⚠️ Model files not found.

Run the training notebook:

`notebooks/02_model.ipynb`

to generate:

- app/delivery_time_model.joblib
- app/delay_risk_model.joblib
""")

    st.stop()

# ------------------------------------------------
# Load Models
# ------------------------------------------------
reg_model = joblib.load(REG_MODEL_PATH)
clf_model = joblib.load(CLF_MODEL_PATH)

# ------------------------------------------------
# Load dropdown values
# ------------------------------------------------
options = load_dropdown_options()

# ------------------------------------------------
# Inputs
# ------------------------------------------------
st.subheader("📥 Delivery Scenario Inputs")

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown("### Location")

    distance_km = st.slider("Distance (km)",0.0,60.0,5.0)

    area = st.selectbox("Area",options["area"])


with col2:

    st.markdown("### Operations")

    traffic = st.selectbox("Traffic",options["traffic"])

    weather = st.selectbox("Weather",options["weather"])

    vehicle = st.selectbox("Vehicle",options["vehicle"])

    category = st.selectbox("Category",options["category"])


with col3:

    st.markdown("### Agent + Time")

    agent_rating = st.slider("Agent Rating",0.0,5.0,4.5)

    order_hour = st.slider("Order Hour",0,23,12)

    day_of_week = st.selectbox(
        "Day of Week",
        [0,1,2,3,4,5,6],
        format_func=lambda x:["Mon","Tue","Wed","Thu","Fri","Sat","Sun"][x]
    )

    pickup_delay = st.slider("Pickup Delay (mins)",0.0,180.0,10.0)


st.divider()

# ------------------------------------------------
# Prediction Button
# ------------------------------------------------
run = st.button("🚀 Run Prediction")

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
        "category": category
    }])

    delivery_time = reg_model.predict(X)[0]

    delay_prob = clf_model.predict_proba(X)[0][1]

    st.subheader("📊 Predictions")

    k1,k2,k3 = st.columns(3)

    with k1:

        st.markdown(f"""
        <div class="kpi">
        <div class="kpi-title">Predicted Delivery Time</div>
        <div class="kpi-value">{delivery_time:.1f} mins</div>
        </div>
        """,unsafe_allow_html=True)

    with k2:

        st.markdown(f"""
        <div class="kpi">
        <div class="kpi-title">Delay Risk</div>
        <div class="kpi-value">{delay_prob*100:.1f}%</div>
        </div>
        """,unsafe_allow_html=True)


    if delay_prob > 0.7:

        tag="High Risk"
        msg="Consider rerouting or assigning another rider"

    elif delay_prob > 0.4:

        tag="Moderate Risk"
        msg="Monitor traffic and pickup time"

    else:

        tag="Low Risk"
        msg="Delivery likely on schedule"

    with k3:

        st.markdown(f"""
        <div class="kpi">
        <div class="kpi-title">Operational Advice</div>
        <div class="kpi-value">{tag}</div>
        <div>{msg}</div>
        </div>
        """,unsafe_allow_html=True)

    st.divider()

    st.subheader("🔍 Scenario Summary")

    s1,s2,s3,s4,s5 = st.columns(5)

    s1.metric("Distance",f"{distance_km} km")
    s2.metric("Traffic",traffic)
    s3.metric("Weather",weather)
    s4.metric("Vehicle",vehicle)
    s5.metric("Pickup Delay",f"{pickup_delay} min")

else:

    st.info("Adjust the inputs and click **Run Prediction**.")
=======
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
>>>>>>> ff548dd (Corrected Streamlit UI)
