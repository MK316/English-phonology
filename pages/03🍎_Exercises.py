import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

# ---------------- Page setup ----------------
st.set_page_config(
    page_title="AEP Exercises",
    layout="wide"
)

st.markdown("### Phonetics Exercises")

# ---------------- File path ----------------
BASE_DIR = Path(__file__).resolve().parent
EXERCISE_DIR = BASE_DIR / "exercises"

# ---------------- Chapter menu ----------------
chapters = {
    "Chapter 1": "ch01-ex01-test1.html",
    "Chapter 2": "ex02_test.html",
    "Chapter 3": "ex03_test.html",
    "Chapter 4": "ex04_test.html",
    "Chapter 5": "ex05_test.html",
}

selected_chapter = st.selectbox(
    "Select a chapter",
    options=list(chapters.keys())
)

# ---------------- Load selected HTML ----------------
html_file = EXERCISE_DIR / chapters[selected_chapter]

if html_file.exists():

    html = html_file.read_text(
        encoding="utf-8"
    )

    components.html(
        html,
        height=1100,
        scrolling=True
    )

else:
    st.error(
        f"File not found: {html_file.name}"
    )
