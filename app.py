import streamlit as st
import folium
import json
import time
from streamlit_folium import st_folium

st.set_page_config(page_title="SkyRoute AI - Advanced Demo", layout="wide")
st.title("SkyRoute AI - Advanced Drone Mission Planner")
st.write("This version shows flight simulation with battery, speed, altitude, return home, and emergency landing.")

with open("map_data.json", "r") as file:
    mission_data = json.load(file)

start = mission_data["start"]
goal = mission_data["goal"]
obstacles = mission_data["obstacles"]
no_fly_zones = mission_data["no_fly_zones"]
route = mission_data["route"]

if "mission_started" not in st.session_state:
    st.session_state.mission_started = False
if "step" not in st.session_state:
    st.session_state.step = 0
if "battery" not in st.session_state:
    st.session_state.battery = 100
if "altitude" not in st.session_state:
    st.session_state.altitude = 0
if "speed" not in st.session_state:
    st.session_state.speed = 0
if "status_text" not in st.session_state:
    st.session_state.status_text = "Drone ready for takeoff."

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Start Mission"):
        st.session_state.mission_started = True
        st.session_state.step = 0
        st.session_state.battery = 100
        st.session_state.altitude = 10
        st.session_state.speed = 12
        st.session_state.status_text = "Mission started. Drone is flying."

with col2:
    if st.button("Reset Mission"):
        st.session_state.mission_started = False
        st.session_state.step = 0
        st.session_state.battery = 100
        st.session_state.altitude = 0
        st.session_state.speed = 0
        st.session_state.status_text = "Mission reset."

with col3:
    if st.button("Return Home"):
        st.session_state.mission_started = False
        st.session_state.step = 0
        st.session_state.altitude = 10
        st.session_state.speed = 10
        st.session_state.status_text = "Return-to-home activated."

with col4:
    if st.button("Emergency Land"):
        st.session_state.mission_started = False
        st.session_state.altitude = 0
        st.session_state.speed = 0
        st.session_state.status_text = "Emergency landing executed."

current_position = route[st.session_state.step]

center_lat = (start[0] + goal[0]) / 2
center_lon = (start[1] + goal[1]) / 2

m = folium.Map(location=[center_lat, center_lon], zoom_start=15)

folium.Marker(
    location=start,
    popup="Start Point",
    tooltip="Start Point",
    icon=folium.Icon(color="green", icon="play")
).add_to(m)

folium.Marker(
    location=goal,
    popup="Goal Point",
    tooltip="Goal Point",
    icon=folium.Icon(color="red", icon="flag")
).add_to(m)

for obs in obstacles:
    folium.Marker(
        location=obs,
        popup="Obstacle",
        tooltip="Obstacle",
        icon=folium.Icon(color="black", icon="warning-sign")
    ).add_to(m)

for zone in no_fly_zones:
    folium.Circle(
        location=zone,
        radius=80,
        popup="No-Fly Zone",
        color="red",
        fill=True,
        fill_opacity=0.4
    ).add_to(m)

folium.PolyLine(
    locations=route,
    color="blue",
    weight=5,
    tooltip="Planned Route"
).add_to(m)

folium.Marker(
    location=current_position,
    popup="Drone Position",
    tooltip="Drone",
    icon=folium.Icon(color="blue", icon="send")
).add_to(m)

st.subheader("Mission Map")
st_folium(m, width=1000, height=600, key=f"map_{st.session_state.step}")

metric1, metric2, metric3, metric4 = st.columns(4)
metric1.metric("Battery", f"{st.session_state.battery}%")
metric2.metric("Speed", f"{st.session_state.speed} m/s")
metric3.metric("Altitude", f"{st.session_state.altitude} m")
metric4.metric("Step", f"{st.session_state.step + 1}/{len(route)}")

st.subheader("Flight Status")
st.write(f"**Drone Position:** {current_position}")
st.write(f"**Mission Status:** {st.session_state.status_text}")

if st.session_state.step >= len(route) - 1 and st.session_state.mission_started:
    st.session_state.mission_started = False
    st.session_state.speed = 0
    st.session_state.altitude = 0
    st.session_state.status_text = "Drone reached destination successfully."
    st.success("Drone reached the destination.")

st.subheader("Mission Details")
st.write(f"**Start Coordinates:** {start}")
st.write(f"**Goal Coordinates:** {goal}")
st.write(f"**Obstacle Points:** {obstacles}")
st.write(f"**No-Fly Zones:** {no_fly_zones}")

if st.session_state.mission_started and st.session_state.step < len(route) - 1:
    time.sleep(1)
    st.session_state.step += 1
    st.session_state.battery = max(0, st.session_state.battery - 5)
    st.session_state.altitude = 10
    st.session_state.speed = 12
    st.rerun()