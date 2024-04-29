import streamlit as st
import time
from utils.functions import format_time

st.title("Track activity")

start_time = time.time()
elapsed_time = 0

if "timer_running" not in st.session_state:
    st.session_state["timer_running"] = False

# timer_running = False
play_button = None
pause_button = None
stop_button = None

col1, col2 = st.columns([0.85, 0.15], gap="small")

with col1:
    st.text_input(
        "Activity name:",
        value="",
        label_visibility="collapsed",
        placeholder="Input activity name...",
    )

with col2:
    save_button = st.button("Save")


# while timer_running:
#     with placeholder.container():
#         st.write("This is one element")
#         elapsed_time = time.time() - start_time
#         st.markdown("### {}".format(format_time(int(elapsed_time))))
#         time.sleep(1)
#         placeholder.empty()

placeholder = st.empty()

while st.session_state["timer_running"]:
    with placeholder.container():
        _, col2, _ = st.columns([0.4, 0.2, 0.4], gap="small")

        with col2:
            elapsed_time = time.time() - start_time
            print(int(elapsed_time))
            st.markdown("### {}".format(format_time(int(elapsed_time))))
            if not st.session_state["timer_running"]:
                break

        col0, col1, col2, col3, col4 = st.columns(
            [0.315, 0.1, 0.115, 0.1, 0.35], gap="small"
        )

        with col1:
            play_button = st.button("Play", key=time.time())
        with col2:
            st.container(height=1, border=False)
            pause_button = st.button("Pause", key=time.time() + 1)
        with col3:
            stop_button = st.button("Stop", key=time.time() + 2)

        time.sleep(1)
        placeholder.empty()

_, col2, _ = st.columns([0.4, 0.2, 0.4], gap="small")

with col2:
    st.markdown("### {}".format(format_time(int(elapsed_time))))

col0, col1, col2, col3, col4 = st.columns(
    [0.315, 0.1, 0.115, 0.1, 0.35], gap="small"
)

with col1:
    play_button = st.button("Play", key=time.time())
with col2:
    st.container(height=1, border=False)
    pause_button = st.button("Pause", key=time.time() + 1)
with col3:
    stop_button = st.button("Stop", key=time.time() + 2)


if play_button:
    st.session_state["timer_running"] = True
    # timer_running = True
    st.write("sdgsdg")
if stop_button:
    # в sessiion state сохранять timer running
    timer_running = False
