import streamlit as st 
from model import predict_temperature
import pandas as pd 
import altair as alt
# -------------------------
# Page Configration
# -------------------------
st.set_page_config(
    page_title=" Forecasting heat(FortyGaurd)",
    page_icon="🌡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------
# Custom CSS   # access to use HTML & CSS
# -------------------------
st.markdown("""
<style>
    /* 1. Standardized Sidebar Width */
    [data-testid="stSidebar"] {
        min-width: 350px !important;
        max-width: 350px !important;
    }
    
    /* Hide Sidebar Collapse Button */
    [data-testid="stSidebarCollapseButton"] {
        display: none !important;
    }

    /* 2. Standardized Sidebar Font Sizing */
    [data-testid="stSidebar"] * {
        font-size: 1.2rem !important;
    }
    
    [data-testid="stSidebarNav"] span {
        font-size: 1.35rem !important;
        font-weight: 600 !important;
    }
    /*Main background*/
    .stApp {
    background: url('https://images.unsplash.com/photo-1513002749550-c59d786b8e6c?q=80&w=1920&auto=format&fit=crop') no-repeat center center fixed !important;
    background-size: cover !important;
}

    /* Remove default top padding */
    .block-container{
    padding-top: 2rem;
    padding-top: 3rem;
    max-width: 1200px;
    }

    /* Header */
    .header {
    text-align: center;
    padding: 40px 0 35px 0;
    }

    .header h1{
    font-size: 3.2rem;
    font-weight: 800;
    margin-bottom: 5px;
    letter-spacing: -1px;
    }

    .header p{
    font-size: 1.5rem;
    color: #121212;
    margin-top: 0;
    }

    /* Second Title */
    .second-title {
    font-size: 3rem;
    font-weight: 900;
    margin: 25px 0 15px 0;
    color: #121212;
    }

    /* Cards */
    .card{
    background: rgba(30, 41, 59, 0.75);
    border: 1px solid rgba(148, 163, 184, 0.15);
    border-radius: 18px;
    padding: 25px;
    margin-bottom: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }

    /* Prediction button */
    .stButton > button {
    width: 100%;
    height: 50px;
    border-radius: 12px;
    font-size: 2rem;
    font-weight: 900;
    border: none;
    background: linear-gradient(
    90deg,
    #f97316
    
    );
    color: white;
    transition: 0.2s;
    }
    .stButton > button:hover{
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(249,115,2,0.25);
    }

    /*Input labels*/
    label{
    font-weight: 900!important;
    }

    /*Forecast table*/
    .forecast-card{
    background: rgba(30,41,59,0.75);
    border-radius: 18px;
    padding: 15px;
    border: 1px solid rgba(148,163,184,0.15);
    }

    /*forecast rows*/
    .forecast-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px 10px;
    border-bottom: 1px solid rgba(148,163,184,0.1);
    transition: 0.2s
    }
    .forecast-row:last-child {
    border-bottom: none;
    }
    .forecast-row:hover{
    background: rgba(148,163,184,0.1);
    border-radius: 10px;
    }
    .forecast-time {
    color: #cbd5e1;
    font-size: 2rem;
    font-weight: 700;
    }
    .forecast-temp {
    color: #fb923c;
    font-size: 2rem;
    font-weight: 700;
    }

    /*Status badge*/
    .status{
    display: inline-block;
    padding: 6px 12px;
    background: rgba(34,197,184,0.12);
    color: #4ade80;
    font-size: 1rem;
    font-weight: 600;
    border-radius: 20px;
    }
    </style>
    """,unsafe_allow_html=True)
# -------------------------
# Header
# -------------------------
st.markdown("""
<div class="header">
    <div style="font-size: 3rem;">🌡️</div>
    <h1>HeatCast</h1>
    <p>
        AI-powered temperature forecasting for your location
    </p>

<div class="status">● Forecast system ready</div>
</div>
""",unsafe_allow_html=True)

# -------------------------
# Location Input
# -------------------------
st.markdown(
    '<div class="second-title"> Select Location</div',
    unsafe_allow_html=True
)

col1 , col2 = st.columns(2)
with col1:
    latitude = st.number_input(
        "latitude (-90 , 90)",
        value=0.0,
        min_value=-90.0,
        max_value=90.0,
        format= "%.7f"
    )
with col2:
    longitude = st.number_input(
        "longitude (-180,180)",
        value=0.0,
        min_value=-180.0,
        max_value=180.0,
        format="%.7f"
    )

# -------------------------
# Predict Button
# -------------------------
predict = st.button(
    "🔮 Predict Temperature",
    use_container_width=True
)

# -------------------------
# Model
# -------------------------
if predict:
    st.markdown(
        '<div class="second-title"> Temperature Forecast</div>',
        unsafe_allow_html=True
    )

    
    # -------------------------
    # Location Card
    # -------------------------
    st.markdown(f"""
<div class="card">
<h3>Selected Location</h3>
<p style="color:#94a3b8;">Forecast location</p>
<p><strong>Latitude:</strong>{latitude}</p>
<p><strong>Longitude:</strong>{longitude}</p>
</div>
""",unsafe_allow_html=True)


    # -------------------------
    # Map Card
    # -------------------------
    st.markdown(
        '<div class="second-title">Site Location</div',
        unsafe_allow_html=True
    )
    map_html = f"""
    <div class="card" style="padding:0; overflow:hidden;">
        <iframe
            src="https://www.google.com/maps?q={latitude},{longitude}&z=19&output=embed"
            width="100%"
            height="250"
            style="border:0; border-radius: 18px; display:block;"
            loading="lazy"
            allowfullscreen>
        </iframe>
    </div>
    """   
    st.markdown(map_html,unsafe_allow_html=True)
    # -------------------------
    # satellite Card 
    # -------------------------
    st.markdown(
            '<div class="second-title">Satellite View</div',
            unsafe_allow_html=True
        )
    satellite_html = f"""
    <div class="card" style="padding:0; overflow:hidden;">
        <iframe
            src="https://www.google.com/maps?q={latitude},{longitude}&z=19&t=k&output=embed"
            width="100%"
            height="250"
            style="border:0; border-radius: 18px; display:block;"
            loading="lazy"
            allowfullscreen>
        </iframe>
    </div>
    """
    st.markdown(satellite_html,unsafe_allow_html=True)

    # -------------------------
    # satellite Card 
    # -------------------------
    st.markdown(
            '<div class="second-title">Street View</div',
                unsafe_allow_html=True)
    street_html = f"""
    <div class="card" style="padding:0; overflow:hidden;">
        <iframe
            src="https://www.google.com/maps/embed?pb=!4v0!6m8!1m7!1sCAoSLEFGMVFpcE...!2m2!1d{latitude}!2d{longitude}!3f0!4f0!5f0.7820865974627469"
            width="100%"
            height="250"
            style="border:0; border-radius: 18px; display:block;"
            loading="lazy"
            allowfullscreen>
        </iframe>
    </div>
    """
    st.markdown(street_html,unsafe_allow_html=True)

    # -------------------------
    # Forecast Card
    # -------------------------
    forecast = predict_temperature(latitude,longitude) ## Real Model(Model sent a dict to GUI)
    rows_html = ""
    for time, temperature in forecast.items():
            rows_html += f"""
    <div class="forecast-row">
        <span class="forecast-time">{time}</span>
        <span class="forecast-temp">{temperature}</span>
    </div>
    """    
    st.markdown(f"""
    <div class="forecast-card">
    <h3>Forecast</h3>
    {rows_html}
    </div>
    """,unsafe_allow_html=True)

    # -------------------------
    # Temperature History
    # -------------------------                
    st.markdown(
        '<div class="second-title">Temperature History</div>',
        unsafe_allow_html=True
    )
    history_df = pd.DataFrame(
        list(forecast.items()),
        columns=["time","temperature"]
    )

    history_df["temp_val"] = history_df["temperature"].str.replace(" °C","").astype(float)
    base = alt.Chart(history_df).encode(
        x = alt.X("time",title="Time",sort=None,
                axis=alt.Axis(labelFontSize=16,titleFontSize=20,grid=True,
                        gridColor="rgba(148,163,184,0.25)",gridDash=[4,4])),

        y = alt.Y("temp_val:Q",title="Temperature (°C)",
                axis=alt.Axis(labelFontSize=16,titleFontSize=20,grid=True,
                        gridColor="rgba(148,163,184,0.25)",gridDash=[4,4]))
    )
    line = base.mark_line(color="#fb923c",strokeWidth=0.5)
    points = base.mark_circle(size=100,color="#fb923c")
    chart = (line + points).properties(
        height=350
    ).configure_view(
        strokeWidth=0
    ).configure_axis(
        labelColor="#cbd5e1",
        titleColor="#e2e8f0",
        gridColor="rgba(148,163,184,0.1)"
    )
    st.altair_chart(chart,use_container_width=True)

