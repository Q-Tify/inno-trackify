import streamlit as st
import pandas as pd
from datetime import date, time
from config import API_URL
import requests



if "dataset" not in st.session_state:
    st.session_state["dataset"] = None

if "activity_option" not in st.session_state:
    st.session_state["activity_option"] = "All"

if "date_option" not in st.session_state:
    st.session_state["date_option"] = None

def update():
    st.session_state["dataset"] = load_data(st.session_state["activity_option"], st.session_state["date_option"])

def get_activity_icon(activity_type):
    for activity in activity_types:
        if activity["id"] == activity_type:
            return activity["icon_name"]

def form_dataframe(response):
    icons = []
    activity_names = []
    durations = []
    dates = []

    for activity in response:
        icons.append(get_activity_icon(activity["type_id"]))
        activity_names.append(activity["name"])
        durations.append(activity["duration"])
        dates.append(activity["start_time"])

    return {"icon": icons, "activity_name": activity_names, "duration": durations, "date": dates}

def get_activity_option(activity_option):
    for activity in activity_types:
        if activity["name"] == activity_option:
            print(activity["id"])
            return activity["id"]

st.title("Activities")

if "session_token" not in st.session_state:
    st.session_state["session_token"] = None

if st.session_state['session_token']:
    def load_data(activity_option, date_option):
        url = f"{API_URL}/activities/"
        data = None

        if activity_option == "All":
            if date_option == None:
                data = {}
            else:
                data = {"date": date_option}
        else:
            if date_option == None:
                data = {"type" : activity_option}
            else:
                data = {"date": date_option, "type" : activity_option}
       

        headers = {"Authorization": f"Bearer {st.session_state['session_token']}"}
        response = requests.put(url, headers=headers, params=data)

        return pd.DataFrame(form_dataframe(response.json()))

    def split_frame(input_df, rows):
        df = [
            input_df.loc[i: i + rows - 1, :]
            for i in range(0, len(input_df), rows)
        ]
        return df

    col1, col2 = st.columns([0.5, 0.5], gap="small")

    with col1:
        st.session_state["activity_option"] = st.selectbox(
            "Filter by activity", ("All", "Sport", "Health", "Sleep", "Study", "Rest", "Eat", "Coding", "Other"),
            on_change=update
        )

    with col2:
        st.session_state["date_option"] = st.date_input("Filter by date:", value=None, format="YYYY.MM.DD", on_change=update)

    st.session_state["dataset"] = load_data(st.session_state["activity_option"], st.session_state["date_option"])
    pagination = st.container()

    bottom_menu = st.columns((4, 1.5, 1))
    with bottom_menu[2]:
        batch_size = st.selectbox("Page Size", options=[5, 10])
    with bottom_menu[1]:
        total_pages = (
            int(len(st.session_state["dataset"]) / batch_size)
            if int(len(st.session_state["dataset"]) / batch_size) > 0
            else 1
        )
        current_page = st.number_input(
            "Page", min_value=1, max_value=total_pages, step=1
        )
    with bottom_menu[0]:
        st.markdown(f"Page **{current_page}** of **{total_pages}** ")

    pages = split_frame(st.session_state["dataset"], batch_size)

    if pages:
        pagination.dataframe(
            data=pages[current_page - 1],
            column_config={
                "icon": st.column_config.ImageColumn(
                    "Icon",
                    help="Streamlit app preview screenshots",
                    width="small",
                ),
                "activity_name": st.column_config.TextColumn(
                    "Activity",
                    help="Streamlit **widget** commands 🎈",
                    default="",
                    max_chars=50,
                    width="medium",
                ),
                "duration": st.column_config.TextColumn(
                    "Activity",
                    default="",
                    max_chars=50,
                    width="medium",
                ),
                "date": st.column_config.TextColumn(
                    "Activity",
                    default="",
                    max_chars=50,
                    width="medium",
                ),
            },
            hide_index=True,
            use_container_width=True,
        )
else:
    st.error("Please, login to your user account.")
