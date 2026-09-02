import base64
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="학습 앱 모음", layout="wide")

BASE_DIR = Path(__file__).parent

# ============================================================
# 여기에 앱을 추가하면 드롭다운 목록에 자동으로 나타납니다.
# key: 드롭다운에 표시될 이름
# value: 이 파일(pages) 기준 상대 경로
# ============================================================
APPS = {
    "Chapter 1 - 어휘 크로스워드": "crossword/crossword.html",
    # "Chapter 2 - 어휘 크로스워드": "crossword/ch02_crossword.html",
    # "Chapter 1 - 빈칸 채우기 퀴즈": "quiz/index.html",
}

st.title("📚 학습 앱 모음")
st.write("아래에서 실행할 앱을 선택하면 새 탭에서 열립니다.")

selected_name = st.selectbox("앱 선택", list(APPS.keys()))
html_path = BASE_DIR / APPS[selected_name]

if not html_path.exists():
    st.error(f"파일을 찾을 수 없습니다: {html_path}")
    st.stop()

html_content = html_path.read_text(encoding="utf-8")
b64 = base64.b64encode(html_content.encode("utf-8")).decode("utf-8")
data_uri = f"data:text/html;base64,{b64}"

st.markdown(
    f'''
    <a href="{data_uri}" target="_blank" rel="noopener noreferrer"
       style="
         display:inline-block;
         padding:14px 26px;
         background:#1B3A63;
         color:#fff;
         font-weight:600;
         text-decoration:none;
         border-radius:6px;
         font-family:sans-serif;
       ">
       🚀 &quot;{selected_name}&quot; 새 창에서 열기
    </a>
    ''',
    unsafe_allow_html=True,
)
