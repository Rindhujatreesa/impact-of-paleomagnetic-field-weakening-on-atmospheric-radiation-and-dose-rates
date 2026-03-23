import streamlit as st
import sys
import os
import numpy as np
import asyncio
# from src.lscoefs import get_coeffs_at_age

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

st.set_page_config(layout="wide")

st.title("Geomagnetic Cutoff Dashboard")

page = st.sidebar.radio(
    "Select Module",
    ["Global Map with Rigidity Cut off", "Dipole Field Intensity Map", "Penumbra", "Trajectory Viewer"]
)

if page == "Global Map with Rigidity Cut off":
    from map_view import global_view as run
    run()
elif page == "Dipole Field Intensity Map":
    from dipole_field import intensity
    from src.lscoefs import get_coeffs_at_age
    st.title("🌍 Dipole Field Intensity Map")

    # @st.cache_data
    # def cached_get_coeffs(age):
    #     return get_coeffs_at_age(age)

    age = st.slider("Age (ka BP)", 30.00, 49.95, 41.12)
    st.write(f"Age: {age} ka BP")
    g, h = get_coeffs_at_age(age)
    
    intensity(g, h)

# elif page == "Penumbra":
#     from app.penumbra import run
# elif page == "Trajectory Viewer":
#     from app.trajectory import run

# run()