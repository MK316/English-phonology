import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
from gtts import gTTS
import io

st.set_page_config(page_title="📘 16-Week Course Schedule", layout="wide")
st.title("📘 Course Overview")

tab1, tab2, tab3 = st.tabs(["Schedule", "Syllabus", "TBA"])

with tab1:
    st.markdown("#### Schedule for Class Activities")
    st.markdown("""
    + Grouping (1st week)
    + Quiz schedule

    """)

    st.markdown("---")
    # Custom styled HTML button
    button_html = """
        <style>
            .custom-button {
                background-color: #003377;
                color: white;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                border: none;
                border-radius: 8px;
                cursor: pointer;
            }
            .custom-button:hover {
                background-color: #002244;
            }
        </style>
        <a href="https://docs.google.com/spreadsheets/d/1PfywzAfzNer4iu1iZBXo54AHb1xYcvKi5dh10qzrzBU/edit?usp=sharing">
            <button class="custom-button">🎯 Click: Go to Google Sheet</button>
        </a>
    """
    st.markdown(button_html, unsafe_allow_html=True)



# ---------------- Tab 2: Syllabus / Course Info ----------------
with tab2:
    st.markdown("## 💦 **English Phonology (Fall 2026)**")
    st.caption("Quick syllabus overview")

    st.markdown(
        """
        **• Instructor:** Miran Kim (Professor, Rm# 301-316)  
        **• Meeting Schedule:** Mondays (11–11:50 pm) & Thursdays (9–10:50 pm)  
        **• Digital classroom:** [MK316.github.io](https://MK316.github.io)  — course apps & resources  
        **• LMS:** rec.ac.kr/gnu  
        **• Classroom:** 301-334  
        """,
    )

    # (QR 이미지 코드 삭제됨)

    # --- Course overview ---
    st.markdown("### 📝 Course overview")
    st.divider()
    overview_text = (
        "This course introduces students to the study of English phonology, "
        "the phonological grammar of English, and discusses why and how this "
        "grammar is relevant to teaching English as a second or foreign language. "
        "The course will cover basic concepts necessary to understand the sound "
        "patterns of English from both descriptive and theoretical perspectives. "
        "Students will learn the fundamentals of the English sound system and "
        "acquire some characteristic phonological patterns of English to prepare "
        "themselves as future English teachers. Additionally, the course will "
        "include practice tests to familiarize students with the types of "
        "questions commonly found on teaching licensure examinations."
    )

    st.markdown(f"""{overview_text}""")

    @st.cache_data
    def generate_tts_audio(text: str, lang: str = "en") -> bytes:
        tts = gTTS(text=text, lang=lang)
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        return audio_fp.read()

    audio_bytes = generate_tts_audio(overview_text)
    # Click-to-play audio (no autoplay)
    st.audio(audio_bytes, format="audio/mp3", start_time=0)

    # --- Textbook & Software ---
    st.markdown("### 📚 Textbook & Apps")
    tb, sw = st.columns(2)
    with tb:
        st.markdown(
            """
            **Textbook**  
            Applied English Phonology (4th edition) by Mehmet Yavaʂ (2020), Wiley Blackwell.
            """
        )
    with sw:
        st.markdown(
            """
            **TCE app**  
            app link: <http://apps4u.streamlit.app>
            """
        )

    st.divider()

    # --- Evaluation table (alternative: keep st.dataframe, separate Link column) ---
    st.markdown("### ✅ Evaluation")
    data = [
        ["Attendance & class participation", "10%", "Unexcused absence (−1); late check-in (−0.2)", None],
        ["Quizzes", "40%", "See quiz schedule", "https://docs.google.com/spreadsheets/d/1PfywzAfzNer4iu1iZBXo54AHb1xYcvKi5dh10qzrzBU/edit?usp=sharing"],
        ["Exam", "40%", "Final exam", None],
        ["Assignments", "10%", "Group activities: Exercises (5), Transcription (5)", None],
    ]
    df = pd.DataFrame(data, columns=["Component", "Percentage", "Notes", "Link"])
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Component": st.column_config.Column(width="medium"),
            "Percentage": st.column_config.Column(width=90),
            "Notes": st.column_config.Column(width="large"),
            "Link": st.column_config.LinkColumn("Link", display_text="Open"),
        },
    )

    st.info(
        "Note: The course schedule can be subject to change. "
        "Most updates will be posted here."
    )
