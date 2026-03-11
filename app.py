import streamlit as st

st.title("The Posse Shope: 3D Generator")

# User Inputs (The "Sliders" for your app)
st.sidebar.header("Design Parameters")
width = st.sidebar.slider("Card Width (mm)", 50, 150, 92)
depth = st.sidebar.slider("Card Depth (mm)", 10, 50, 15)
angle = st.sidebar.slider("Lean Angle (degrees)", 0, 45, 15)

# The OpenSCAD Template
scad_code = f"""
width = {width};
depth = {depth};
angle = {angle};
wall = 2.5;
height = 35;

difference() {{
    rotate([angle, 0, 0])
    cube([width + (wall * 2), depth + (wall * 2), height + wall]);
    
    translate([wall, wall, wall])
    rotate([angle, 0, 0])
    cube([width, depth, height + wall + 5]);
}}
"""

st.code(scad_code, language="scad")

# Download button for the file
st.download_button(
    label="Download .scad file",
    data=scad_code,
    file_name="posse_design.scad",
    mime="text/plain"
)
