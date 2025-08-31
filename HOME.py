import streamlit as st

img = "https://github.com/MK316/english-phonology/raw/main/pages/images/bg01.png"  # e.g., "images/figure.png" or a PIL Image

col1, col2, col3 = st.columns([0.5, 3, 0.5])
with col2:
    st.markdown("### 🍎 English Phonology (Fall 2025)")
    st.image(img, use_container_width=True)  # or: width=400
