import streamlit as st

st.set_page_config(page_title="Past Exam Video Archive", layout="centered")

st.title("English Linguistics Exam Video Archive")
st.write(
    "Select a year and exam session from the dropdown menu to view the corresponding video."
)

# Year–session to YouTube URL mapping (replace with actual links)
video_urls = {
    "2005-1": "https://youtu.be/lQifRHNOvQU?si=hTHnHeA8e6lE7XQO",
    "2005-2": "https://youtu.be/U6DUlOx7BA4?si=mCHKL4bhIkh9UutH",
    "2007-1": "https://youtu.be/Eh08ksF4cBY?si=pnt1vV5_yk8CKR_E",
    "2008-2": "https://youtu.be/e-yVJrLD9BM",
    "2011-1": "https://youtu.be/V-mVg9yMALc",
    "2012-2": "https://youtu.be/clH-AL6_Zmg",
    "2013-2": "https://youtu.be/0ctVnCBFF-8",
    "2015-1": "https://youtu.be/v-yMQcii6hM?si=vMQcHEelkSMn1VAa",
    "2015-2": "https://youtu.be/5dhmyHosP4c",
    "2016-3": "https://youtu.be/PVFo0xgUmEA?si=WYA3j7OGk06vcuoU",
    "2018-3": "https://youtu.be/a00mqL6pRiU?si=YdH4Z19RkXp2U5Q8",
    "2020-2": "https://youtu.be/ntqgNYfpQ-g?si=mhdPTKxO8wMFIWwK",
}

# Sorted list for dropdown
options = sorted(video_urls.keys())

selected_label = st.selectbox(
    "Select Year and Session",
    options,
    index=0,
    placeholder="Choose a video",
)

if selected_label:
    st.subheader(f"Selected Video: {selected_label}")
    url = video_urls[selected_label]
    st.video(url)
