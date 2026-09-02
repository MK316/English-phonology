import re
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="Ch01 강의 슬라이드", layout="wide")

# 이 파일(pages/1_강의슬라이드.py) 기준으로 pages/lectureslides/Ch01 폴더를 찾습니다.
CHAPTER_DIR = Path(__file__).parent / "lectureslides" / "Ch01"


def natural_key(path: Path):
    """slide_2.png < slide_10.png 처럼 숫자 기준으로 정렬되도록 하는 키"""
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", path.stem)]


IMAGE_EXTENSIONS = ("*.png", "*.jpg", "*.jpeg", "*.PNG", "*.JPG", "*.JPEG")


@st.cache_data
def load_slide_paths(chapter_dir: str):
    p = Path(chapter_dir)
    files = []
    for pattern in IMAGE_EXTENSIONS:
        files.extend(p.glob(pattern))
    # 중복 제거 후 자연 정렬
    files = sorted(set(files), key=natural_key)
    return [str(f) for f in files]


slides = load_slide_paths(str(CHAPTER_DIR))

if not slides:
    st.error(f"슬라이드를 찾을 수 없습니다: {CHAPTER_DIR}")
    st.info("이 폴더 안에 이미지 파일들을 넣어주세요. 예: AEP_CH01.001.jpeg, AEP_CH01.002.jpeg ...")
    st.stop()

total = len(slides)

if "slide_idx" not in st.session_state:
    st.session_state.slide_idx = 0


def go_to(idx: int):
    st.session_state.slide_idx = max(0, min(idx, total - 1))


st.title("📘 Ch01 강의 슬라이드")

# ---------------- 상단 네비게이션 버튼 ----------------
nav_cols = st.columns([1, 1, 1, 3, 1])
with nav_cols[0]:
    if st.button("⏮ 처음", use_container_width=True):
        go_to(0)
with nav_cols[1]:
    if st.button("◀ 이전", use_container_width=True):
        go_to(st.session_state.slide_idx - 1)
with nav_cols[2]:
    if st.button("다음 ▶", use_container_width=True):
        go_to(st.session_state.slide_idx + 1)
with nav_cols[4]:
    if st.button("마지막 ⏭", use_container_width=True):
        go_to(total - 1)

# ---------------- 특정 슬라이드로 바로 이동 ----------------
jump_col1, jump_col2 = st.columns([1, 4])
with jump_col1:
    jump_num = st.number_input(
        "슬라이드 번호로 이동",
        min_value=1,
        max_value=total,
        value=st.session_state.slide_idx + 1,
        step=1,
    )
with jump_col2:
    st.write("")  # 세로 정렬용 여백
    if st.button("이동"):
        go_to(int(jump_num) - 1)

st.caption(f"현재 슬라이드: {st.session_state.slide_idx + 1} / {total}")

# ---------------- 현재 슬라이드 표시 ----------------
st.image(slides[st.session_state.slide_idx], use_container_width=True)

st.divider()

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
