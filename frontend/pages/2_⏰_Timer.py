import streamlit as st
import time
from utils.functions import format_time
from config import API_URL
import requests
from datetime import datetime
from utils.functions import activity_types

def get_activity_option(activity_option):
    for activity in activity_types:
        if activity["name"] == activity_option:
            print(activity["id"])
            return activity["id"]

def add_activity(activity_name, type_id, user_id, start_time, end_time, duration, description):
    url = f"{API_URL}/activities/"
    data = {"name": activity_name,
            "type_id": type_id,
            "user_id": user_id,
            "start_time": datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S'),
            "end_time": datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S'),
            "duration": datetime.fromtimestamp(duration).strftime('%H:%M:%S'),
            "description": description}

    headers = {"Authorization": f"Bearer {st.session_state['session_token']}"}
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def render_timer(seconds):
    _, col2, _ = st.columns([0.4, 0.2, 0.4], gap="small")

    with col2:
        st.markdown("### {}".format(format_time(int(seconds))))


st.title("Track activity")

if "session_token" not in st.session_state:
    st.session_state["session_token"] = None


if st.session_state['session_token']:
    activity_added = False
    activity_error = False
    elapsed_time = 0
    if "start_time" not in st.session_state:
        st.session_state["start_time"] = time.time()

    if "timer_running" not in st.session_state:
        st.session_state["timer_running"] = False

    if "elapsed_time" not in st.session_state:
        st.session_state["elapsed_time"] = 0

    if "paused_time" not in st.session_state:
        st.session_state["paused_time"] = 0

    if "is_stopped" not in st.session_state:
        st.session_state["is_stopped"] = False

    col1, col2, col3 = st.columns([0.65, 0.2, 0.15], gap="small")

    with col1:
        activity_name = st.text_input(
            "Activity name:",
            value="",
            label_visibility="collapsed",
            placeholder="Input activity name...",
        )

    with col2:
        activity_option = st.selectbox(
            "Activity type", ("Sport", "Health", "Sleep", "Study", "Rest", "Eat", "Coding", "Other"), label_visibility="collapsed"
        )

    with col3:
        if st.button("Save"):
            if activity_name:
                add_activity(activity_name, get_activity_option(activity_option), st.session_state["user_id"], st.session_state["start_time"], st.session_state["start_time"]+st.session_state["elapsed_time"], st.session_state["elapsed_time"], "")
                if not activity_added:
                    activity_added = not activity_added
            else:
                if not activity_error:
                    activity_error = not activity_error

    st.container(height=1, border=False)

    col0, col1, col2, col3, col4 = st.columns(
        [0.315, 0.115, 0.115, 0.115, 0.35], gap="small"
    )

    placeholder = st.empty()
    
    if activity_added:
        activity_added = not activity_added
        st.success("Activity added.")
    
    if activity_error:
        activity_error = not activity_error
        st.error("Please, enter activity name.")

    # Убирать кнопку play при нажатии
    with col1:
        if st.button("Play"):
            st.session_state["start_time"] = time.time()
            st.session_state["timer_running"] = True
            st.session_state["is_stopped"] = False

    with col2:
        if st.button("Stop"):
            st.session_state["timer_running"] = False
            st.session_state["is_stopped"] = True
            st.session_state["paused_time"] = 0

    with col3:
        if st.button("Pause"):
            st.session_state["timer_running"] = False
            st.session_state["is_stopped"] = True
            st.session_state["paused_time"] = st.session_state["elapsed_time"]

    with placeholder.container():
        render_timer(st.session_state["elapsed_time"])

    # Timer

    while st.session_state["timer_running"]:
        st.session_state["elapsed_time"] = (
            st.session_state["paused_time"] + time.time() - st.session_state["start_time"]
        )

        with placeholder.container():
            render_timer(st.session_state["elapsed_time"])

        if not st.session_state["timer_running"]:
            break

        time.sleep(1)
        placeholder.empty()
else:
    st.error("Please, login to your user account.")
    # st.page_link("pages/page_1.py", label="Page 1", icon="1️⃣")
