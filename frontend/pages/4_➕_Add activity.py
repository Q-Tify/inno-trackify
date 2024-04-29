import streamlit as st
from config import API_URL
import requests

activity_types = [
    {"id": 1, "name": "Sport", "icon_name": "https://raw.githubusercontent.com/Wild-Queue/inno-trackify-icons/main/Sport.jpg"},
    {"id": 2, "name": "Health", "icon_name": "https://raw.githubusercontent.com/Wild-Queue/inno-trackify-icons/main/Health.jpg"},
    {"id": 3, "name": "Sleep", "icon_name": "https://raw.githubusercontent.com/Wild-Queue/inno-trackify-icons/main/Sleep.jpg"},
    {"id": 4, "name": "Study", "icon_name": "https://raw.githubusercontent.com/Wild-Queue/inno-trackify-icons/main/Study.jpg"},
    {"id": 5, "name": "Rest", "icon_name": "https://raw.githubusercontent.com/Wild-Queue/inno-trackify-icons/main/Rest.jpg"},
    {"id": 6, "name": "Eat", "icon_name": "https://raw.githubusercontent.com/Wild-Queue/inno-trackify-icons/main/Eat.jpg"},
    {"id": 7, "name": "Coding", "icon_name": "https://raw.githubusercontent.com/Wild-Queue/inno-trackify-icons/main/Coding.jpg"},
    {"id": 8, "name": "Other", "icon_name": "https://raw.githubusercontent.com/Wild-Queue/inno-trackify-icons/main/Other.jpg"},
]

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
            "start_time": start_time,
            "end_time": end_time,
            "duration": duration,
            "description": description}

    headers = {"Authorization": f"Bearer {st.session_state['session_token']}"}
    response = requests.post(url, headers=headers, json=data)
    return response.json()

st.title("Add activity")


if 'session_token' not in st.session_state:
    st.session_state['session_token'] = None

if st.session_state['session_token']:
    activity_added = False
    activity_error = False

    activity_name = st.text_input("Activity name:", value="", label_visibility="collapsed",placeholder="Input activity name...")
    col1, col2, col3, col4 = st.columns([0.2, 0.4, 0.3, 0.2], gap="small")



    with col1:
        activity_type = st.selectbox(
            "Activity type", ("Sport", "Health", "Sleep", "Study", "Rest", "Eat", "Coding", "Other"), label_visibility="collapsed"
        )

    with col2:
        duration = st.text_input("Duration:", value="", label_visibility="collapsed", placeholder="XX:XX:XX")

    with col3:
        date = st.date_input("Date", value=None, format="YYYY.MM.DD", label_visibility="collapsed")

    with col4:
        if st.button('Add activity'):
            if activity_name == "":
                if not activity_error:
                    activity_error = not activity_error
            else:
                if not activity_added:
                    activity_added = not activity_added
                
                add_activity(activity_name, get_activity_option(activity_type), st.session_state["user_id"], f"{date} {duration}", f"{date} {duration}", duration, "")
                # add_activity(activity_name, get_activity_option(activity_type), user_id, start_time, end_time, duration, description)
    
    if activity_added:
        activity_added = not activity_added
        st.success("Activity added.")
    
    if activity_error:
        activity_error = not activity_error
        st.error("Please, enter activity name.")
else:
    st.error("Please, login to your user account.")
