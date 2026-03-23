import streamlit as st
from src.geomagnetic_components import compute_dipole_field
import numpy as np
import plotly.express as px

def intensity(g, h):

    lats = np.linspace(-90, 90, 181)
    lons = np.linspace(-180, 180, 361)

    LAT, LON = np.meshgrid(lats, lons, indexing = "ij")

    Bmap = compute_dipole_field(LAT, LON, g, h)


    fig = px.imshow(
        Bmap,
        x=lons,
        y=lats,
        origin="lower",
        color_continuous_scale="Turbo",
        labels=dict(color="|B| (nT)")
    )

    fig.update_layout(
        title="Dipole Magnetic Field Intensity",
        xaxis_title="Longitude",
        yaxis_title="Latitude"
    )

    st.plotly_chart(fig, width ="stretch")

    with st.expander("Show Magnetic Field intensity"):
        st.dataframe(Bmap)
    with st.expander("Show g, h values"):
        st.dataframe([g,h])