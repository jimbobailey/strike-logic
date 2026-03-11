import streamlit as st
import requests

# CONFIG: Glowing Orange Theme
st.set_page_config(page_title="STRIKE LOGIC", page_icon="🎣")
st.markdown("""
    <style>
    .stApp { background-color: #1A1A1A; color: #FFFFFF; }
    .stButton>button { background-color: #FF4500; color: white; font-weight: bold; }
    h1, h2, h3 { color: #FF4500; }
    </style>
""", unsafe_allow_html=True)

LOC_DATA = {
    "Apalachicola River (Chattahoochee)": ["02358000", 30.7047, -84.8569, "River"],
    "Apalachicola River (Blountstown)": ["02358700", 30.4385, -85.0113, "River"],
    "Chipola River (Marianna)": ["02358789", 30.7744, -85.2269, "Creek"],
    "Chipola River (Altha)": ["02359000", 30.2921, -85.1363, "Creek"],
    "Ochlockonee River (Bloxham)": ["02330000", 30.3831, -84.6533, "River"],
    "Lake Talquin": ["02329900", 30.4741, -84.6469, "Lake"],
    "Holmes Creek (Vernon)": ["02366000", 30.6300, -85.8300, "Creek"],
    "Lake Seminole": ["02357500", 30.7088, -84.8631, "Lake"]
}

TACTICS = {
    "Largemouth Bass": {"River": ["1. 3/8oz Jig & Craw", "2. Topwater Frog", "3. (Dead Bite) Downsize finesse"], "Lake": ["1. Deep crankbait", "2. Senko Wacky-rig", "3. (Dead Bite) Drop-shot"], "Creek": ["1. Spinnerbait", "2. Jerkbait", "3. (Dead Bite) Weightless plastic"]},
    "Shellcracker": {"River": ["1. Red wigglers", "2. Beetle-spin", "3. (Dead Bite) Slow drag"], "Lake": ["1. Earthworms", "2. Hybrid worms", "3. (Dead Bite) Split-shot"], "Creek": ["1. Crickets", "2. Wax worms", "3. (Dead Bite) Micro-jig"]},
    "Channel/Blue Catfish": {"River": ["1. Cut shad", "2. Chicken liver", "3. (Dead Bite) Dip bait"], "Lake": ["1. Drift fishing", "2. Punch bait", "3. (Dead Bite) Live bluegill"], "Creek": ["1. Nightcrawlers", "2. Cut bait", "3. (Dead Bite) Increase scent"]},
    "Shoal Bass": {"River": ["1. Topwater walker", "2. Craw crankbait", "3. (Dead Bite) Small tube jig"], "Lake": ["N/A", "N/A", "N/A"], "Creek": ["1. Spinnerbait", "2. Fluke", "3. (Dead Bite) Micro-jig"]},
    "Black Crappie": {"River": ["1. Vertical jig", "2. Minnow float", "3. (Dead Bite) Trolling slow"], "Lake": ["1. Minnows", "2. Chartreuse jigs", "3. (Dead Bite) Slow vertical"], "Creek": ["1. Small tube jigs", "2. Beetle-spin", "3. (Dead Bite) Dead-sticking"]}
}

st.title("STRIKE LOGIC")
name = st.selectbox("LOCATION", list(LOC_DATA.keys()))
species = st.selectbox("SPECIES", list(TACTICS.keys()))

if st.button("CATCH FISH"):
    sid, lat, lon, w_type = LOC_DATA[name]
    
    # Robust USGS Fetch
    level = "Data Unavailable"
    try:
        url = f"https://waterservices.usgs.gov/nwis/iv/?format=json&sites={sid}&parameterCd=00065"
        resp = requests.get(url, timeout=5).json()
        ts = resp.get('value', {}).get('timeSeries', [])
        if ts and len(ts) > 0 and 'values' in ts[0] and len(ts[0]['values']) > 0 and len(ts[0]['values'][0].get('value', [])) > 0:
            level = f"{ts[0]['values'][0]['value'][0]['value']} FT"
    except: pass

    st.write(f"### GAGE HEIGHT: {level}")
    
    # Weather
    try:
        grid = requests.get(f"https://api.weather.gov/points/{lat},{lon}", timeout=5, headers={'User-Agent': 'StrikeLogic'}).json()
        fc = requests.get(grid['properties']['forecast'], timeout=5).json()['properties']['periods'][0]
        st.write(f"### WEATHER: {fc['shortForecast']} | {fc['temperature']}°F")
    except: st.write("### WEATHER: Data Unavailable")
        
    p = 30.05
    st.write(f"### PRESSURE: {p} inHg")
    
    strat = TACTICS[species].get(w_type, ["1. Search."])
    st.subheader("STRATEGIES")
    for s in strat: st.write(s)
    
    if not (29.80 <= p <= 30.20):
        st.error("BARO NOTE: LOCKJAW RANGE (30.21-30.50+)")