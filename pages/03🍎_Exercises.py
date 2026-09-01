import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

st.set_page_config(
    page_title="Phonetics Exercises",
    layout="wide"
)

html = Path("ex01_test.html").read_text(
    encoding="utf-8"
)

components.html(
    html,
    height=1100,
    scrolling=True
)
