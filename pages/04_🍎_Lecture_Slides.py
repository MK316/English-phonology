import re
from pathlib import Path
from urllib.parse import quote

import requests
import streamlit as st


# ============================================================
# Page configuration
# ============================================================

st.set_page_config(
    page_title="강의 슬라이드",
    layout="wide"
)

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


# ============================================================
# GitHub configuration
# ============================================================

GITHUB_OWNER = "MK316"
GITHUB_REPO = "English-phonology"
GITHUB_BRANCH = "main"

GITHUB_SLIDE_FOLDER = "pages/lectureslides"

GITHUB_API = (
    f"https://api.github.com/repos/"
    f"{GITHUB_OWNER}/{GITHUB_REPO}/contents"
)

RAW_BASE = (
    f"https://raw.githubusercontent.com/"
    f"{GITHUB_OWNER}/{GITHUB_REPO}/"
    f"{GITHUB_BRANCH}"
)


# ============================================================
# Chapter configuration
# ============================================================

CHAPTERS = [
    f"Ch{i:02d}"
    for i in range(1, 8)
]

IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
}


# ============================================================
# Local folder search
# ============================================================

def find_local_chapter_dir(chapter):

    """
    Search for chapter folders in several possible
    local directory structures.
    """

    current_dir = Path(__file__).resolve().parent

    parent_names = [
        "lectureslides",
        "lectureslide",
    ]

    # Search current directory and its parent directories.
    search_roots = [
        current_dir,
        *current_dir.parents
    ]

    for root in search_roots:

        for parent_name in parent_names:

            possible_dirs = [
                root / parent_name / chapter,
                root / "pages" / parent_name / chapter,
            ]

            for candidate in possible_dirs:

                if candidate.is_dir():

                    return candidate

    return None


# ============================================================
# Natural sorting
# ============================================================

def natural_key(filename):

    """
    Sort filenames numerically.

    Example:
    AEPCh03.001
    AEPCh03.002
    AEPCh03.010
    """

    name = Path(str(filename)).stem

    return [
        int(part) if part.isdigit()
        else part.lower()

        for part in re.split(
            r"(\d+)",
            name
        )
    ]


# ============================================================
# Load local slides
# ============================================================

@st.cache_data(ttl=300)
def load_local_slides(chapter_dir):

    if not chapter_dir:
        return []

    folder = Path(chapter_dir)

    if not folder.is_dir():
        return []

    files = [
        file
        for file in folder.iterdir()

        if (
            file.is_file()
            and
            file.suffix.lower() in IMAGE_EXTENSIONS
        )
    ]

    files = sorted(
        files,
        key=lambda p: natural_key(p.name)
    )

    return [
        str(file)
        for file in files
    ]


# ============================================================
# Load slides directly from GitHub
# ============================================================

@st.cache_data(ttl=300)
def load_github_slides(chapter):

    """
    Retrieve all image filenames from GitHub API.
    Construct raw image URLs.
    """

    folder_path = (
        f"{GITHUB_SLIDE_FOLDER}/{chapter}"
    )

    api_url = (
        f"{GITHUB_API}/{folder_path}"
    )

    headers = {
        "Accept": "application/vnd.github+json"
    }

    try:

        response = requests.get(
            api_url,
            params={
                "ref": GITHUB_BRANCH
            },
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

        items = response.json()

        if not isinstance(items, list):
            return []

        image_files = []

        for item in items:

            filename = item.get(
                "name",
                ""
            )

            file_type = item.get(
                "type",
                ""
            )

            if file_type != "file":
                continue

            extension = Path(
                filename
            ).suffix.lower()

            if extension not in IMAGE_EXTENSIONS:
                continue

            image_files.append(
                filename
            )

        image_files = sorted(
            image_files,
            key=natural_key
        )

        image_urls = []

        for filename in image_files:

            safe_filename = quote(
                filename
            )

            image_url = (
                f"{RAW_BASE}/"
                f"{folder_path}/"
                f"{safe_filename}"
            )

            image_urls.append(
                image_url
            )

        return image_urls

    except requests.exceptions.RequestException:

        return []


# ============================================================
# Combined slide loader
# ============================================================

def load_chapter_slides(chapter):

    """
    Priority:

    1. Local chapter directory
    2. GitHub repository
    """

    # Search local folders
    local_dir = find_local_chapter_dir(
        chapter
    )

    if local_dir:

        local_slides = load_local_slides(
            str(local_dir)
        )

        if local_slides:

            return (
                local_slides,
                "Local",
                str(local_dir)
            )

    # Fallback: GitHub
    github_slides = load_github_slides(
        chapter
    )

    if github_slides:

        github_path = (
            f"{GITHUB_SLIDE_FOLDER}/"
            f"{chapter}"
        )

        return (
            github_slides,
            "GitHub",
            github_path
        )

    return (
        [],
        "Not Found",
        None
    )


# ============================================================
# Sidebar: chapter selection
# ============================================================

st.sidebar.markdown("---")

selected_chapter = st.sidebar.selectbox(
    "📂 챕터 선택",
    CHAPTERS,
    key="selected_chapter"
)


# ============================================================
# Load selected chapter
# ============================================================

slides, slide_source, slide_location = (
    load_chapter_slides(
        selected_chapter
    )
)


# ============================================================
# Reset index when chapter changes
# ============================================================

if "current_chapter" not in st.session_state:

    st.session_state.current_chapter = (
        selected_chapter
    )

    st.session_state.slide_idx = 0

elif (
    st.session_state.current_chapter
    != selected_chapter
):

    st.session_state.current_chapter = (
        selected_chapter
    )

    st.session_state.slide_idx = 0


# ============================================================
# Error handling
# ============================================================

if not slides:

    st.error(
        f"슬라이드를 찾을 수 없습니다: "
        f"{selected_chapter}"
    )

    st.info(
        "로컬 폴더와 GitHub 저장소를 "
        "모두 확인했지만 이미지가 발견되지 않았습니다."
    )

    st.code(
        f"{GITHUB_SLIDE_FOLDER}/"
        f"{selected_chapter}"
    )

    st.stop()


# ============================================================
# Slide information
# ============================================================

total = len(
    slides
)

if st.session_state.slide_idx >= total:

    st.session_state.slide_idx = 0


# ============================================================
# Navigation function
# ============================================================

def go_to(idx):

    st.session_state.slide_idx = max(
        0,
        min(
            idx,
            total - 1
        )
    )


# ============================================================
# Navigation controls
# ============================================================

nav_cols = st.columns(
    [1, 1, 1, 1, 1, 1, 2]
)


# First slide
with nav_cols[0]:

    if st.button(
        "⏮ 처음",
        use_container_width=True
    ):

        go_to(0)


# Previous slide
with nav_cols[1]:

    if st.button(
        "◀ 이전",
        use_container_width=True
    ):

        go_to(
            st.session_state.slide_idx - 1
        )


# Next slide
with nav_cols[2]:

    if st.button(
        "다음 ▶",
        use_container_width=True
    ):

        go_to(
            st.session_state.slide_idx + 1
        )


# Last slide
with nav_cols[3]:

    if st.button(
        "마지막 ⏭",
        use_container_width=True
    ):

        go_to(
            total - 1
        )


# Jump to slide
with nav_cols[4]:

    jump_num = st.number_input(
        "이동",
        min_value=1,
        max_value=total,
        value=(
            st.session_state.slide_idx + 1
        ),
        step=1,
        label_visibility="collapsed"
    )


with nav_cols[5]:

    if st.button(
        "이동",
        use_container_width=True
    ):

        go_to(
            int(jump_num) - 1
        )


# Current position
with nav_cols[6]:

    st.caption(
        f"**{selected_chapter}**"
        f" | "
        f"슬라이드 "
        f"{st.session_state.slide_idx + 1}"
        f" / "
        f"{total}"
    )


# ============================================================
# Display current slide
# ============================================================

current_slide = slides[
    st.session_state.slide_idx
]

st.image(
    current_slide,
    use_container_width=True
)


# ============================================================
# Slide previews
# ============================================================

with st.expander(
    "📑 전체 슬라이드 미리보기",
    expanded=False
):

    cols_per_row = 5

    for row_start in range(
        0,
        total,
        cols_per_row
    ):

        row_slides = slides[
            row_start:
            row_start + cols_per_row
        ]

        cols = st.columns(
            cols_per_row
        )

        for i, slide_path in enumerate(
            row_slides
        ):

            idx = row_start + i

            with cols[i]:

                st.image(
                    slide_path,
                    use_container_width=True
                )

                if (
                    idx
                    == st.session_state.slide_idx
                ):

                    label = (
                        f"📍 {idx + 1} (현재)"
                    )

                else:

                    label = (
                        f"{idx + 1}번으로 이동"
                    )

                if st.button(
                    label,
                    key=f"thumb_{idx}",
                    use_container_width=True
                ):

                    go_to(
                        idx
                    )

                    st.rerun()


# ============================================================
# Optional source information
# ============================================================

with st.sidebar.expander(
    "📁 Slide information"
):

    st.write(
        f"Chapter: {selected_chapter}"
    )

    st.write(
        f"Total slides: {total}"
    )

    st.write(
        f"Source: {slide_source}"
    )

    st.write(
        f"Location: {slide_location}"
    )

    if st.button(
        "🔄 Refresh slide list"
    ):

        load_local_slides.clear()
        load_github_slides.clear()

        st.rerun()
