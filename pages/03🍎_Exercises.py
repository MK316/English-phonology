import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

st.set_page_config(
    page_title="Phonetics Exercises",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent
html_path = BASE_DIR / "exercises" / "ex01_test.html"

html = html_path.read_text(encoding="utf-8")

components.html(
    html,
    height=1100,
    scrolling=True
)
