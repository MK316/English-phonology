import streamlit as st

st.set_page_config(page_title="Audio Review App", layout="centered")

st.title("English stress: audio samples")

# ---------------------------
# Tab layout
# ---------------------------
tab1, tab2, tab3 = st.tabs(["🎵 Audio Player", "📄 Tab 2", "📄 Tab 3"])

# ---------------------------
# TAB 1: Audio from GitHub
# ---------------------------
with tab1:
    st.subheader("Listen to the audio files")

    st.write(
        "Select an audio file from the dropdown menu below and use the player to listen."
    )

    # Base URL where your MP3 files are stored on GitHub
    # Example pattern:
    # https://raw.githubusercontent.com/USERNAME/REPO/BRANCH/path/to/audio/file.mp3
    BASE_URL = "https://raw.githubusercontent.com/MK316/English-phonology/main/pages/audio/"

    # Dictionary of files: label -> full URL
    audio_files = {
        "Audio 1: democrat (Female)": BASE_URL + "01_democrat.mp3",
        "Audio 2: democrat (Male)": BASE_URL + "02_democrat_male.mp3",
        # Add more later if needed:
        # "Audio 3": BASE_URL + "audio3.mp3",
    }

    # Dropdown to choose audio
    selected_label = st.selectbox(
        "Choose an audio file",
        list(audio_files.keys()),
        index=0,
    )

    # Get the URL of the chosen file
    selected_url = audio_files[selected_label]

    # Audio player
    st.audio(selected_url, format="audio/mp3")

# ---------------------------
# TAB 2: Placeholder
# ---------------------------
with tab2:
    st.subheader("Tab 2")
    st.write("This tab is reserved for future content (e.g., rating, notes, quiz, etc.).")

# ---------------------------
# TAB 3: Placeholder
# ---------------------------
with tab3:
    st.subheader("Tab 3")
    st.write("This tab is also reserved for future content.")
