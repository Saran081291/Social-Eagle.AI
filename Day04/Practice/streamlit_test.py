import streamlit as st

st.title("Streamlit Test Application")

st.write("This is a simple Streamlit application for testing purposes.")

st.balloons()

st.audio(
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
    format="audio/mp3",
    start_time=0
)