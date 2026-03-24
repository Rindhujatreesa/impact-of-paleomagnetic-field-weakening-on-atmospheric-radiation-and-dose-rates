import streamlit as st
import pandas as pd
import plotly.express as px




def global_view():
    """
    Loads the data stored at data/rigidity_cutoff_values.csv for viz
    """
    # Should be replaced with the actual path
    # here, the values are considered only for the date (28/10/2008)
    # see, Section 2 in rigidity_cutoff.ipynb for the steps
    df = pd.read_csv("/Users/rindhujajohnson/Documents/GitHub/paleomagnetic/data/rigidity_cutoff_values.csv")


    # Definig the Slider for Altitude Control
    st.sidebar.title("Controls")

    altitudes = sorted(df["Altitude"].unique())

    # quantity = st.sidebar.selectbox("Select Quantity", ["Rc", "Ru", "Rl"])
    selected_altitude = st.sidebar.slider(
        "Select Altitude",
        min_value = float(min(altitudes)),
        max_value = float(max(altitudes)),
        value = float(altitudes[0]),
        step = float(altitudes[1] - altitudes[0]) if len(altitudes) > 1 else 1.0
    )

    filtered_df = df[df["Altitude"] == selected_altitude]

    st.title(f"Global Cutoff Rigidity (Rc)")
    st.subheader(f"At different Altitudes (30 - 10000 km)")
    st.markdown(f"Date: {df["Date"][0]}")
    st.markdown(f"**Altitude: {selected_altitude} km**")

    # Plot the interactive map

    fig = px.scatter_geo(
        filtered_df,
        lat = "Latitude",
        lon = "Longitude",
        color = "Rc",
        size = "Rc",
        color_continuous_scale = "viridis_r",
        projection = "natural earth2"
    )

    fig.update_layout(
        coloraxis_colorbar = dict(title = "Rc [GV]"),
        margin = dict(l=0, r=0, t=40, b = 0),
        geo = dict(
            showland = True,
            landcolor = "burlywood",
            bgcolor = "azure",
            showcountries = True
        )
    )

    st.plotly_chart(fig, width="stretch")

    with st.expander("Show Data"):
        st.dataframe(filtered_df)
        # st.download_button("Download Figure", fig.to_image(format = "png"))