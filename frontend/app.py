import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("InnoTrackify")


def fetch_activities():
    response = requests.get(f"{API_URL}/activities")
    if response.status_code == 200:
        return response.json()
    else:
        return None


def display_activities(activities):
    st.write("## Activities")
    if activities:
        for activity in activities:
            st.write(f"- {activity['name']}")


activities = fetch_activities()
display_activities(activities)
