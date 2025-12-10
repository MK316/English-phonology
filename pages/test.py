import streamlit as st
import pandas as pd
from gtts import gTTS
from io import BytesIO
from datetime import datetime

# For PDF generation
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

st.set_page_config(page_title="Word & Transcription Practice App", layout="wide")

# ---- CSV URL ----
CSV_URL = "https://raw.githubusercontent.com/MK316/English-phonology/refs/heads/main/data/Stress-wordlist-2025.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(CSV_URL, encoding="utf-8-sig")
    return df

@st.cache_resource
def tts_audio(word: str) -> bytes:
    tts = gTTS(text=word, lang="en")
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp.read()

df = load_data()

# ---------- PDF helper ----------
def create_pdf_report(username, history, score, start_time, end_time):
    """
    Create a PDF report and return it as bytes.
    history: list of dicts with keys {'word', 'correct'}.
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 50

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Word Quiz Report")
    y -= 30

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Name: {username}")
    y -= 18
    if start_time:
        c.drawString(50, y, f"Start time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        y -= 18
    if end_time:
        c.drawString(50, y, f"End time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        y -= 18

    total_items = len(history)
    c.drawString(50, y, f"Score: {score} / {total_items}")
    y -= 30

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Items practiced:")
    y -= 20

    c.setFont("Helvetica", 10)
    for i, item in enumerate(history, start=1):
        status = "Correct" if item["correct"] else "Incorrect"
        line = f"{i}. {item['word']}  -  {status}"
        if y < 50:  # new page if needed
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 10)
        c.drawString(50, y, line)
        y -= 15

    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    return pdf

# ---------- helpers for practice tabs ----------
def init_tab_subset(tab_prefix: str):
    n_key = f"{tab_prefix}_n"
    order_key = f"{tab_prefix}_order"
    subset_key = f"{tab_prefix}_subset"
    idx_key = f"{tab_prefix}_idx"

    n = st.session_state.get(n_key, 10)
    order = st.session_state.get(order_key, "Random")

    n = max(1, min(int(n), len(df)))

    if order == "Random":
        subset = df.sample(n).reset_index(drop=True)
    else:
        subset = df.sort_values("WID").head(n).reset_index(drop=True)

    st.session_state[subset_key] = subset
    st.session_state[idx_key] = 0

    if tab_prefix == "tab2":
        st.session_state["tab2_answer"] = ""
        st.session_state["tab2_feedback"] = ""
        st.session_state["tab2_finished"] = False

def nav_prev(tab_prefix: str):
    idx_key = f"{tab_prefix}_idx"
    if idx_key in st.session_state and st.session_state[idx_key] > 0:
        st.session_state[idx_key] -= 1

def nav_next(tab_prefix: str):
    subset_key = f"{tab_prefix}_subset"
    idx_key = f"{tab_prefix}_idx"
    if subset_key not in st.session_state:
        return
    subset = st.session_state[subset_key]
    if st.session_state[idx_key] < len(subset) - 1:
        st.session_state[idx_key] += 1
        if tab_prefix == "tab2":
            st.session_state["tab2_answer"] = ""
            st.session_state["tab2_feedback"] = ""
    else:
        if tab_prefix == "tab2":
            st.session_state["tab2_finished"] = True

def check_tab2_answer():
    subset = st.session_state.get("tab2_subset")
    idx = st.session_state.get("tab2_idx", 0)
    if subset is None:
        return
    user = st.session_state.get("tab2_answer", "").strip().lower()
    correct = subset.iloc[idx]["Word"].strip().lower()
    if not user:
        st.session_state["tab2_feedback"] = "Please type an answer."
    elif user == correct:
        st.session_state["tab2_feedback"] = "✅ Correct!"
    else:
        st.session_state["tab2_feedback"] = (
            f"❌ Incorrect. Correct answer: **{subset.iloc[idx]['Word']}**"
        )

# ---------- quiz helpers ----------
def start_quiz():
    # Read settings from widgets in Tab 3
    n = st.session_state.get("tab3_n", 10)
    order = st.session_state.get("tab3_order", "Random")

    n = max(1, min(int(n), len(df)))

    if order == "Random":
        subset = df.sample(n).reset_index(drop=True)
    else:  # WID order
        subset = df.sort_values("WID").head(n).reset_index(drop=True)

    st.session_state["quiz_subset"] = subset
    st.session_state["quiz_idx"] = 0
    st.session_state["quiz_score"] = 0
    st.session_state["quiz_answer"] = ""
    st.session_state["quiz_feedback"] = ""
    st.session_state["quiz_finished"] = False
    st.session_state["quiz_history"] = []  # store per-item results
    # record time & username snapshot
    st.session_state["quiz_start_time"] = datetime.now()
    st.session_state["quiz_end_time"] = None
    st.session_state["quiz_username_stored"] = (
        st.session_state.get("quiz_username", "").strip() or "Anonymous"
    )

def check_quiz_answer():
    subset = st.session_state.get("quiz_subset")
    idx = st.session_state.get("quiz_idx", 0)
    if subset is None:
        return

    user = st.session_state.get("quiz_answer", "").strip().lower()
    correct_word = subset.iloc[idx]["Word"].strip().lower()

    if not user:
        st.session_state["quiz_feedback"] = "Please type an answer."
        return

    is_correct = user == correct_word

    if is_correct:
        st.session_state["quiz_score"] += 1
        st.session_state["quiz_feedback"] = "✅ Correct!"
    else:
        st.session_state["quiz_feedback"] = (
            f"❌ Incorrect. Correct answer: **{subset.iloc[idx]['Word']}**"
        )

    # Log result for this item (once)
    history = st.session_state.get("quiz_history", [])
    # avoid duplicate logging if user presses submit multiple times
    already_logged = any(h["index"] == idx for h in history)
    if not already_logged:
        history.append(
            {
                "index": idx,
                "word": subset.iloc[idx]["Word"],
                "correct": is_correct,
            }
        )
        st.session_state["quiz_history"] = history

    # Move on or finish
    if st.session_state["quiz_idx"] < len(subset) - 1:
        st.session_state["quiz_idx"] += 1
        st.session_state["quiz_answer"] = ""
    else:
        st.session_state["quiz_finished"] = True
        st.session_state["quiz_end_time"] = datetime.now()

# ---------- UI ----------
st.title("🎧 Word & Transcription Practice App")

tab1, tab2, tab3, tab4 = st.tabs(
    ["1️⃣ Listening Practice", "2️⃣ Transcription Reading", "3️⃣ Quiz", "4️⃣ Word Lookup"]
)

# ===== TAB 1 =====
with tab1:
    st.subheader("Listening Practice (Transcription + Audio)")
    c1, c2 = st.columns(2)
    with c1:
        st.number_input(
            "Number of words to practice",
            1, len(df), 10, 1,
            key="tab1_n",
        )
    with c2:
        st.radio(
            "Order",
            ["Random", "WID order"],
            index=0,
            key="tab1_order",
        )
    st.button("Start Practice", on_click=init_tab_subset,
              args=("tab1",), key="tab1_start")

    if "tab1_subset" in st.session_state:
        subset = st.session_state["tab1_subset"]
        idx = st.session_state.get("tab1_idx", 0)
        row = subset.iloc[idx]
        st.markdown(f"**Item {idx + 1} / {len(subset)}**")
        st.markdown(f"**Word:** {row['Word']}")
        st.text(f"Transcription: {row['Transcription']}")
        audio_bytes = tts_audio(row["Word"])
        st.audio(audio_bytes, format="audio/mp3")
        b1, b2 = st.columns(2)
        with b1:
            st.button("⬅️ Previous", on_click=nav_prev,
                      args=("tab1",), key="tab1_prev")
        with b2:
            st.button("Next ➡️", on_click=nav_next,
                      args=("tab1",), key="tab1_next")

# ===== TAB 2 =====
with tab2:
    st.subheader("Transcription Reading Practice")
    c1, c2 = st.columns(2)
    with c1:
        st.number_input(
            "Number of words to practice",
            1, len(df), 10, 1,
            key="tab2_n",
        )
    with c2:
        st.radio(
            "Order",
            ["Random", "WID order"],
            index=0,
            key="tab2_order",
        )
    st.button("Start Typing Practice", on_click=init_tab_subset,
              args=("tab2",), key="tab2_start")

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

            b1, b2 = st.columns(2)
            with b1:
                st.button("Submit", on_click=check_tab2_answer,
                          key="tab2_submit")
            with b2:
                st.button("Next ➡️", on_click=nav_next,
                          args=("tab2",), key="tab2_next")

            feedback = st.session_state.get("tab2_feedback", "")
            if feedback:
                st.markdown(feedback)
        else:
            st.success("✅ All selected words have been practiced!")

# ===== TAB 3 =====
with tab3:
    st.subheader("Quiz: Type the Word from the Transcription")

    # name input
    username = st.text_input("Enter your name", key="quiz_username")

    # length & order selection
    c1, c2 = st.columns(2)
    with c1:
        st.number_input(
            "Number of quiz items",
            min_value=1,
            max_value=len(df),
            value=10,
            step=1,
            key="tab3_n",
        )
    with c2:
        st.radio(
            "Order",
            options=["Random", "WID order"],
            index=0,
            key="tab3_order",
        )

    # Start / restart quiz using current settings (name required)
    if st.button("Start Quiz / Restart", key="quiz_start"):
        if not username.strip():
            st.warning("Please enter your name before starting the quiz.")
        else:
            start_quiz()

    # main quiz logic
    if "quiz_subset" in st.session_state and not st.session_state.get("quiz_finished", False):
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
        st.button("Submit", on_click=check_quiz_answer, key="quiz_submit")

        feedback = st.session_state.get("quiz_feedback", "")
        if feedback:
            st.markdown(feedback)

    # quiz finished: show score, restart, and PDF download
    if st.session_state.get("quiz_finished", False):
        subset = st.session_state["quiz_subset"]
        score = st.session_state.get("quiz_score", 0)
        stored_name = st.session_state.get("quiz_username_stored", "Anonymous")
        start_time = st.session_state.get("quiz_start_time", None)
        end_time = st.session_state.get("quiz_end_time", None)
        history = st.session_state.get("quiz_history", [])

        st.success(f"🎉 Quiz finished! Final score: {score} / {len(subset)}")

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Practice More", key="quiz_more"):
                if not st.session_state.get("quiz_username", "").strip():
                    st.warning("Please enter your name before starting the quiz.")
                else:
                    start_quiz()

        with col_b:
            if history:
                pdf_bytes = create_pdf_report(
                    stored_name, history, score, start_time, end_time
                )
                st.download_button(
                    "📄 Download PDF report",
                    data=pdf_bytes,
                    file_name=f"{stored_name.replace(' ', '_')}_quiz_report.pdf",
                    mime="application/pdf",
                    key="quiz_pdf",
                )
            else:
                st.info("No history recorded yet for this quiz session.")

# ===== TAB 4 =====
with tab4:
    st.subheader("Word Lookup (Transcription + Audio)")

    lookup_word = st.text_input(
        "Type a word to look up",
        key="lookup_word",
        placeholder="e.g., resignation",
    )

    if st.button("Search", key="lookup_search"):
        if not lookup_word.strip():
            st.warning("Please type a word to search.")
        else:
            # case-insensitive match
            mask = df["Word"].str.lower() == lookup_word.strip().lower()
            if mask.any():
                row = df[mask].iloc[0]
                st.markdown(f"**Word:** {row['Word']}")
                st.text(f"Transcription: {row['Transcription']}")
                audio_bytes = tts_audio(row["Word"])
                st.audio(audio_bytes, format="audio/mp3")
            else:
                st.error("Word not found in the list.")
