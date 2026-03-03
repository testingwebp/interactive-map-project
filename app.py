import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# 1. Page Config (Hides the code by default)
st.set_page_config(page_title="World Map Interactive", layout="wide")

# 2. Load Data (Cached so it's fast)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson"
    world = gpd.read_file(url)
    world.columns = [col.lower() for col in world.columns]
    return world

world = load_data()

# 3. Initialize Memory (History)
if 'history' not in st.session_state:
    st.session_state.history = []

st.title("🌍 Interactive World Map Labeler")
st.write("Enter a country name and a label to add it to the map.")

# 4. Sidebar Inputs (This keeps the main area clean)
with st.sidebar:
    st.header("Add New Location")
    country_input = st.selectbox("Select Country", sorted(world['name'].tolist()))
    marker_label = st.text_input("Enter Label", placeholder="e.g., My Hometown")
    
    if st.button("Add to Map"):
        selected = world[world['name'] == country_input]
        point = selected.geometry.representative_point().iloc[0]
        st.session_state.history.append({
            'name': country_input,
            'lat': point.y,
            'lon': point.x,
            'label': marker_label
        })
    
    if st.button("Clear All Markers"):
        st.session_state.history = []
        st.rerun()

# 5. Generate and Display Map
# Start view at the last added point, or center of the world
start_lat, start_lon = (20, 0)
if st.session_state.history:
    start_lat = st.session_state.history[-1]['lat']
    start_lon = st.session_state.history[-1]['lon']

m = folium.Map(location=[start_lat, start_lon], zoom_start=2)

for item in st.session_state.history:
    folium.Marker(
        [item['lat'], item['lon']], 
        popup=item['label'], 
        tooltip=item['name']
    ).add_to(m)

# Display the map in the main area
st_folium(m, width=1000, height=600)
