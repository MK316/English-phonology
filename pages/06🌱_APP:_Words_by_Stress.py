import streamlit as st
import pandas as pd
import tempfile
from gtts import gTTS

# Set page configuration for wider layout
st.set_page_config(layout="wide")

# Load the dataset from GitHub
@st.cache_data
def load_data(url):
    return pd.read_csv(url)

csv_url = "https://raw.githubusercontent.com/MK316/stress2024/refs/heads/main/data/data20241216.csv"
df = load_data(csv_url)

# POS mapping
pos_mapping = {
    "n": "Noun",
    "adj": "Adjective",
    "v": "Verb",
    "adv": "Adverb"
}

# Convert POS abbreviations to full forms
def convert_pos(pos_abbrev):
    return ", ".join([pos_mapping.get(p.strip(), p.strip()) for p in pos_abbrev.split(',')])

# Function to add visual circles for stress patterns
def add_stress_circles(stress):
    stress_options = ["1st", "2nd", "antepenult", "penult", "ult"]
    circle_html = "<div style='display: flex; flex-direction: row; justify-content: center; gap: 20px;'>"
    for idx, option in enumerate(stress_options):
        background_color = "yellow" if option == stress else "white"
        text_color = "black" if option == stress else "gray"
        border_color = "gray"
        circle_html += f"<div style='width: 100px; height: 60px; background: {background_color}; border: 2px solid {border_color}; color: {text_color}; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 16px;'>{option.capitalize()}</div>"
        if option == "2nd":
            circle_html += "<div style='display: flex; align-items: center; justify-content: center; color: gray; font-size: 16px;'> (optional syllables) </div>"
    circle_html += "</div>"
    return circle_html

# Initialize session state for button click
if 'button_clicked' not in st.session_state:
    st.session_state.button_clicked = False

# Main app layout
st.markdown("### ⛄ 1. Words-by-stress")
st.caption("Chapter 7. Stress; A total of 564 words")
st.caption("Focus on learning the first word's details, and understand the variations as a reference.")
selected_stress = st.selectbox("🔴 Select Stress Position", ["1st", "2nd", "antepenult", "penult", "ult", "compound"])

# Display stress circles
if selected_stress:
    st.markdown(add_stress_circles(selected_stress), unsafe_allow_html=True)

    # Display data based on selected stress
    filtered_data = df[df['Stress'] == selected_stress]
    st.write("")
    st.write(f"🌱 Total words with '{selected_stress}' stress: {len(filtered_data)}")
    st.dataframe(filtered_data[['Word', 'POS', 'Transcription', 'Variation']], width=600, height=200)

# Word Search with Audio Playback
st.markdown("### ❄️ 2. Word details with Audio")
user_input = st.text_input("🔴 Enter the number next to a word to search (e.g., 104 for 'category'):", placeholder="Type a word here...")

# Manage button click state
def on_search():
    st.session_state.button_clicked = True

search_button = st.button("Search", on_click=on_search)

if search_button or st.session_state.button_clicked:
    try:
        # Convert user input to integer index
        index = int(user_input)
        # Access the DataFrame by index
        row = df.iloc[index]
        
        pos = row['POS']
        full_pos = convert_pos(pos)
        stress = row['Stress']
        transcription = row['Transcription']
        word = row['Word']
        variation = row.get('Variation', 'N/A')  # Assuming 'Variation' might not exist

        tts = gTTS(text=word, lang='en')
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_file.name)

        st.write(f"POS: {full_pos}")
        st.write(f"Stress: {stress}")
        st.write(f"IPA: {transcription}")
        st.write(f"Variation: {variation}")
        st.audio(temp_file.name)

    except ValueError:
        st.error("Please enter a valid integer index.")
    except IndexError:
        st.error("Index out of range. Please enter a valid index.")
    finally:
        st.session_state.button_clicked = False  # Reset state after the search attempt
