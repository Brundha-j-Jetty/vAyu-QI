import streamlit as st
import joblib
import pandas as pd

model = joblib.load("models/aqi_model.pkl")
features = joblib.load("models/model_features.pkl")
mean_values = joblib.load("models/mean_values.pkl")
city_avg = joblib.load("models/city_avg.pkl")
city_columns = [col for col in features if col.startswith("City_")]
cities = [col.replace("City_", "") for col in city_columns]


# -----------------------------
# AQI Analysis Function
# -----------------------------
def display_aqi_analysis(prediction, dominant, pollutant_data):

    # AQI Category
    if prediction <= 50:
        category = "Good 🟢"
    elif prediction <= 100:
        category = "Moderate 🟡"
    elif prediction <= 200:
        category = "Poor 🟠"
    elif prediction <= 300:
        category = "Very Poor 🔴"
    else:
        category = "Severe ⚫"
    st.success(f"Predicted AQI: {round(prediction)}")
    st.markdown(f"### AQI Category: {category}")
        

    # Health Impact
    if prediction <= 50:
        health = "Air quality is good. Safe for outdoor activities."
    elif prediction <= 100:
        health = "Air is acceptable. Sensitive individuals may feel slight discomfort."
    elif prediction <= 200:
        health = "Breathing discomfort possible. Reduce prolonged outdoor exposure."
    elif prediction <= 300:
        health = "Unhealthy air. Avoid outdoor activities."
    else:
        health = "Severe conditions. Stay indoors and use protective measures."
    st.divider()

    st.info(f"🫁 Health Impact: {health}")

    # Recommended Actions
    st.divider()
    st.subheader("🌿 Recommended Actions")

    if prediction <= 50:
        personal = ["Enjoy outdoor activities", "Keep windows open for fresh air"]
        environmental = ["Maintain green surroundings", "Promote eco-friendly habits"]

    elif prediction <= 100:
        personal = [
            "Safe for most people",
            "Sensitive individuals should take light precautions",
        ]
        environmental = [
            "Reduce unnecessary vehicle usage",
            "Support clean energy initiatives",
        ]

    elif prediction <= 200:
        personal = ["Limit prolonged outdoor exposure", "Wear a mask if needed"]
        environmental = ["Use public transport", "Avoid burning waste"]

    elif prediction <= 300:
        personal = ["Avoid outdoor activities", "Use air purifiers indoors"]
        environmental = ["Reduce industrial emissions", "Encourage carpooling"]

    else:
        personal = ["Stay indoors", "Wear N95 masks if going outside"]
        environmental = [
            "Strict pollution control measures needed",
            "Government intervention required",
        ]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("👤 Personal Actions")
        for act in personal:
            st.write(f"- {act}")

    with col2:
        st.subheader("🌍 Environmental Actions")
        for act in environmental:
            st.write(f"- {act}")

    # Government Policies
    st.divider()
    st.subheader("🏛️ Government Initiatives")

    if prediction <= 100:
        policies = [
            {
                "name": "National Clean Air Programme (NCAP)",
                "desc": "A government initiative to reduce PM2.5 and PM10 levels in major cities.",
                "use": "Support local environmental programs and spread awareness.",
            }
        ]

    elif prediction <= 200:
        policies = [
            {
                "name": "NCAP",
                "desc": "Targets reduction of harmful particulate matter across cities.",
                "use": "Participate in community green drives and reduce pollution sources.",
            },
            {
                "name": "BS6 Emission Norms",
                "desc": "Stricter vehicle emission standards to control air pollution.",
                "use": "Prefer BS6 vehicles and maintain your vehicle properly.",
            },
        ]

    elif prediction <= 300:
        policies = [
            {
                "name": "Odd-Even Rule",
                "desc": "Limits vehicles on roads based on registration numbers.",
                "use": "Use public transport and follow traffic restrictions.",
            }
        ]

    else:
        policies = [
            {
                "name": "GRAP",
                "desc": "Emergency pollution control measures during severe AQI.",
                "use": "Follow public safety and pollution control guidelines.",
            }
        ]

    for policy in policies:
        st.markdown(f"**{policy['name']}**")
        st.write(f"📌 {policy['desc']}")
        st.write(f"👉 {policy['use']}")
        st.write("---")

    # Pollutant Insight
    st.subheader("🧠 Key Pollutant Insight")
    st.success(f"Dominant Pollutant: {dominant}")
    # -----------------------------
    # Pollutant Visualization Chart
    # -----------------------------
    st.divider()

    st.subheader("📈 Pollutant Levels")

    chart_df = pd.DataFrame(
        {
            "Pollutant": list(pollutant_data.keys()),
            "Value": list(pollutant_data.values())
        }
    )

    st.bar_chart(chart_df.set_index("Pollutant"))


# -----------------------------
# Page Config (VERY IMPORTANT)
# -----------------------------
st.set_page_config(page_title="vAyu-QI", page_icon="🍃", layout="wide")
# -----------------------------
# Custom Styling (Premium Look)
# -----------------------------
st.markdown(
    """
    <style>
    body {
        background-color: #0e1117;
    }
    .main {
        background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
        color: white;
    }
    h1 {
        text-align: center;
        font-weight: bold;
    }
    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #a0c4ff;
        margin-bottom: 30px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# -----------------------------
# Title Section
# -----------------------------
st.markdown("<h1>🍃 vAyu-QI</h1>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>Air Quality Intelligence System</div>",
    unsafe_allow_html=True,
)

st.sidebar.title("🍃 vAyu-QI")

st.sidebar.info(
    "An AI-powered environmental intelligence platform that predicts AQI levels,analyzes pollutant impact, and provides actionable environmental insights through interactive visualization and simulation."
)
# -----------------------------
# Divider
# -----------------------------
st.divider()

# -----------------------------
# Mode Selection (Basic)
# -----------------------------
mode = st.radio("Select Mode", ["Simple Mode", "Advanced Mode"], horizontal=True)

st.write(f"Current Mode: {mode}")
# -----------------------------
# Simple Mode Input
# -----------------------------
if mode == "Simple Mode":

    st.subheader("🌱 Simple AQI Prediction")

    st.info("Enter basic pollution values for a quick prediction")

    col1, col2, col3 = st.columns(3)

    with col1:
        city = st.selectbox("Select City", sorted(cities))

    # Get city average values
    city_data = city_avg.loc[city]

    with col2:
        pm25 = st.number_input("PM2.5", min_value=0.0, value=float(city_data["PM2.5"]))

    with col3:
        pm10 = st.number_input("PM10", min_value=0.0, value=float(city_data["PM10"]))
    st.caption(
        "Enter values in µg/m³ (micrograms per cubic meter). Approximate values are acceptable."
    )
    st.warning("⚠️ This mode gives approximate predictions using limited inputs")
    predict_simple = st.button("Predict AQI (Simple Mode)")

    if predict_simple:

        # Create input dictionary
        input_data = {"PM2.5": pm25, "PM10": pm10}

        input_df = pd.DataFrame([input_data])

        # Add missing features with default (0)
        for col in features:
            if col not in input_df.columns:
                input_df[col] = mean_values.get(col, 0)

        # Handle city encoding
        for col in features:
            if "City_" in col:
                input_df[col] = 1 if col == f"City_{city}" else 0

        # Ensure correct column order
        input_df = input_df[features]

        # Prediction
        prediction = model.predict(input_df)[0]

        # Dominant pollutant
        if pm25 > pm10:
            dominant = "PM2.5"
        else:
            dominant = "PM10"

        pollutant_data = {
            "PM2.5": pm25,
            "PM10": pm10
        }

        display_aqi_analysis(prediction, dominant, pollutant_data)

# -----------------------------
# Advanced Mode Input
# -----------------------------
if mode == "Advanced Mode":

    st.subheader("⚙️ Advanced AQI Prediction")

    st.markdown("### 🌍 Intelligent Environmental Simulation")

    st.info(
        "Pollutant values are auto-filled using historical city patterns. "
        "You may adjust them manually to simulate different environmental conditions."
    )

    # Inputs
    col1, col2, col3 = st.columns(3)

    with col1:
        city = st.selectbox("Select City", sorted(cities))
        city_data = city_avg.loc[city]
        scenario = st.selectbox(
            "Select Environmental Scenario",
            [
                "Normal Conditions",
                "Heavy Traffic",
                "Industrial Zone",
                "Rainy Day",
                "Green Area",
            ],
        )
        # Scenario adjustments
        multiplier = 1.0

        if scenario == "Heavy Traffic":
            multiplier = 1.3

        elif scenario == "Industrial Zone":
            multiplier = 1.5

        elif scenario == "Rainy Day":
            multiplier = 0.7

        elif scenario == "Green Area":
            multiplier = 0.6
        pm25 = st.number_input(
            "PM2.5", min_value=0.0, value=float(city_data["PM2.5"] * multiplier)
        )
        pm10 = st.number_input(
            "PM10", min_value=0.0, value=float(city_data["PM10"] * multiplier)
        )
        no = st.number_input(
            "NO", min_value=0.0, value=float(city_data["NO"] * multiplier)
        )

    with col2:
        no2 = st.number_input(
            "NO2", min_value=0.0, value=float(city_data["NO2"] * multiplier)
        )
        nox = st.number_input(
            "NOx", min_value=0.0, value=float(city_data["NOx"] * multiplier)
        )
        nh3 = st.number_input(
            "NH3", min_value=0.0, value=float(city_data["NH3"] * multiplier)
        )
        co = st.number_input(
            "CO", min_value=0.0, value=float(city_data["CO"] * multiplier)
        )

    with col3:
        so2 = st.number_input(
            "SO2", min_value=0.0, value=float(city_data["SO2"] * multiplier)
        )
        o3 = st.number_input(
            "O3", min_value=0.0, value=float(city_data["O3"] * multiplier)
        )
        benzene = st.number_input(
            "Benzene", min_value=0.0, value=float(city_data["Benzene"] * multiplier)
        )
        toluene = st.number_input(
            "Toluene", min_value=0.0, value=float(city_data["Toluene"] * multiplier)
        )

    st.caption("All values are in µg/m³")

    predict_advanced = st.button("Predict AQI (Advanced Mode)")
    if predict_advanced:

        input_data = {
            "PM2.5": pm25,
            "PM10": pm10,
            "NO": no,
            "NO2": no2,
            "NOx": nox,
            "NH3": nh3,
            "CO": co,
            "SO2": so2,
            "O3": o3,
            "Benzene": benzene,
            "Toluene": toluene,
        }

        input_df = pd.DataFrame([input_data])

        # Add city encoding
        for col in features:
            if "City_" in col:
                input_df[col] = 1 if col == f"City_{city}" else 0

        # Ensure all columns exist
        input_df = input_df.reindex(columns=features, fill_value=0)

        prediction = model.predict(input_df)[0]
        # Find dominant pollutant
        pollutants = {
            "PM2.5": pm25,
            "PM10": pm10,
            "NO": no,
            "NO2": no2,
            "NOx": nox,
            "NH3": nh3,
            "CO": co,
            "SO2": so2,
            "O3": o3,
            "Benzene": benzene,
            "Toluene": toluene,
        }

        dominant = max(pollutants, key=pollutants.get)

        display_aqi_analysis(prediction, dominant, pollutants)

st.divider()

st.caption(
    "Dataset Source: Historical AQI dataset (up to 2020). "
    "Predictions are simulation-based and intended for educational "
    "and analytical purposes."
)

