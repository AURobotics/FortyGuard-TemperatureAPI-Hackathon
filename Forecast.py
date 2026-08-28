import streamlit as st 
import pandas as pd 
import altair as alt
import geopandas as gpd
from shapely.geometry import Polygon
import folium 
from folium.plugins import Draw
from streamlit_folium import st_folium
from datetime import datetime, timedelta
import json
from Fortyguard import FortyGuardClient

client = FortyGuardClient(
    api_key="1f09e84c78a5b65ff648ce9e93b55cc6"
)

# -------------------------
# USA Coordinates
# -------------------------
countries = gpd.read_file("ne_10m_admin_0_countries.shp")
USA = countries[countries["ADMIN"] == "United States of America"]

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



if "forecast_data" not in st.session_state:
    st.session_state.forecast_data = None

if "forecast_latitude" not in st.session_state:
    st.session_state.forecast_latitude = None

if "forecast_longitude" not in st.session_state:
    st.session_state.forecast_longitude = None

if "heatmap_data" not in st.session_state:
    st.session_state.heatmap_data = None

if "heat_polygon" not in st.session_state:
    st.session_state.heatmap_polygon = None  

if "heatmap_hours" not in st.session_state:
    st.session_state.heatmap_hours = None 

if "heatmap_granularity" not in st.session_state:
    st.session_state.heatmap_granularity = None 

if "heatmap_filter_type" not in st.session_state:
    st.session_state.heatmap_filter_type = None

# -------------------------
# Select Polygon
# -------------------------
st.markdown(
    '<div class="second-title"> Select Area</div',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="card">
        <h3>Draw your area</h3>
        <p style="color:"#cbd5e1;">
            Draw a polygon on the map to select the area you want to analyze.
        </p>
    </div>        
    """,
    unsafe_allow_html=True
)
## create map
map = folium.Map(
    location = [40.7128,-74.0060],
    zoom_start = 11,
    tiles = "OpenStreetMap"
)
## Drawing
Draw(
    export=True,
    draw_options={
        "polyline":False,
        "rectangle":False,
        "circle":False,
        "marker":False,
        "circlemarker":False,
        "polygon":True 
    },
    edit_options={
        "edit":True,
        "remove":True
    }
).add_to(map)
##Display map
map_data = st_folium(
    map,
    width=1200,
    height=600,
    key="polygon_map",
    returned_objects=["last_active_drawing"]
) 
if map_data and map_data["last_active_drawing"] is not None:
    selected_polygon = map_data["last_active_drawing"]
    if selected_polygon["geometry"]["type"] == "Polygon":
        st.session_state.heatmap_polygon = (
            selected_polygon["geometry"]["coordinates"]
            )


# -------------------------
# Get Saved Polygon
# -------------------------
predict = False

if st.session_state.heatmap_polygon is not None:

    coordinates = st.session_state.heatmap_polygon

    st.markdown(
        """
        <div style="
            background: rgba(15, 23, 42, 0.9);
            color: #f8fafc;
            padding: 12px 18px;
            border-radius: 10px;
            border: 1px solid rgba(148, 163, 184, 0.2);
            font-weight: 700;
            text-align: center;
        ">
            ✓ Polygon Selected Successfully
        </div>
        """,
        unsafe_allow_html=True
    )

    
    with st.form("heatmap_form"):
            st.markdown(
                '<div class="second-title">Forecast time</div>'
                ,unsafe_allow_html=True
            )
            st.markdown(
            '<p style="color:#0f172a; font-size:1.2rem; font-weight:800;">'
            'How many hours from now you want predict temperature?'
            '</p>',
            unsafe_allow_html=True
            )
            hours = st.slider(
                "Forecast hours",
                min_value= 1,
                max_value=12,
                value=1,
                label_visibility="collapsed"
            )
            ## Granularity
            st.markdown( '<p style="color:#0f172a; font-size:1.2rem; font-weight:800;">' \
            '' 'Enter Heatmap Granularity (meters)' '</p>'
            , unsafe_allow_html=True )
            granularity = st.selectbox(
                "Granularity",
                options=[60,80,100],
                index=2,
                label_visibility="collapsed"
            )
            ## filter type
            if hours == 1:
                filter_type = 1
            else :
                filter_type = 2    

            predict = st.form_submit_button(
                "🌡️ Generate Heatmap",
                use_container_width=True
            )

# -------------------------
# Heatmap
# -------------------------
if predict:
    ## prepare polygon for API 
    polygon_aoi = {
        "type" : "Polygon",
        "coordinates" : coordinates
    }
    ## Current Date & Time
    now = datetime.now()

    next_hour = now + timedelta(hours=1)

    start_date = next_hour.strftime("%Y-%m-%d")
    start_time = next_hour.strftime("%H:00")

    end_datetime = next_hour + timedelta(hours=hours)
    if hours == 1:
        filter_type = 1
        heatmap_response = client.create_heatmap(
        polygon_aoi=polygon_aoi,
        start_date=start_date,
        start_time=start_time,
        filter_type=filter_type,
        granularity=granularity,
        analytic_type="tcm",
        verbose=False
        )
    else:
        if end_datetime.date() == next_hour.date():
            filter_type = 2
            end_time = end_datetime.strftime("%H:00")

            heatmap_response = client.create_heatmap(
            polygon_aoi=polygon_aoi,
            start_date=start_date,
            start_time=start_time,
            end_time=end_time,
            filter_type=filter_type,
            granularity=granularity,
            analytic_type="tcm",
            verbose=False
            )
        else:
            filter_type = 4
            end_date = end_datetime.strftime("%Y-%m-%d")
            heatmap_response = client.create_heatmap(
                polygon_aoi=polygon_aoi,
                start_date=start_date,
                end_date=end_date,
                filter_type=filter_type,
                granularity=granularity,
                analytic_type="tcm",
                verbose=False
            )    


    st.session_state.heatmap_data = heatmap_response
    st.session_state.heatmap_polygon = coordinates
    st.session_state.heatmap_hours = hours
    st.session_state.heatmap_granularity = granularity
    st.session_state.heatmap_filter_type = filter_type

if (
    st.session_state.heatmap_data is not None
    and st.session_state.heatmap_polygon is not None
):
    result = st.session_state.heatmap_data.get("result",{})
    map_data = result.get("map_data")
    if map_data and map_data.get("features"):
        st.markdown(
            '<div class="second-title">Temperature Heatmap</div>',
            unsafe_allow_html=True
        )

        first_point = st.session_state.heatmap_polygon[0][0]
        heatmap_map = folium.Map(
            location=[first_point[1],first_point[0]],
            zoom_start=12,
            tiles="OpenStreetMap"
        )
        temperatures = []
        for feature in map_data["features"]:
            temp = feature["properties"].get("average_temperature")
            if temp is not None:
                temperatures.append(temp)
        if temperatures:
            min_temp = min(temperatures)
            max_temp = max(temperatures)

            def style_heatmap(feature):
                temp = feature["properties"].get(
                    "average_temperature",
                    min_temp
                )        
                if max_temp == min_temp:
                    fraction = 0
                else :
                    fraction = (
                        temp - min_temp
                    ) / (max_temp-min_temp)

                red = int(255 * fraction)
                blue = int(255 * (1-fraction))
                return {
                    "fillColor": f"#{red:02x}00{blue:02x}",
                    "color": "#00000000",
                    "weight": 0,
                    "fillOpacity": 0.7
                } 
            folium.GeoJson(
                        map_data,
                        style_function=style_heatmap,
                        tooltip=folium.GeoJsonTooltip( 
                            fields=[ "tile_id",
                                    "average_temperature",
                                    "min_temperature",
                                    "max_temperature" ],
                                    aliases=[ 
                                        "Tile",
                                        "Average Temperature",
                                        "Minimum Temperature",
                                        "Maximum Temperature" ],
                                        localize=True ) ).add_to(heatmap_map)
            st_folium(
                heatmap_map,
                width=1200,
                height=600,
                key="temperature_heatmap" ,
                returned_objects=[]
                ) 
        else: 
            st.error("No heatmap data was returned from FortyGuard.")




