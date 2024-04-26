import streamlit as st
import requests

st.title('InnoTrackify')

def register(username, email, password):
    url = "http://localhost:5000/register"
    data = {"username": username, "email": email, "password": password}
    response = requests.post(url, json=data)
    return response.json()

def login(username, password):
    url = "http://localhost:5000/login"
    data = {"username": username, "password": password}
    response = requests.post(url, json=data)
    return response.json()


# st.markdown("""
# InnoTrackify is the ultimate solution for individuals seeking to efficiently track and manage their daily activities, offering a comprehensive suite of features tailored to meet diverse user needs while prioritizing usability and functionality.
# """)

if 'session_token' not in st.session_state:
    st.session_state['session_token'] = None

choice = st.selectbox('Login/Signup', ["Sign-up", "Login"])

if choice == "Login":
    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")

    if st.button("Login"):
        result = login(username, password)
        if result["success"]:
            st.success(result["message"])
            session_token = result["session_token"]
            st.session_state['session_token'] = session_token
            # Redirect to another page or perform other actions
        else:
            st.error(result["message"])
else:
    username = st.text_input("Username:")
    email = st.text_input("Email:")
    password = st.text_input("Password:", type="password")

    if st.button("Sign up"):
        result = register(username, email, password)
        if result["success"]:
            st.success(result["message"])
        else:
            st.error(result["message"])