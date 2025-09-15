import streamlit as st

st.set_page_config(page_title="My App Collection", layout="centered")

st.title("📚 Chapter 1 Applications")
st.write("Click a button below to open the app in a new tab. Each app is designed for English education with interactive features.")

# Define your apps here
apps = [
    {
        "name": "1. Vocal Anatomy",
        "url": "https://vocal-anatomy.streamlit.app/",
        "description": "Explore the structure and function of vocal organs involved in speech production."
    },
    {
        "name": "2. Consonant Full Description",
        "url": "https://sound-description-1.streamlit.app/",
        "description": "Review English consonants by their voicing, place, manner, centrality, and oro-nasal process."
    },
    {
        "name": "3. Chapter 1 Term Practice & Quiz",
        "url": "https://ch1-term-practice.streamlit.app/",
        "description": "Test your understanding of key phonetics terms from Chapter 1 through interactive quizzes."
    },
    {
        "name": "4. (TBA)",
        "url": "",
        "description": "This app will be announced soon. Stay tuned for new phonetics resources!"
    }
]


# Display each app as a colored button with description
for app in apps:
    st.markdown(
        f"""
        <div style="margin-bottom: 20px; padding: 10px; border-radius: 10px; background-color: #e5ffcc;">
            <h4 style="margin-bottom: 5px;">{app['name']}</h4>
            <p style="margin-top: 0; margin-bottom: 10px;">{app['description']}</p>
            <a href="{app['url']}" target="_blank">
                <button style="background-color: #4CAF50; color: white; padding: 8px 16px;
                               border: none; border-radius: 5px; font-size: 16px; cursor: pointer;">
                    🍰 Open App
                </button>
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )
