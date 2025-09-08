import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

st.set_page_config(page_title="📘 16-Week Course Schedule", layout="wide")
st.title("📘 Course Overview")

tab1, tab2, tab3 = st.tabs(["Schedule", "Syllabus", "TBA"])

with tab1:

    # Table header
    table_header = "| Date | Chapter | Keywords | Assignments & Activities | Remark |\n"
    table_divider = "|------|---------|----------|---------------------------|--------|\n"
    
    # Start on Tuesday, September 2, 2025
    start_date = datetime(2025, 9, 2)
    
    
    
    # ✅ STEP 1: Fill only the weeks you want — here, Week 3 has data (Sept. 16 & 18)
    schedule_content = {
        "2025-09-02": ["Ch. 1", "Syllabus, Course overview", "Grouping", "Reading Chapter 1"],
        "2025-09-04": ["Ch. 1", "Vocal anatomy", "Lecture video on LMS (Ch1)","Summary note-taking"],
        "2025-09-09": ["Ch. 2", "Phonetics & Phonology", "", "Summary note-taking"],
        "2025-09-11": ["Ch. 2", "Phonetics & Phonology", "", "Summary note-taking"],
        "2025-09-16": ["", "", "", ""],
        "2025-09-18": ["", "", "", ""],
        "2025-09-23": ["", "", "", ""],
        "2025-09-25": ["", "", "", ""],
        "2025-09-30": ["", "", "", ""],
        "2025-10-02": ["", "", "", "🔴 Quiz1 #1"],
        "2025-10-07": ["", "", "", ""],
        "2025-10-09": ["", "", "", ""],
        "2025-10-14": ["", "", "", ""],
        "2025-10-16": ["", "", "", ""],
        "2025-10-21": ["", "", "", ""],
        "2025-10-23": ["", "", "", ""],
        "2025-10-28": ["", "", "", ""],
        "2025-10-30": ["", "", "", ""],
        "2025-11-04": ["", "", "", ""],
        "2025-11-06": ["", "", "", ""],
        "2025-11-11": ["", "", "", ""],
        "2025-11-13": ["", "", "", ""],
        "2025-11-18": ["", "", "", "🔴 Quiz #2"],
        "2025-11-20": ["", "", "", ""],
        "2025-11-25": ["", "", "", ""],
        "2025-11-27": ["", "", "", ""],
        "2025-12-02": ["", "", "", ""],
        "2025-12-04": ["", "", "", ""],
        "2025-12-09": ["", "", "", ""],
        "2025-12-11": ["", "", "", ""],
        "2025-12-16": ["", "", "", ""],
        "2025-12-18": ["", "", "", "🔴 Final exam"]
    }
    
    # ✅ STEP 2: Build the markdown table
    table_md = ""
    
    table_md = ""
    
    for week in range(16):
        # --- choose emoji/tag first ---
        if 7 <= (week + 1) <= 11:
            emoji, tag = "💙", " (Academic trip) 〽️ 〽️ 〽️ 〽️ 〽️ 〽️ 〽️"
        else:
            emoji, tag = "🗓️", ""
    
        # --- label & header (once) ---
        week_label = f"**{emoji} Week {week + 1:02d}{tag}**"
        table_md += f"\n{week_label}\n\n"
        table_md += table_header + table_divider
    
        # --- dates for this week ---
        tuesday  = start_date + timedelta(weeks=week)
        thursday = tuesday + timedelta(days=2)
    
        # --- format date (red for Oct 7 & 9 only) ---
        def format_date(d):
            s = d.strftime("%Y-%m-%d")
            if s in ("2025-10-07", "2025-10-09"):
                return f"<span style='color:red'>{d.strftime('%b. %d')}</span>"
            return d.strftime("%b. %d")
    
        # --- fetch content once for each date ---
        tue_data = schedule_content.get(tuesday.strftime("%Y-%m-%d"),  ["", "", "", ""])
        thu_data = schedule_content.get(thursday.strftime("%Y-%m-%d"), ["", "", "", ""])
    
        # --- append EXACTLY TWO ROWS (do not append anywhere else) ---
        table_md += f"| {format_date(tuesday)}  | {tue_data[0]} | {tue_data[1]} | {tue_data[2]} | {tue_data[3]} |\n"
        table_md += f"| {format_date(thursday)} | {thu_data[0]} | {thu_data[1]} | {thu_data[2]} | {thu_data[3]} |\n"
    

    # ✅ STEP 3: Display it
    st.markdown(table_md, unsafe_allow_html=True)



# ---------------- Tab 2: Syllabus / Course Info ----------------
with tab2:
    st.markdown("## 💦 **English Phonetics (Fall 2025)**")
    st.caption("Quick syllabus overview")

    # --- Top section: key facts + QR/link ---
    col1, col2 = st.columns([3, 2], vertical_alignment="top")

    with col1:
        st.markdown(
            """
            **• Instructor:** Miran Kim (Professor, Rm# 301-316)  
            **• Meeting Schedule:** Tuesdays (1–1:50 pm) & Thursdays (2–2:50 pm)  
            **• Digital classroom:** [MK316.github.io](https://MK316.github.io)  — course apps & resources  
            **• LMS:** rec.ac.kr/gnu  
            **• Classroom:** 301-330  
            """,
        )

    with col2:
        QR_URL = "https://github.com/MK316/english-phonetics/raw/main/pages/images/qr_phonetics.png"
        st.image(QR_URL, caption="Digital classroom QR", width=150)  # set width in pixels
    st.divider()

    # --- Course overview ---
    st.markdown("### 📝 Course overview")
    st.markdown(
        """
        This course introduces the fundamental aspects of the English sound system with an emphasis on
        learning and teaching English pronunciation. We cover the basic phonetic properties of English
        speech sounds—**consonants and vowels**—and core concepts needed to understand the sound system.
        We also explore **English prosody** (syllables, rhythm, and intonation).

        You will practice **phonetic transcription** of spoken English data and develop skills for teaching
        pronunciation. Throughout the course, you’ll learn to distinguish **connected vs. isolated speech** and
        **formal vs. informal** styles.
        """
    )
    AUDIO_URL = "https://raw.githubusercontent.com/MK316/english-phonetics/main/pages/audio/audio-overview.mp3"

    # Click-to-play audio (no autoplay)
    st.audio(AUDIO_URL, format="audio/mp3", start_time=0)

    # --- Textbook & Software ---
    st.markdown("### 📚 Textbook & Software")
    tb, sw = st.columns(2)
    with tb:
        st.markdown(
            """
            **Textbook**  
            Johnson, K. & Ladefoged, P. (2014). *A Course in Phonetics* (7th ed.). CENGAGE Learning.
            """
        )
    with sw:
        st.markdown(
            """
            **Software**  
            Praat — download: <http://www.fon.hum.uva.nl/praat/download_win.html>
            """
        )

    st.divider()

    # --- Evaluation table ---
    st.markdown("### ✅ Evaluation")
    data = [
        ["Attendance & class participation", "10%", "Unexcused absence (−1); late check-in (−0.2)"],
        ["Quizzes", "30%", "TBA"],
        ["Exam", "40%", "Final exam"],
        ["Assignments", "10%", "Group activities: Exercises (5), Transcription (5)"],
        ["Summary notes", "10%", "All chapters (will be checked 3 times)"],
    ]
    df = pd.DataFrame(data, columns=["Component", "Percentage", "Notes"])

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Component": st.column_config.Column(width="medium"),
            "Percentage": st.column_config.Column(width=90),
            "Notes": st.column_config.Column(width="large"),
        },
    )

    st.info(
        "Note: The course schedule can be subject to change. "
        "Most updates will be posted here."
    )
