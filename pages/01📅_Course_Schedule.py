import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

st.set_page_config(page_title="📘 16-Week Course Schedule", layout="wide")
st.title("📘 Course Overview")

tab1, tab2, tab3 = st.tabs(["Schedule", "Syllabus", "TBA"])

with tab1:
    # Start on Thursday, September 3, 2026 (course meets Mondays & Thursdays)
    start_date = datetime(2026, 9, 3)

    # ✅ STEP 1: Fill only the weeks you want — here, Week 3 has data (Sept. 16 & 18)
    schedule_content = {
        "2026-09-03": ["Ch. 1", "Syllabus, Course overview", "Grouping", "Reading Chapter 1"],
        "2026-09-07": ["Ch. 1", "Phonetics review", "Reading", "Summary note-taking"],
        "2026-09-10": ["Ch. 1", "Sound description", "", "Summary note-taking"],
        "2026-09-14": ["Ch. 2", "Phonetics & Phonology", "", "Summary note-taking"],
        "2026-09-17": ["Ch. 3", "English consonants", "", "", ""],
        "2026-09-21": ["", "", "", ""],
        "2026-09-24": ["🎈Holiday", "", "", ""],
        "2026-09-28": ["", "", "", ""],
        "2026-10-01": ["", "", "", ""],
        "2026-10-05": ["🎈Alt Holiday", "", "", "🔴 Makeup video "],
        "2026-10-08": ["", "", "", ""],
        "2026-10-12": ["", "", "", ""],
        "2026-10-15": ["", "", "", ""],
        "2026-10-19": ["", "", "", ""],
        "2026-10-22": ["", "", "", ""],
        "2026-10-26": ["", "", "", ""],
        "2026-10-29": ["", "", "", ""],
        "2026-11-02": ["", "", "", ""],
        "2026-11-05": ["", "", "", ""],
        "2026-11-09": ["", "", "", ""],
        "2026-11-12": ["", "", "", ""],
        "2026-11-16": ["", "", "", ""],
        "2026-11-19": ["", "", "", ""],
        "2026-11-23": ["", "", "", "🔴 "],
        "2026-11-26": ["", "", "", ""],
        "2026-11-30": ["", "", "", ""],
        "2026-12-03": ["", "", "", ""],
        "2026-12-07": ["", "", "", ""],
        "2026-12-10": ["", "", "", ""],
        "2026-12-14": ["", "", "", ""],
        "2026-12-17": ["", "", "", "🔴 Final exam"],
        "2026-12-21": ["", "", "", ""]
    }

    # ✅ STEP 2: Build the HTML table (Week 1-16, Thursday rows highlighted light blue)
    table_rows_html = ""
    for i, (date_str, content) in enumerate(schedule_content.items()):
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        display_date = date_obj.strftime("%b %d (%a)")  # e.g., "Sep 03 (Thu)"

        # Pad content to always have 4 columns: Chapter, Keywords, Assignments, Remark
        row = (content + ["", "", "", ""])[:4]
        chapter, keywords, assignments, remark = row

        # Week number: two sessions (Mon/Thu) per week -> Week 1 to 16
        week_num = (i // 2) + 1

        # Highlight Thursday rows in light blue
        is_thursday = date_obj.strftime("%A") == "Thursday"
        row_style = ' style="background-color:#ADD8E6;"' if is_thursday else ""

        table_rows_html += (
            f"<tr{row_style}>"
            f"<td>{week_num}</td>"
            f"<td>{display_date}</td>"
            f"<td>{chapter}</td>"
            f"<td>{keywords}</td>"
            f"<td>{assignments}</td>"
            f"<td>{remark}</td>"
            f"</tr>\n"
        )

    table_header_html = (
        "<table>"
        "<tr>"
        "<th>Week</th><th>Date</th><th>Chapter</th><th>Keywords</th>"
        "<th>Assignments & Activities</th><th>Remark</th>"
        "</tr>\n"
    )
    table_footer_html = "</table>"

    schedule_table = table_header_html + table_rows_html + table_footer_html

    # ✅ STEP 3: Display it
    st.markdown(schedule_table, unsafe_allow_html=True)

# ---------------- Tab 2: Syllabus / Course Info ----------------
with tab2:
    st.markdown("## 💦 **English Phonology (Fall 2026)**")
    st.caption("Quick syllabus overview")

    # --- Top section: key facts + QR/link ---
    col1, col2 = st.columns([3, 2], vertical_alignment="top")

    with col1:
        st.markdown(
            """
            **• Instructor:** Miran Kim (Professor, Rm# 301-316)  
            **• Meeting Schedule:** Mondays (11–11:50 pm) & Thursdays (9–10:50 pm)  
            **• Digital classroom:** [MK316.github.io](https://MK316.github.io)  — course apps & resources  
            **• LMS:** rec.ac.kr/gnu  
            **• Classroom:** 301-334  
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
