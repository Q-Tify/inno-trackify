import streamlit as st
import time 
from utils.functions import format_time



def render_timer(seconds):
    _, col2, _ = st.columns([0.4, 0.2, 0.4], gap="small")

    with col2:        
        st.markdown("### {}".format(format_time(int(seconds))))



st.title('Track activity')
        
if 'session_token' not in st.session_state:
    st.session_state['session_token'] = None


if True or st.session_state['session_token']:
    # start_time = time.time()
    elapsed_time = 0
    if 'start_time' not in st.session_state:
        st.session_state['start_time'] = time.time()

    if 'timer_running' not in st.session_state:
        st.session_state['timer_running'] = False

    if 'elapsed_time' not in st.session_state:
        st.session_state['elapsed_time'] = 0

    if 'paused_time' not in st.session_state:
        st.session_state['paused_time'] = 0

    if 'is_stopped' not in st.session_state:
        st.session_state['is_stopped'] = False


    col1, col2 = st.columns([0.85, 0.15], gap="small")

    with col1:
        activity_name = st.text_input("Activity name:", value="", label_visibility="collapsed",placeholder="Input activity name...")

    with col2:
        if st.button("Save"):
            if activity_name:
                print(activity_name)
            print(st.session_state['elapsed_time'])


    st.container(height=1, border=False)

    col0, col1, col2, col3, col4 = st.columns([0.315, 0.115, 0.115, 0.115, 0.35], gap="small")
            
    placeholder = st.empty()

    #Убирать кнопку play при нажатии
    with col1:
        if st.button("Play"):
            st.session_state['start_time'] = time.time()
            # st.session_state['paused_time'] = 0
            st.session_state['timer_running'] = True
            st.session_state['is_stopped'] = False

    with col2:
        if st.button("Stop"):
            st.session_state['timer_running'] = False
            st.session_state['is_stopped'] = True
            st.session_state['paused_time'] = 0
            
    with col3:
        if st.button("Pause"):
            st.session_state['timer_running'] = False
            st.session_state['is_stopped'] = True
            st.session_state['paused_time'] = st.session_state['elapsed_time']

                

    with placeholder.container():
        render_timer(st.session_state['elapsed_time'])





    #Timer

    while st.session_state['timer_running']:
        st.session_state['elapsed_time'] = st.session_state['paused_time'] + time.time() - st.session_state['start_time']

        with placeholder.container():    
            render_timer(st.session_state['elapsed_time'])
        
        if not st.session_state['timer_running']:
            break
        
        time.sleep(1)
        placeholder.empty()
else:
    st.write("Please, login to your user account.")
    # st.page_link("pages/page_1.py", label="Page 1", icon="1️⃣")