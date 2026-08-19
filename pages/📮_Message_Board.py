import streamlit as st
import streamlit.components.v1 as components

def main():
    st.caption("💙 Greetings! Feel free to leave any feedback, suggestions, or messages about the application on this page. I'll make sure to look into them as soon as I can! 😍")
    st.write("➡️ Click the '+' sign to write.")
    # Padlet embed URL (you need to replace this with your actual Padlet embed URL)
    padlet_url = "https://padlet.com/mirankim316/apps4u"

    # Create an iframe to embed the Padlet
    padlet_iframe = f"<iframe src='{padlet_url}' width='100%' height='600' frameborder='0' allow='autoplay'></iframe>"

    # Display the iframe in Streamlit
    components.html(padlet_iframe, height=600)

if __name__ == "__main__":
    main()
