import streamlit as st
import pandas as pd
from gtts import gTTS
from io import BytesIO

# -------------------------------------------------------
# Config
# -------------------------------------------------------
st.set_page_config(page_title="Word & IPA Practice", layout="wide")

# >>>>>>>>>> CHANGE THIS TO YOUR RAW GITHUB CSV URL <<<<<<<<<<
CSV_URL = "https://raw.githubusercontent.com/MK316/English-phonology/refs/heads/main/data/Stress-wordlist-2025.csv"

# -------------------------------------------------------
# Data loading & TTS helpers
# -------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(CSV_URL, encoding="utf-8-sig")
    # Ensure the essential columns exist
    required = {"WID", "Word", "Transcription"}
    missing = required - set(df.columns)
    if missing:
        st.error(f"Missing columns in CSV: {', '.join(missing)}")
    return df


@st.cache_resource
def tts_audio(word: str) -> bytes:
    """Return gTTS audio bytes for a given word."""
    tts = gTTS(text=word, lang="en")
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp.read()


df = load_data()

# -------------------------------------------------------
# Session-state helpers
# -------------------------------------------------------
def init_tab_subset(tab_prefix: str):
    """Create a subset for tab1 or tab2 depending on user selection."""
    n_key = f"{tab_prefix}_n"
    order_key = f"{tab_prefix}_order"
    subset_key = f"{tab_prefix}_subset"
    idx_key = f"{tab_prefix}_idx"

    n = st.session_state.get(n_key, 10)
    order = st.session_state.get(order_key, "Random")

    n = max(1, min(int(n), len(df)))

    if order == "Random":
        subset = df.sample(n, random_state=None).reset_index(drop=True)
    else:  # WID order
        subset = df.sort_values("WID").head(n).reset_index(drop=True)

    st.session_state[subset_key] = subset
    st.session_state[idx_key] = 0

    # Extras for typing practice tab
    if tab_prefix == "tab2":
        st.session_state["tab2_answer"] = ""
        st.session_state["tab2_feedback"] = ""
        st.session_state["tab2_finished"] = False

def nav_prev(tab_prefix: str):
    subset_key = f"{tab_prefix}_subset"
    idx_key = f"{tab_prefix}_idx"
    if subset_key in st.session_state:
        if st.session_state[idx_key] > 0:
            st.session_state[idx_key] -= 1

def nav_next(tab_prefix: str):
    subset_key = f"{tab_prefix}_subset"
    idx_key = f"{tab_prefix}_idx"
    if subset_key in st.session_state:
        subset = st.session_state[subset_key]
        if st.session_state[idx_key] < len(subset) - 1:
            st.session_state[idx_key] += 1
            if tab_prefix == "tab2":
                st.session_state["tab2_answer"] = ""
                st.session_state["tab2_feedback"] = ""
        else:
            if tab_prefix == "tab2":
                st.session_state["tab2_finished"] = True


# -------------------------------------------------------
# Typing practice (Tab 2) callbacks
# -------------------------------------------------------
def check_tab2_answer():
    subset = st.session_state.get("tab2_subset")
    idx = st.session_state.get("tab2_idx", 0)
    if subset is None:
        return

    user = st.session_state.get("tab2_answer", "").strip().lower()
    correct = subset.iloc[idx]["Word"].strip().lower()

    if not user:
        st.session_state["tab2_feedback"] = "Please type an answer."
        return

    if user == correct:
        st.session_state["tab2_feedback"] = "✅ Correct!"
    else:
        st.session_state["tab2_feedback"] = f"❌ Incorrect. Correct answer: **{subset.iloc[idx]['Word']}**"


# -------------------------------------------------------
# Quiz (Tab 3) callbacks
# -------------------------------------------------------
def start_quiz():
    n_items = min(10, len(df))
    subset = df.sample(n_items, random_state=None).reset_index(drop=True)
    st.session_state["quiz_subset"] = subset
    st.session_state["quiz_idx"] = 0
    st.session_state["quiz_score"] = 0
    st.session_state["quiz_answer"] = ""
    st.session_state["quiz_feedback"] = ""
    st.session_state["quiz_finished"] = False


def check_quiz_answer():
    subset = st.session_state.get("quiz_subset")
    idx = st.session_state.get("quiz_idx", 0)
    if subset is None:
        return

    user = st.session_state.get("quiz_answer", "").strip().lower()
    correct = subset.iloc[idx]["Word"].strip().lower()

    if not user:
        st.session_state["quiz_feedback"] = "Please type an answer."
        return

    if user == correct:
        st.session_state["quiz_score"] += 1
        st.session_state["quiz_feedback"] = "✅ Correct!"
    else:
        st.session_state["quiz_feedback"] = f"❌ Incorrect. Correct answer: **{subset.iloc[idx]['Word']}**"

    # Move to next question or finish
    if st.session_state["quiz_idx"] < len(subset) - 1:
        st.session_state["quiz_idx"] += 1
        st.session_state["quiz_answer"] = ""
    else:
        st.session_state["quiz_finished"] = True


# -------------------------------------------------------
# UI
# -------------------------------------------------------
st.title("🎧 Word & IPA Practice App")

tab1, tab2, tab3 = st.tabs(
    ["1️⃣ Listening Practice", "2️⃣ Typing Practice", "3️⃣ Quiz (10 items)"]
)

# -------------------------------------------------------
# TAB 1 – Listening Practice
# -------------------------------------------------------
with tab1:
    st.subheader("Listening Practice (Transcription + Audio)")

    col1, col2 = st.columns(2)
    with col1:
        st.number_input(
            "Number of words to practice",
            min_value=1,
            max_value=len(df),
            value=10,
            step=1,
            key="tab1_n",
        )
    with col2:
        st.radio(
            "Order",
            options=["Random", "WID order"],
            index=0,
            key="tab1_order",
        )

    st.button("Start Practice", on_click=init_tab_subset, args=("tab1",))

    if "tab1_subset" in st.session_state:
        subset = st.session_state["tab1_subset"]
        idx = st.session_state.get("tab1_idx", 0)

        row = subset.iloc[idx]
        st.markdown(f"**Item {idx + 1} / {len(subset)}**")
        st.markdown(f"**Word:** {row['Word']}")
        st.text(f"Transcription: {row['Transcription']}")

        audio_bytes = tts_audio(row["Word"])
        st.audio(audio_bytes, format="audio/mp3")

        c1, c2 = st.columns(2)
        with c1:
            st.button("⬅️ Previous", on_click=nav_prev, args=("tab1",))
        with c2:
            st.button("Next ➡️", on_click=nav_next, args=("tab1",))


# -------------------------------------------------------
# TAB 2 – Typing Practice
# -------------------------------------------------------
with tab2:
    st.subheader("Typing Practice (Listen & Type the Word)")

    col1, col2 = st.columns(2)
    with col1:
        st.number_input(
            "Number of words to practice",
            min_value=1,
            max_value=len(df),
            value=10,
            step=1,
            key="tab2_n",
        )
    with col2:
        st.radio(
            "Order",
            options=["Random", "WID order"],
            index=0,
            key="tab2_order",
        )

    st.button("Start Typing Practice", on_click=init_tab_subset, args=("tab2",))

    if "tab2_subset" in st.session_state:
        subset = st.session_state["tab2_subset"]
        idx = st.session_state.get("tab2_idx", 0)
        finished = st.session_state.get("tab2_finished", False)

        if not finished:
            row = subset.iloc[idx]
            st.markdown(f"**Item {idx + 1} / {len(subset)}**")
            st.text(f"Transcription: {row['Transcription']}")

            audio_bytes = tts_audio(row["Word"])
            st.audio(audio_bytes, format="audio/mp3")

            st.text_input(
                "Type the word here",
                key="tab2_answer",
                placeholder="Enter the word you heard / saw",
            )

            c1, c2 = st.columns(2)
            with c1:
                st.button("Submit", on_click=check_tab2_answer)
            with c2:
                st.button("Next ➡️", on_click=nav_next, args=("tab2",))

            feedback = st.session_state.get("tab2_feedback", "")
            if feedback:
                st.markdown(feedback)
        else:
            st.success("✅ All selected words have been practiced!")


# -------------------------------------------------------
# TAB 3 – Quiz (10 Random Items)
# -------------------------------------------------------
with tab3:
    st.subheader("Quiz: Type the Word from the Transcription (10 random items)")

    if "quiz_subset" not in st.session_state or st.session_state.get(
        "quiz_finished", False
    ):
        st.button("Start Quiz / Practice More", on_click=start_quiz)

    if "quiz_subset" in st.session_state and not st.session_state.get(
        "quiz_finished", False
    ):
        subset = st.session_state["quiz_subset"]
        idx = st.session_state.get("quiz_idx", 0)
        score = st.session_state.get("quiz_score", 0)

        row = subset.iloc[idx]

        st.markdown(f"**Question {idx + 1} / {len(subset)}**")
        st.text(f"Transcription: {row['Transcription']}")
        st.markdown(f"**Current score:** {score}")

        st.text_input(
            "Type the word here",
            key="quiz_answer",
            placeholder="Enter the word",
        )

        st.button("Submit", on_click=check_quiz_answer)

        feedback = st.session_state.get("quiz_feedback", "")
        if feedback:
            st.markdown(feedback)

    if st.session_state.get("quiz_finished", False):
        subset = st.session_state["quiz_subset"]
        score = st.session_state.get("quiz_score", 0)
        st.success(f"🎉 Quiz finished! Final score: {score} / {len(subset)}")
        st.button("Practice More", on_click=start_quiz)
