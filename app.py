import streamlit as st
import requests

# THEME: Glowing Orange, Black, White, Gray
st.markdown("""
    <style>
    .stApp { background-color: #1A1A1A; color: #FFFFFF; }
    .stButton>button { background-color: #FF4500; color: white; font-weight: bold; }
    h1 { color: #FF4500; }
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
    "Largemouth Bass": {
        "River": ["1. 3/8oz Jig & Craw in current seams.", "2. Topwater frog over grassy banks.", "3. (Dead Bite) Downsize to 4in finesse worm, slow drag."],
        "Lake": ["1. Deep diving crankbait on main lake points.", "2. Senko Wacky-rig around boat docks.", "3. (Dead Bite) Drop-shot in 15ft+ near structure."],
        "Creek": ["1. Spinnerbait along wood structure.", "2. Jerkbait in pockets.", "3. (Dead Bite) Weightless soft-plastic jerkbait, dead-sticking."]
    },
    "Shellcracker": {
        "River": ["1. Red wigglers on bottom in backwater eddies.", "2. Small beetle-spin near lily pads.", "3. (Dead Bite) Cast beyond bed and drag slowly."],
        "Lake": ["1. Earthworms near shell beds.", "2. Hybrid redworms on drop-offs.", "3. (Dead Bite) Light split-shot, long leader."],
        "Creek": ["1. Crickets near overhanging limbs.", "2. Wax worms in eddies.", "3. (Dead Bite) Switch to micro-jigging."]
    },
    "Channel/Blue Catfish": {
        "River": ["1. Cut shad on deep bottom bends.", "2. Chicken liver in slow pools.", "3. (Dead Bite) High-scent dip bait, stationary."],
        "Lake": ["1. Drift fishing shad on flats.", "2. Punch bait near drop-offs.", "3. (Dead Bite) Live bluegill, anchored."],
        "Creek": ["1. Nightcrawlers on deep holes.", "2. Cut bait near feeder mouths.", "3. (Dead Bite) Increase scent profile."]
    },
    "Shoal Bass": {
        "River": ["1. Topwater walker in current breaks.", "2. Craw-pattern crankbait on rocks.", "3. (Dead Bite) Small tube jig, bottom bounce."],
        "Lake": ["N/A", "N/A", "N/A"],
        "Creek": ["1. Spinnerbait in eddies.", "2. Fluke on light lead.", "3. (Dead Bite) Micro-jig, slow drift."]
    },
    "Black Crappie": {
        "River": ["1. Vertical jigging timber.", "2. Minnow under slip float.", "3. (Dead Bite) Trolling slow with small curly tails."],
        "Lake": ["1. Minnows over brush piles.", "2. Chartreuse jigs in coves.", "3. (Dead Bite) Slow vertical jigging."],
        "Creek": ["1. Small tube jigs near wood.", "2. Beetle-spin slow roll.", "3. (Dead Bite) Live minnow, dead-sticking."]
    }
}

st.title("STRIKE LOGIC")
name = st.selectbox("Location", list(LOC_DATA.keys()))
species = st.selectbox("Species", list(TACTICS.keys()))

if st.button("CATCH FISH"):
    try:
        station_id, lat, lon, w_type = LOC_DATA[name]
        
        # USGS Level with extended 15s timeout
        u_url = f"https://waterservices.usgs.gov/nwis/iv/?format=json&sites={station_id}&parameterCd=00065"
        level_data = requests.get(u_url, timeout=15).json()
        level = level_data['value']['timeSeries'][0]['values'][0]['value'][0]['value']
        
        # Weather / Pressure
        headers = {'User-Agent': 'StrikeLogic'}
        grid = requests.get(f"https://api.weather.gov/points/{lat},{lon}", headers=headers, timeout=10).json()
        fc = requests.get(grid['properties']['forecast'], headers=headers, timeout=10).json()['properties']['periods'][0]
        p = 30.05 
        
        st.write(f"**GAGE HEIGHT:** {level} FT")
        st.write(f"**WEATHER:** {fc['shortForecast']} | {fc['temperature']}°F")
        st.write(f"**PRESSURE:** {p} inHg")
        score = 5 if 29.80 <= p <= 30.20 else 2
        st.write(f"**PREDICTION:** {score}/5")
        st.markdown("---")
        
        strat = TACTICS.get(species, {}).get(w_type, ["1. Search.", "2. Search.", "3. Change Location."])
        st.subheader("STRATEGIES")
        for s in strat: st.write(s)
        
        st.markdown("---")
        p_note = "Good Pressure Range (29.80-30.20): Optimal." if 29.80 <= p <= 30.20 else "LOCKJAW RANGE (30.21-30.50+): High pressure, slow activity."
        st.write(f"**BARO NOTE:** {p_note}")
    except Exception as e:
        st.error(f"Data feed delay. Please try again. Error: {e}")
