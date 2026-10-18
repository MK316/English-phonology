from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

# pages/ 폴더 방식이면 페이지마다 둘 수 있습니다.
# st.navigation 방식이면 이 줄은 지우고 메인 파일에서만 설정하세요.
st.set_page_config(page_title="IPA Consonants", page_icon="🔠", layout="centered")

HTML_PATH = Path(__file__).resolve().parent.parent / "assets" / "ipa_consonants.html"


def embed(html: str, height: int) -> None:
    """최신 Streamlit(st.iframe 있음)은 내용 높이에 맞춰 자동 조절, 이전 버전은 components.html 사용."""
    if hasattr(st, "iframe"):
        st.iframe(html, height="content")
    else:
        components.html(html, height=height, scrolling=True)


@st.cache_data
def load_html(path: str, mtime: float) -> str:
    return Path(path).read_text(encoding="utf-8")


embed(load_html(str(HTML_PATH), HTML_PATH.stat().st_mtime), 950)
