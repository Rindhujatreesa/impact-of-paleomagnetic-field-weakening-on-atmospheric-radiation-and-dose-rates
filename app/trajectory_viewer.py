import streamlit as st
import plotly.graph_objects as go
import numpy as np
from OTSO._trajectory import trajectory

def trajectory():
    st.title("🧭 Particle Trajectory Viewer")

    stations_list = ["OULU","ROME","ATHN","CALG"]

    trajectories = trajectory(
        Stations=stations_list,
        rigidity=5,
        computation_params={"corenum":1}
    )

    st.write(type(trajectories[0]))
    st.write(trajectories[0].keys())
    # Example trajectory (replace with OTSO output)
    # x, y, z = get_trajectory()

    # # Dummy trajectory (replace later)

    # t = np.linspace(0, 10, 500)
    # x = 5 * np.cos(t)
    # y = 5 * np.sin(t)
    # z = 0.5 * t


    # # Earth sphere

    # u = np.linspace(0, 2*np.pi, 50)
    # v = np.linspace(0, np.pi, 50)

    # xe = np.outer(np.cos(u), np.sin(v))
    # ye = np.outer(np.sin(u), np.sin(v))
    # ze = np.outer(np.ones(np.size(u)), np.cos(v))


    # fig = go.Figure()

    # # Earth
    # fig.add_trace(go.Surface(
    #     x=xe, y=ye, z=ze,
    #     colorscale="Blues",
    #     opacity=0.6,
    #     showscale=False
    # ))

    # # Trajectory
    # fig.add_trace(go.Scatter3d(
    #     x=x, y=y, z=z,
    #     mode='lines',
    #     line=dict(width=4, color='red'),
    #     name="Particle Path"
    # ))


    # # Layout

    # fig.update_layout(
    #     scene=dict(
    #         xaxis_title="X (Re)",
    #         yaxis_title="Y (Re)",
    #         zaxis_title="Z (Re)",
    #         aspectmode="data"
    #     ),
    #     margin=dict(l=0, r=0, t=40, b=0)
    # )

    # st.plotly_chart(fig, use_container_width=True)