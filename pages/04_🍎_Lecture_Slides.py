import re
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="강의 슬라이드", layout="wide")

# 화면 여백을 줄여서 슬라이드 이미지를 최대한 크게 보이도록 함
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 3rem;
        padding-bottom: 1rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

BASE_DIR = Path(__file__).parent / "lectureslides"
CHAPTERS = [f"Ch{str(i).zfill(2)}" for i in range(1, 8)]  # Ch01 ~ Ch07
IMAGE_EXTENSIONS = ("*.png", "*.jpg", "*.jpeg", "*.PNG", "*.JPG", "*.JPEG")


def natural_key(path: Path):
    """AEP_CH01.001 < AEP_CH01.002 < AEP_CH01.010 처럼 숫자 기준으로 정렬되도록 하는 키"""
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", path.stem)]


@st.cache_data
def load_slide_paths(chapter_dir: str):
    p = Path(chapter_dir)
    files = []
    for pattern in IMAGE_EXTENSIONS:
        files.extend(p.glob(pattern))
    files = sorted(set(files), key=natural_key)
    return [str(f) for f in files]


# ---------------- 왼쪽 메뉴(사이드바) 하단 - 챕터 선택 드롭다운 ----------------
# 자동으로 생성되는 페이지 메뉴(멀티페이지 네비게이션) 아래쪽에 표시됩니다.
st.sidebar.markdown("---")
selected_chapter = st.sidebar.selectbox("📂 챕터 선택", CHAPTERS, key="selected_chapter")

CHAPTER_DIR = BASE_DIR / selected_chapter
slides = load_slide_paths(str(CHAPTER_DIR))

# 챕터가 바뀌면 슬라이드 인덱스를 처음으로 초기화
if "current_chapter" not in st.session_state:
    st.session_state.current_chapter = selected_chapter
    st.session_state.slide_idx = 0
elif st.session_state.current_chapter != selected_chapter:
    st.session_state.current_chapter = selected_chapter
    st.session_state.slide_idx = 0

if not slides:
    st.error(f"슬라이드를 찾을 수 없습니다: {CHAPTER_DIR}")
    st.info("이 폴더 안에 이미지 파일들을 넣어주세요. 예: AEP_CH01.001.jpeg, AEP_CH01.002.jpeg ...")
    st.stop()

total = len(slides)

# 챕터 전환 등으로 인덱스가 범위를 벗어난 경우 보정
if st.session_state.slide_idx >= total:
    st.session_state.slide_idx = 0


def go_to(idx: int):
    st.session_state.slide_idx = max(0, min(idx, total - 1))


# ---------------- 상단 네비게이션 버튼 ----------------
nav_cols = st.columns([1, 1, 1, 1, 1, 1, 2])
with nav_cols[0]:
    if st.button("⏮ 처음", use_container_width=True):
        go_to(0)
with nav_cols[1]:
    if st.button("◀ 이전", use_container_width=True):
        go_to(st.session_state.slide_idx - 1)
with nav_cols[2]:
    if st.button("다음 ▶", use_container_width=True):
        go_to(st.session_state.slide_idx + 1)
with nav_cols[3]:
    if st.button("마지막 ⏭", use_container_width=True):
        go_to(total - 1)
with nav_cols[4]:
    jump_num = st.number_input(
        "이동",
        min_value=1,
        max_value=total,
        value=st.session_state.slide_idx + 1,
        step=1,
        label_visibility="collapsed",
    )
with nav_cols[5]:
    if st.button("이동", use_container_width=True):
        go_to(int(jump_num) - 1)
with nav_cols[6]:
    st.caption(f"**{selected_chapter}**  |  슬라이드 {st.session_state.slide_idx + 1} / {total}")

# ---------------- 현재 슬라이드 표시 (최대한 크게) ----------------
st.image(slides[st.session_state.slide_idx], use_container_width=True)

# ---------------- 전체 슬라이드 미리보기 ----------------
with st.expander("📑 전체 슬라이드 미리보기", expanded=False):
    cols_per_row = 5
    for row_start in range(0, total, cols_per_row):
        row_slides = slides[row_start: row_start + cols_per_row]
        cols = st.columns(cols_per_row)
        for i, slide_path in enumerate(row_slides):
            idx = row_start + i
            with cols[i]:
                st.image(slide_path, use_container_width=True)
                label = f"📍 {idx + 1} (현재)" if idx == st.session_state.slide_idx else f"{idx + 1}번으로 이동"
                if st.button(label, key=f"thumb_{idx}", use_container_width=True):
                    go_to(idx)
                    st.rerun()
