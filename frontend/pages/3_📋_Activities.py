import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, time

st.title("Activities")

if "session_token" not in st.session_state:
    st.session_state["session_token"] = None

if True or st.session_state["session_token"]:

    @st.cache_data(show_spinner=False)
    def load_data():
        df = pd.DataFrame(
            {
                "icon": [
                    "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/5435b8cb-6c6c-490b-9608-799b543655d3/Home_Page.png",
                    "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/ef9a7627-13f2-47e5-8f65-3f69bb38a5c2/Home_Page.png",
                    "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/31b99099-8eae-4ff8-aa89-042895ed3843/Home_Page.png",
                    "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/6a399b09-241e-4ae7-a31f-7640dc1d181e/Home_Page.png",
                ],
                "activity_name": [
                    "Work",
                    "Job",
                    "Homework",
                    "Gym",
                ],
                "duration": [
                    time(12, 30),
                    time(18, 0),
                    time(9, 10),
                    time(16, 25),
                ],
                "date": [
                    date(1980, 1, 1),
                    date(1990, 5, 3),
                    date(1974, 5, 19),
                    date(2001, 8, 17),
                ],
            }
        )
        return df

    @st.cache_data(show_spinner=False)
    def split_frame(input_df, rows):
        df = [
            input_df.loc[i : i + rows - 1, :]
            for i in range(0, len(input_df), rows)
        ]
        return df

    col1, col2 = st.columns([0.5, 0.5], gap="small")

    with col1:
        activity_option = st.selectbox(
            "Filter by activity", ("All", "Homework", "Job", "Gym")
        )

    with col2:
        date_option = st.selectbox(
            "Filter by date",
            ("All", "Today", "Yesterday", "Last week", "Last month"),
        )

    dataset = load_data()
    pagination = st.container()

    bottom_menu = st.columns((4, 1.5, 1))
    with bottom_menu[2]:
        batch_size = st.selectbox("Page Size", options=[1, 2, 4])
    with bottom_menu[1]:
        total_pages = (
            int(len(dataset) / batch_size)
            if int(len(dataset) / batch_size) > 0
            else 1
        )
        current_page = st.number_input(
            "Page", min_value=1, max_value=total_pages, step=1
        )
    with bottom_menu[0]:
        st.markdown(f"Page **{current_page}** of **{total_pages}** ")

    pages = split_frame(dataset, batch_size)

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
                width="large",
            ),
            "duration": st.column_config.TimeColumn(
                "Duration",
                width="small",
            ),
            "date": st.column_config.DateColumn(
                "Date",
                format="DD.MM.YYYY",
                width="small",
            ),
        },
        hide_index=True,
        use_container_width=True,
    )

    # pagination.dataframe(data=pages[current_page - 1], use_container_width=True)

    # st.write('You selected:', activity_option + " " + date_option)
    # number = st.number_input('Insert a number')
    # st.write('The current number is ', number)
else:
    st.write("Please, login to your user account.")
