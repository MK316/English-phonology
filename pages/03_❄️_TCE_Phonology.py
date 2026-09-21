import streamlit as st
import pandas as pd


# ---------------------------
# Page setup (MUST be first Streamlit call)
# ---------------------------
st.set_page_config(page_title="Teacher Certification Exam Search", layout="wide")
st.title("TCE Search I")

# Define tab navigation
tab1, tab2 = st.tabs(["🌀 TCE Search: Phonology & Morphology", "🍎 Overview"])


with tab1:
    # Load the DataFrame
    # url = "https://raw.githubusercontent.com/MK316/APP4U/refs/heads/main/data/TExam_new20241125.csv"
    url = "https://raw.githubusercontent.com/MK316/APP4U/refs/heads/main/pages/data/TExam_new20251122.csv"
    df = pd.read_csv(url, encoding='utf-8-sig')

    # Function to search years based on the selected mode
    def search_years(search_mode, query):
        query = query.strip().lower()
        if search_mode == "YEAR":
            matches = df[df['YEAR'].str.startswith(query[:4])]
        elif search_mode == "Keywords":
            keyword_list = query.split(',')
            matches = df[df['KEYWORDS'].str.lower().apply(lambda x: any(keyword in x for keyword in keyword_list))]
        elif search_mode == "Words containing":
            matches = df[df['TEXT'].str.lower().str.contains(query)]
        else:
            st.error("Please select a valid search mode.")
            return []

        if matches.empty:
            st.error("No results found for your query.")
            return []
        return matches['YEAR'].tolist()

    # Streamlit layout for search

    st.subheader('❄️ [1] Start Searching')

    with st.form(key='search_form'):
        col1, col2 = st.columns([1, 3])

        with col1:
            st.write("Search mode by:")  # Label

        with col2:
            search_mode = st.radio("", ["YEAR", "Keywords", "Words containing"], horizontal=True)

        query = st.text_input("Search Query: e.g., 2024 (by YEAR), 'tapping' (by Keywords) or 'distribution' (Words containing)", "")
        search_button = st.form_submit_button('🍒 Click to Search')

    if search_button:
        results = search_years(search_mode, query)
        if results:
            st.session_state['results'] = results
            st.session_state['selected_year'] = results[0]  # Default to first result
            st.success("Search completed successfully.")

    # Select box to choose year from results
    st.subheader('❄️ [2] Choose an item from the selected:')
    if 'results' in st.session_state:
        selected_year = st.selectbox("Select a year from the results", st.session_state['results'], index=0, key='selected_year')

    # Button to display exam question
    if st.button('🍒 Show me the exam question') and 'selected_year' in st.session_state:
        match = df[df['YEAR'] == st.session_state['selected_year']]
        if not match.empty:
            image_filename = match.iloc[0]['Filename']
            image_url = f'https://huggingface.co/spaces/MK-316/TCE/resolve/main/TExams/{image_filename}'
            keywords = match.iloc[0]['KEYWORDS']
            st.markdown(f"**🌷 Keywords:** 🔑 {keywords}")
            st.image(image_url, caption=f'Exam Image for {st.session_state["selected_year"]}', width=800)
        else:
            st.error("No keywords or image found for this year.")


with tab2:
    st.markdown("##### TCE (Teacher Certificate Exam) Question Searching Engine")

    st.info("Note: Data contains previous exam questions in the area of phonetics & phonology from 2005 up to date. _Laste updated (2025. 11.23)_")



    st.caption("This application is designed to help users efficiently search and review past exam questions.")
    
    st.markdown("""
    #### ❄️ Here's How to Use:
    <div style="color: #FF8000;"><b>+ Step 1 Start Searching:</b></div>
    Users can search exam questions by <b>year, keywords, or text content (words containing...)</b>. After specifying the search criteria,
    the application displays the relevant years where these questions appeared.
    
    <div style="color: #FF8000;"><b>+ Step 2 Choose an Item from the Selected:</b></div>
    Following a successful search, users can select a year to view the exam question in detail,
    including an image and related keywords.
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="color: #0066CC;">This tool supports teachers and students preparing for certification exams in phonetics and phonology,
    continually updating to enhance its functionality and user experience.</div>
    """, unsafe_allow_html=True)
