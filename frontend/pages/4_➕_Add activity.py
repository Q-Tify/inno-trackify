import streamlit as st

st.title("Add activity")


if 'session_token' not in st.session_state:
    st.session_state['session_token'] = None

if st.session_state['session_token']:
    activity_name = st.text_input("Activity name:", value="", label_visibility="collapsed",placeholder="Input activity name...")
    col1, col2, col3, col4 = st.columns([0.2, 0.5, 0.2, 0.2], gap="small")



    with col1:
        if st.button('Choose icon'):
            pass

    with col2:
        duration = st.text_input("Duration:", value="", label_visibility="collapsed", placeholder="XX:XX:XX")

    with col3:
        date = st.date_input("Date", value=None, format="DD.MM.YYYY", label_visibility="collapsed")

    with col4:
        if st.button('Add activity'):
            if activity_name == "":
                st.write("Please, enter activity name.")
else:
    st.error("Please, login to your user account.")
