import streamlit as st
import requests
import time
from streamlit_lottie import st_lottie

# Configure the page
st.set_page_config(page_title="ArrivalIQ Demo", layout="centered")

# Helper function to load the Lottie JSON from a URL
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load a sleek car/map animation
lottie_driving = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_xwmj0hsk.json")

# Build the Header with the Animation
col_anim, col_title = st.columns([1, 3])
with col_anim:
    if lottie_driving:
        st_lottie(lottie_driving, height=120, key="car")
with col_title:
    st.title("ArrivalIQ")
    st.markdown("**Real-Time ETA Prediction Engine**")

st.divider()

# Input UI
col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 Trip Details")
    # Changed max to 100.0 miles
    trip_miles = st.slider("Trip Distance (Miles)", 1.0, 100.0, 5.0, 0.5)
    
    days = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday", 7: "Sunday"}
    day_name = st.selectbox("Day of the Week", list(days.values()), index=4)
    day_num = [k for k, v in days.items() if v == day_name][0]
    
    hour = st.slider("Time of Day (Hour)", 0, 23, 17, format="%d:00")

with col2:
    st.subheader("🚦 Live Traffic State")
    st.markdown("*(Simulates the Redis Feature Store)*")
    # Changed max to 100.0 MPH
    speed = st.slider("Recent 15-min Avg Speed (MPH)", 5.0, 100.0, 15.0, 0.5)

st.divider()

# The Predict Button
if st.button("Predict ETA", type="primary", use_container_width=True):
    # Simulate routing calculation for a realistic UX feel
    with st.spinner("Analyzing live traffic and computing optimal route..."):
        time.sleep(0.8) # Artificial delay
        
        payload = {
            "trip_miles": trip_miles,
            "pickup_hour": hour,
            "pickup_day_of_week": day_num,
            "prior_15m_speed": speed
        }
        
        try:
            response = requests.post("https://arrival-iq-api-51708746478.us-central1.run.app/predict_eta", json=payload)
            data = response.json()
            
            st.success("✅ Prediction Generated")
            
            # Highlight the main display text
            st.metric(label="Expected Arrival", value=data["ui_display_text"])
            
            # Display the quantiles
            c1, c2, c3 = st.columns(3)
            c1.metric("Best Case (p10)", f"{data['eta_best_case_min']} min")
            c2.metric("Median (p50)", f"{data['eta_median_min']} min")
            c3.metric("Worst Case (p90)", f"{data['eta_worst_case_min']} min")
            
        except requests.exceptions.ConnectionError:
            st.error("⚠️ Cannot connect to the API. Is your FastAPI server running?")