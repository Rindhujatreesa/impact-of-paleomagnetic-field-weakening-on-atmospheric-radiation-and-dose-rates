import streamlit as st
import sys
import os
import numpy as np
import asyncio
import plotly.express as px
# from src.lscoefs import get_coeffs_at_age

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

st.set_page_config(layout="wide")

st.title("Geomagnetic Dashboard")

page = st.sidebar.radio(
    "Select Module",
    ["Global Map with Rigidity Cut off", "Dipole Field Intensity Map", "Cosmic Ray Ionization"]
)
# 1. Global Map with Rigidity Cut off
if page == "Global Map with Rigidity Cut off":
    from map_view import global_view as run
    run()

# 2. Dipole Field Intensity Map
elif page == "Dipole Field Intensity Map":
    from dipole_field import intensity
    from src.lscoefs import get_coeffs_at_age
    st.title("Dipole Field Intensity Map")

    age = st.slider("Age (ka BP)", 30.00, 49.95, 41.12)
    st.write(f"Age: {age} ka BP")
    g, h = get_coeffs_at_age(age)
    
    intensity(g, h)

# 3. Cosmic Ray Induced Ionization
elif page == "Cosmic Ray Ionization":
    from crii_model import crii_model

    crii_model()
    