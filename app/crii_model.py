import os
import numpy as np
import pandas as pd
from scipy.interpolate import RegularGridInterpolator
import streamlit as st
import plotly.express as px


# DATA_DIR = "/Users/rindhujajohnson/Documents/GitHub/paleomagnetic/data"
DATA_DIR = os.path.dirname(os.path.dirname(__file__))
CRII_DIR = os.path.join(DATA_DIR, "data", "CRII_tables")
RC_FILE = os.path.join(DATA_DIR, "data", "rigidity_cutoff_values.csv")


# LOAD Rc DATA for the selected altitude across the (lat, lon) points to plot on the graph

@st.cache_data
def load_rc_data():
    df = pd.read_csv(RC_FILE)
    df.columns = df.columns.str.strip()

    lats = np.sort(df["Latitude"].unique())
    lons = np.sort(df["Longitude"].unique())
    alts = np.sort(df["Altitude"].unique())

    Rc_grid = np.zeros((len(lats), len(lons), len(alts)))

    for i, lat in enumerate(lats):
        for j, lon in enumerate(lons):
            for k, alt in enumerate(alts):
                Rc_grid[i, j, k] = df[
                    (df["Latitude"] == lat) &
                    (df["Longitude"] == lon) &
                    (df["Altitude"] == alt)
                ]["Rc"].values[0]

    interp = RegularGridInterpolator(
        (lats, lons, alts),
        Rc_grid,
        bounds_error=False,
        fill_value=None
    )

    return interp, lats, lons, alts


# Get a list of the CRII tables to ensure no runtime happens when the user selects an atmospheric depth

def get_depth_files():
    files = [f for f in os.listdir(CRII_DIR) if f.endswith(".RES")]
    
    depth_map = {}
    for f in files:
        try:
            val = int(f.split("_")[1].split(".")[0])
            depth = val / 100.0
            depth_map[depth] = f
        except:
            continue

    depths = sorted(depth_map.keys())
    return depths, depth_map


# Load the necessary CRII table to obtain the value for corresponding Rc and phi

@st.cache_data
def load_crii(filepath):
    with open(filepath) as f:
        lines = f.readlines()

    phi_vals = np.array([float(x) for x in lines[0][2:].split()])

    Pc_vals, CRII = [], []
    for line in lines[1:]:
        parts = line.split()
        Pc_vals.append(float(parts[0]))
        CRII.append([float(x) for x in parts[1:]])

    Pc_vals = np.array(Pc_vals)
    CRII = np.array(CRII)

    interp = RegularGridInterpolator(
        (Pc_vals, phi_vals),
        CRII,
        bounds_error=False,
        fill_value=None
    )

    return interp


# the executable function

def crii_model():

    st.title("CR Induced Ionization & Rc Map")

    # Load Rc interpolator
    Rc_interp, lats, lons, alts = load_rc_data()

    
    # Sidebar Controls
    
    depths, depth_map = get_depth_files()

    selected_depth = st.sidebar.select_slider(
        "Atmospheric Depth (g/cm²)",
        options=depths,
        value=depths[len(depths)//2]
    )

    phi = st.sidebar.slider("Solar Modulation Φ (MV)", 0, 1500, 500)

    altitude = st.sidebar.slider(
        "Altitude (km)",
        float(min(alts)),
        float(max(alts)),
        float(alts[len(alts)//2])
    )

    mode = st.sidebar.radio(
    "Scenario",
    ["Present", "Excursion", "Enhancement (Exc/Present)"]
    )
    
    # Load CRII file
    
    filename = depth_map[selected_depth]
    filepath = os.path.join(CRII_DIR, filename)

    crii_interp = load_crii(filepath)

    st.sidebar.write(f"Using file: {filename}")

    
    # Compute Grid
    
    lat_grid = lats
    lon_grid = lons

    CRII_present = np.zeros((len(lat_grid), len(lon_grid)))
    CRII_exc = np.zeros_like(CRII_present)
    Rc_map = np.zeros_like(CRII_present)

    with st.spinner("Computing map..."):

        for i, lat in enumerate(lat_grid):
            for j, lon in enumerate(lon_grid):

                Rc = Rc_interp([[lat, lon, altitude]])[0]
                Rc_map[i, j] = Rc

                # Present
                CRII_present[i, j] = crii_interp([[Rc, phi]])[0]

                # Excursion (dipole collapse)
                Rc_exc = 0.2 * Rc
                CRII_exc[i, j] = crii_interp([[Rc_exc, phi]])[0]

    # choose the data to plot based on the scenario

    if mode == "Present":
        plot_data = CRII_present
        title = "CRII (Present Day)"

    elif mode == "Excursion":
        plot_data = CRII_exc
        title = "CRII (Excursion)"

    else:
        plot_data = CRII_exc / CRII_present
        title = "CRII Enhancement (Excursion / Present)"
    
    # Plot
    
    lat_flat = np.repeat(lat_grid, len(lon_grid))
    lon_flat = np.tile(lon_grid, len(lat_grid))
    CRII_flat = plot_data.flatten()
    Rc_flat = Rc_map.flatten()

    # Normalize Rc for marker size
    Rc_norm = (Rc_flat - Rc_flat.min()) / (Rc_flat.max() - Rc_flat.min() + 1e-8)
    marker_size = 4 + 12 * Rc_norm   # allows scaling w.r.t Rc

    # Rc_flat = np.asarray(Rc_flat).flatten()
    # custom_data = Rc_flat.reshape(-1, 1)
    
    # Build DataFrame
    plot_df = pd.DataFrame({
        "lat": lat_flat,
        "lon": lon_flat,
        "CRII": CRII_flat,
        "Rc": Rc_flat,
        "size": marker_size
    })

    fig = px.scatter_geo(
        plot_df,
        lat="lat",
        lon="lon",
        color="CRII",
        size="size",
        projection="natural earth",
        color_continuous_scale="Turbo",
        labels={"CRII": "CRII Value"},
        custom_data=["Rc"]   
    )


    fig.update_traces(
        hovertemplate=
            "Lat: %{lat:.2f}<br>" +
            "Lon: %{lon:.2f}<br>" +
            "CRII Value: %{marker.color:.3e}<br>" +
            "Rc: %{customdata[0]:.2f} GV"
    )

    fig.update_layout(
        title=title,
        geo = dict(
            showland = True,
            landcolor = "green",
            bgcolor = "skyblue",
            showcountries = True
        )
    )

    st.plotly_chart(fig, width="stretch")

    fig = px.imshow(
    plot_data,
    x=lon_grid,
    y=lat_grid,
    origin="lower",
    color_continuous_scale="Turbo",
    aspect="auto",
    labels={"color": "CRII Value"}
    )

    fig.update_layout(
        title=title,
        xaxis_title="Longitude",
        yaxis_title="Latitude"
    )

    st.plotly_chart(fig, width="stretch")

    with st.expander("Show Data"):
        st.dataframe(plot_data)