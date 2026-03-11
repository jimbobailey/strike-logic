import streamlit as st
import requests

# =========================================================
# PAGE CONFIG / BRANDING
# =========================================================
LOGO_URL = "https://raw.githubusercontent.com/jimbobailey/strikelogic/mainsl/strikelogic.png"

st.set_page_config(
    page_title="STRIKE LOGIC",
    page_icon=LOGO_URL,
    layout="wide"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #0B0B0B;
        color: #FFFFFF;
    }

    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    h1, h2, h3 {
        color: #FF6A00 !important;
        text-shadow: 0 0 8px rgba(255,106,0,0.35);
    }

    .stButton > button {
        background: linear-gradient(180deg, #ff7a1a 0%, #ff4d00 100%);
        color: white;
        font-weight: 800;
        border: 1px solid #ff7a1a;
        border-radius: 12px;
        padding: 0.7rem 1.2rem;
        box-shadow: 0 0 14px rgba(255,106,0,0.35);
    }

    .stButton > button:hover {
        border-color: #ffa366;
        box-shadow: 0 0 18px rgba(255,106,0,0.55);
    }

    div[data-baseweb="select"] > div {
        background-color: #151515 !important;
        border: 1px solid #333 !important;
        border-radius: 10px !important;
        color: white !important;
    }

    .metric-card {
        background: #121212;
        border: 1px solid #2a2a2a;
        border-radius: 16px;
        padding: 16px 18px;
        box-shadow: 0 0 18px rgba(255,106,0,0.10);
        margin-bottom: 12px;
    }

    .metric-title {
        font-size: 0.95rem;
        color: #ff9a52;
        font-weight: 700;
        margin-bottom: 6px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .metric-value {
        font-size: 1.2rem;
        font-weight: 800;
        color: #ffffff;
    }

    .strategy-card {
        background: #121212;
        border: 1px solid #2a2a2a;
        border-left: 4px solid #ff6a00;
        border-radius: 14px;
        padding: 12px 14px;
        margin-bottom: 10px;
        box-shadow: 0 0 14px rgba(255,106,0,0.08);
    }

    .small-note {
        color: #bbbbbb;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# =========================================================
# DATA
# =========================================================
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
        "River": [
            "1. 3/8oz Jig & Craw in current seams.",
            "2. Topwater frog over grassy banks.",
            "3. (Dead Bite) Downsize to 4in finesse worm, slow drag."
        ],
        "Lake": [
            "1. Deep diving crankbait on main lake points.",
            "2. Senko Wacky-rig around boat docks.",
            "3. (Dead Bite) Drop-shot in 15ft+ near structure."
        ],
        "Creek": [
            "1. Spinnerbait along wood structure.",
            "2. Jerkbait in pockets.",
            "3. (Dead Bite) Weightless soft-plastic jerkbait, dead-sticking."
        ]
    },
    "Shellcracker": {
        "River": [
            "1. Red wigglers on bottom in backwater eddies.",
            "2. Small beetle-spin near lily pads.",
            "3. (Dead Bite) Cast beyond bed and drag slowly."
        ],
        "Lake": [
            "1. Earthworms near shell beds.",
            "2. Hybrid redworms on drop-offs.",
            "3. (Dead Bite) Light split-shot, long leader."
        ],
        "Creek": [
            "1. Crickets near overhanging limbs.",
            "2. Wax worms in eddies.",
            "3. (Dead Bite) Switch to micro-jigging."
        ]
    },
    "Channel/Blue Catfish": {
        "River": [
            "1. Cut shad on deep bottom bends.",
            "2. Chicken liver in slow pools.",
            "3. (Dead Bite) High-scent dip bait, stationary."
        ],
        "Lake": [
            "1. Drift fishing shad on flats.",
            "2. Punch bait near drop-offs.",
            "3. (Dead Bite) Live bluegill, anchored."
        ],
        "Creek": [
            "1. Nightcrawlers on deep holes.",
            "2. Cut bait near feeder mouths.",
            "3. (Dead Bite) Increase scent profile."
        ]
    },
    "Shoal Bass": {
        "River": [
            "1. Topwater walker in current breaks.",
            "2. Craw-pattern crankbait on rocks.",
            "3. (Dead Bite) Small tube jig, bottom bounce."
        ],
        "Lake": ["N/A", "N/A", "N/A"],
        "Creek": [
            "1. Spinnerbait in eddies.",
            "2. Fluke on light lead.",
            "3. (Dead Bite) Micro-jig, slow drift."
        ]
    },
    "Black Crappie": {
        "River": [
            "1. Vertical jigging timber.",
            "2. Minnow under slip float.",
            "3. (Dead Bite) Trolling slow with small curly tails."
        ],
        "Lake": [
            "1. Minnows over brush piles.",
            "2. Chartreuse jigs in coves.",
            "3. (Dead Bite) Slow vertical jigging."
        ],
        "Creek": [
            "1. Small tube jigs near wood.",
            "2. Beetle-spin slow roll.",
            "3. (Dead Bite) Live minnow, dead-sticking."
        ]
    }
}

# =========================================================
# HEADER
# =========================================================
st.image(LOGO_URL, use_container_width=True)
st.markdown("<h1 style='margin-top:0;'>STRIKE LOGIC</h1>", unsafe_allow_html=True)
st.markdown(
    "<div class='small-note'>HYDROMETRIC ANGLING INTELLIGENCE</div>",
    unsafe_allow_html=True
)

# =========================================================
# INPUTS
# =========================================================
col1, col2 = st.columns(2)

with col1:
    name = st.selectbox("LOCATION", list(LOC_DATA.keys()))

with col2:
    species = st.selectbox("SPECIES", list(TACTICS.keys()))

# =========================================================
# ANALYZE BUTTON
# =========================================================
if st.button("ANALYZE"):
    sid, lat, lon, w_type = LOC_DATA[name]

    # USGS Water Level
    level = "Data Unavailable"
    try:
        usgs_url = f"https://waterservices.usgs.gov/nwis/iv/?format=json&sites={sid}&parameterCd=00065"
        resp = requests.get(usgs_url, timeout=8).json()
        ts = resp.get("value", {}).get("timeSeries", [])
        if (
            ts
            and len(ts) > 0
            and "values" in ts[0]
            and len(ts[0]["values"]) > 0
            and len(ts[0]["values"][0].get("value", [])) > 0
        ):
            level = f"{ts[0]['values'][0]['value'][0]['value']} FT"
    except Exception:
        pass

    # Weather
    weather_res = "Data Unavailable"
    try:
        headers = {"User-Agent": "StrikeLogic"}
        grid = requests.get(
            f"https://api.weather.gov/points/{lat},{lon}",
            timeout=8,
            headers=headers
        ).json()

        forecast_url = grid["properties"]["forecast"]
        fc = requests.get(
            forecast_url,
            timeout=8,
            headers=headers
        ).json()["properties"]["periods"][0]

        weather_res = f"{fc['shortForecast']} | {fc['temperature']}°F"
    except Exception:
        pass

    # Placeholder Barometric Pressure
    p = 30.05

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Water Level</div>
            <div class="metric-value">{level}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Weather</div>
            <div class="metric-value">{weather_res}</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Barometric Pressure</div>
            <div class="metric-value">{p} inHg</div>
        </div>
        """, unsafe_allow_html=True)

    if 29.80 <= p <= 30.20:
        st.success("BAROMETRIC PRESSURE NOTE: Good Range (29.80–30.20): Optimal.")
    else:
        st.error("BAROMETRIC PRESSURE NOTE: LOCKJAW RANGE (30.21–30.50+): High pressure, slow activity.")

    st.subheader("STRATEGIES")
    strat = TACTICS[species].get(w_type, ["1. Search."])

    for s in strat:
        st.markdown(f'<div class="strategy-card">{s}</div>', unsafe_allow_html=True)
