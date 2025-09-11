# ===== Imports (top of file) =====
from io import BytesIO
from datetime import datetime
import os

import streamlit as st
import pandas as pd

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ===== App setup =====
st.set_page_config(page_title="IPA Practice — Step-by-Step", layout="centered")
st.markdown("#### 🐾 IPA Practice — Describing 24 English consonants")

st.caption(
    "Work through the five steps. Each step shows one feature for all symbols. "
    "At the end, you’ll see correctness, feedback, and a PDF download."
)

# ===== Data / options =====
FEATURES_ORDER = ["Voicing", "Place", "Centrality", "Oro-nasal", "Manner"]

ipa_symbols = ["p","b","t","d","k","g","f","v","θ","ð","s","z","ʃ","ʒ","tʃ","dʒ","h","m","n","ŋ","ɹ","l","j","w"]

# Centrality has "Not applicable"; Oro-nasal does NOT include it
OPTIONS = {
    "Voicing": ["voiceless", "voiced"],
    "Place": ["bilabial", "labio-dental", "labio-velar", "dental", "alveolar", "post-alveolar", "palatal", "velar", "glottal"],
    "Centrality": ["central", "lateral", "Not applicable"],
    "Oro-nasal": ["oral", "nasal"],
    "Manner": ["stop", "fricative", "affricate", "approximant"],
}
DEFAULTS = {
    "Voicing": "voiceless",
    "Place": "bilabial",
    "Centrality": "central",
    "Oro-nasal": "oral",
    "Manner": "stop",
}

# Answer key aligned to the option sets (simplified)
ANSWER_KEY = {
    "p":  {"Voicing":"voiceless","Place":"bilabial","Centrality":"central","Oro-nasal":"oral","Manner":"stop"},
    "b":  {"Voicing":"voiced","Place":"bilabial","Centrality":"central","Oro-nasal":"oral","Manner":"stop"},
    "t":  {"Voicing":"voiceless","Place":"alveolar","Centrality":"central","Oro-nasal":"oral","Manner":"stop"},
    "d":  {"Voicing":"voiced","Place":"alveolar","Centrality":"central","Oro-nasal":"oral","Manner":"stop"},
    "k":  {"Voicing":"voiceless","Place":"velar","Centrality":"central","Oro-nasal":"oral","Manner":"stop"},
    "g":  {"Voicing":"voiced","Place":"velar","Centrality":"central","Oro-nasal":"oral","Manner":"stop"},
    "f":  {"Voicing":"voiceless","Place":"labio-dental","Centrality":"central","Oro-nasal":"oral","Manner":"fricative"},
    "v":  {"Voicing":"voiced","Place":"labio-dental","Centrality":"central","Oro-nasal":"oral","Manner":"fricative"},
    "θ":  {"Voicing":"voiceless","Place":"dental","Centrality":"central","Oro-nasal":"oral","Manner":"fricative"},
    "ð":  {"Voicing":"voiced","Place":"dental","Centrality":"central","Oro-nasal":"oral","Manner":"fricative"},
    "s":  {"Voicing":"voiceless","Place":"alveolar","Centrality":"central","Oro-nasal":"oral","Manner":"fricative"},
    "z":  {"Voicing":"voiced","Place":"alveolar","Centrality":"central","Oro-nasal":"oral","Manner":"fricative"},
    "ʃ":  {"Voicing":"voiceless","Place":"post-alveolar","Centrality":"central","Oro-nasal":"oral","Manner":"fricative"},
    "ʒ":  {"Voicing":"voiced","Place":"post-alveolar","Centrality":"central","Oro-nasal":"oral","Manner":"fricative"},
    "tʃ": {"Voicing":"voiceless","Place":"post-alveolar","Centrality":"central","Oro-nasal":"oral","Manner":"affricate"},
    "dʒ": {"Voicing":"voiced","Place":"post-alveolar","Centrality":"central","Oro-nasal":"oral","Manner":"affricate"},
    "h":  {"Voicing":"voiceless","Place":"glottal","Centrality":"central","Oro-nasal":"oral","Manner":"fricative"},
    "m":  {"Voicing":"voiced","Place":"bilabial","Centrality":"Not applicable","Oro-nasal":"nasal","Manner":"stop"},
    "n":  {"Voicing":"voiced","Place":"alveolar","Centrality":"Not applicable","Oro-nasal":"nasal","Manner":"stop"},
    "ŋ":  {"Voicing":"voiced","Place":"velar","Centrality":"Not applicable","Oro-nasal":"nasal","Manner":"stop"},
    "ɹ":  {"Voicing":"voiced","Place":"alveolar","Centrality":"central","Oro-nasal":"oral","Manner":"approximant"},
    "l":  {"Voicing":"voiced","Place":"alveolar","Centrality":"lateral","Oro-nasal":"oral","Manner":"approximant"},
    "j":  {"Voicing":"voiced","Place":"palatal","Centrality":"central","Oro-nasal":"oral","Manner":"approximant"},
    "w":  {"Voicing":"voiced","Place":"labio-velar","Centrality":"central","Oro-nasal":"oral","Manner":"approximant"},
}

# ===== State init =====
if "step" not in st.session_state:
    st.session_state.step = 0  # 0..4 => feature steps; 5 => results
if "selections" not in st.session_state:
    st.session_state.selections = {
        feat: {sym: DEFAULTS[feat] for sym in ipa_symbols} for feat in FEATURES_ORDER
    }
if "group_name" not in st.session_state:
    st.session_state.group_name = ""
if "student_name" not in st.session_state:
    st.session_state.student_name = ""
if "pdf_bytes" not in st.session_state:
    st.session_state.pdf_bytes = None

# ===== Reset helpers =====
def reset_all():
    st.session_state.step = 0
    st.session_state.selections = {
        feat: {sym: DEFAULTS[feat] for sym in ipa_symbols} for feat in FEATURES_ORDER
    }
    for feat in FEATURES_ORDER:
        for sym in ipa_symbols:
            st.session_state.pop(f"sel__{feat}__{sym}", None)
    st.session_state.group_name = ""
    st.session_state.student_name = ""
    st.rerun()

def start_over_keep():
    st.session_state.step = 0
    st.rerun()

# ===== Header controls (unique keys to avoid duplicates) =====
col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    st.button("Start Over (keep choices)", key="btn_start_over_top", on_click=start_over_keep)
with col_btn2:
    st.button("Reset All (clear everything)", key="btn_reset_all_top", on_click=reset_all)

# ----- Header info (persist) -----
col1, col2 = st.columns(2)
with col1:
    group_name = st.text_input("Group", value=st.session_state.group_name)
    st.session_state.group_name = group_name
with col2:
    student_name = st.text_input("Name", value=st.session_state.student_name)
    st.session_state.student_name = student_name

st.divider()

# ===== Step renderer =====
def render_step(feature_name: str):
    help_text = {
        "Voicing": "Choose voiced / voiceless.",
        "Place": "Choose one place of articulation.",
        "Centrality": "Choose central / lateral / Not applicable.",
        "Oro-nasal": "Choose oral / nasal.",
        "Manner": "Choose stop / fricative / affricate / approximant.",
    }[feature_name]

    st.markdown(f"### Step {st.session_state.step + 1} of 5 — {feature_name}")
    st.caption(help_text)

    with st.form(f"form_{feature_name}", clear_on_submit=False):
        # header row
        hdr = st.columns([0.7, 2.5])
        hdr[0].markdown("**IPA**")
        hdr[1].markdown(f"**{feature_name}**")

        for sym in ipa_symbols:
            cols = st.columns([0.7, 2.5])
            cols[0].markdown(f"**{sym}**")
            current = st.session_state.selections[feature_name][sym]
            cols[1].selectbox(
                label=feature_name,
                options=OPTIONS[feature_name],
                index=OPTIONS[feature_name].index(current) if current in OPTIONS[feature_name] else 0,
                key=f"sel__{feature_name}__{sym}",
                label_visibility="collapsed",
            )

        next_label = "Finish & Check" if feature_name == "Manner" else "Next ▶️"
        submitted = st.form_submit_button(next_label, type="primary")

    if submitted:
        for sym in ipa_symbols:
            st.session_state.selections[feature_name][sym] = st.session_state.get(
                f"sel__{feature_name}__{sym}", st.session_state.selections[feature_name][sym]
            )
        st.session_state.step += 1
        st.rerun()

# ===== Utilities =====
def selections_to_df():
    data = []
    for sym in ipa_symbols:
        row = {"IPA": sym}
        for feat in FEATURES_ORDER:
            row[feat] = st.session_state.selections[feat][sym]
        data.append(row)
    return pd.DataFrame(data, columns=["IPA"] + FEATURES_ORDER)

def compute_wrong_mask_and_feedback(df_user: pd.DataFrame):
    df_ans = pd.DataFrame(
        [{"IPA": sym, **ANSWER_KEY[sym]} for sym in ipa_symbols],
        columns=["IPA"] + FEATURES_ORDER
    )
    wrong_mask = pd.DataFrame(False, index=df_user.index, columns=df_user.columns)
    for feat in FEATURES_ORDER:
        wrong_mask[feat] = df_user[feat] != df_ans[feat]
    wrong_mask["IPA"] = False

    feedback_lines = []
    for i, sym in enumerate(df_user["IPA"]):
        wrong_feats = [feat for feat in FEATURES_ORDER if wrong_mask.loc[i, feat]]
        if wrong_feats:
            detail = ", ".join(
                f"{feat}: expected {df_ans.loc[i, feat]} / got {df_user.loc[i, feat]}"
                for feat in wrong_feats
            )
            feedback_lines.append(f"• {sym} — {detail}")
    return wrong_mask, feedback_lines, df_ans

# ===== PDF helpers =====
def _find_unicode_font():
    for p in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
        "fonts/DejaVuSans.ttf",
        "fonts/NotoSans-Regular.ttf",
    ]:
        if os.path.exists(p):
            try:
                pdfmetrics.registerFont(TTFont("UnicodeBase", p))
                return "UnicodeBase"
            except Exception:
                pass
    return "Helvetica"

def build_pdf(df_user: pd.DataFrame, wrong_mask: pd.DataFrame, feedback_lines, group_name: str, student_name: str) -> bytes:
    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4, leftMargin=24, rightMargin=24, topMargin=28, bottomMargin=28,
        title="IPA Practice"
    )
    base_font = _find_unicode_font()
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("Title", parent=styles["Heading2"], fontName=base_font, spaceAfter=6)
    meta_style  = ParagraphStyle("Meta",  parent=styles["Normal"],   fontName=base_font, fontSize=9, spaceAfter=10)
    cell_style  = ParagraphStyle("Cell",  parent=styles["BodyText"], fontName=base_font, fontSize=9, leading=11)
    feedback_title_style = ParagraphStyle("FBTitle", parent=styles["Heading3"], fontName=base_font, spaceBefore=10, spaceAfter=4)
    fb_style = ParagraphStyle("FB", parent=styles["Normal"], fontName=base_font, fontSize=9, leading=11)

    elements = []
    elements.append(Paragraph("ლ( ╹ ◡ ╹ ლ) IPA Practice — 24 English consonants", title_style))
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    elements.append(Paragraph(
        f"Group: {group_name or ''} &nbsp;&nbsp; Name: {student_name or ''} &nbsp;&nbsp; Exported: {ts}",
        meta_style
    ))
    elements.append(Spacer(1, 6))

    # Build table data
    header = ["IPA"] + FEATURES_ORDER
    data = [header]
    for _, r in df_user.iterrows():
        data.append([
            Paragraph(str(r["IPA"]), cell_style),
            Paragraph(str(r["Voicing"]), cell_style),
            Paragraph(str(r["Place"]), cell_style),
            Paragraph(str(r["Centrality"]), cell_style),
            Paragraph(str(r["Oro-nasal"]), cell_style),
            Paragraph(str(r["Manner"]), cell_style),
        ])

    col_widths = [35, 90, 120, 100, 90, 120]
    tbl = Table(data, colWidths=col_widths, repeatRows=1, hAlign="LEFT")

    # Base table style
    style_cmds = [
        ("FONTNAME", (0,0), (-1,-1), base_font),
        ("FONTSIZE", (0,0), (-1,-1), 9),
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#f0f2f6")),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("ALIGN", (0,0), (0,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#fbfbfb")]),
        ("TOPPADDING", (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
    ]

    # Add wrong cell highlights (remember: table rows are +1 due to header)
    for i in range(len(df_user)):
        for j, feat in enumerate(FEATURES_ORDER, start=1):
            if wrong_mask.loc[i, feat]:
                style_cmds.append(("BACKGROUND", (j, i+1), (j, i+1), colors.black))
                style_cmds.append(("TEXTCOLOR", (j, i+1), (j, i+1), colors.white))

    tbl.setStyle(TableStyle(style_cmds))
    elements.append(tbl)

    # Feedback section in PDF
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("◕‿◕✿ Feedback", feedback_title_style))
    if feedback_lines:
        for line in feedback_lines:
            elements.append(Paragraph(line, fb_style))
    else:
        elements.append(Paragraph("All correct. Well done!", fb_style))

    doc.build(elements)
    buf.seek(0)
    return buf.getvalue()

# ===== Flow control =====
if st.session_state.step < len(FEATURES_ORDER):
    render_step(FEATURES_ORDER[st.session_state.step])
else:
    # ===== Results =====
    st.markdown("### Results")
    df_user = selections_to_df()
    wrong_mask, feedback_lines, df_ans = compute_wrong_mask_and_feedback(df_user)

    # Style: wrong cells black + white text (on screen)
    def _style_wrong(_df):
        styles = pd.DataFrame("", index=df_user.index, columns=df_user.columns)
        styles = styles.mask(wrong_mask, other="background-color: black; color: white;")
        return styles

    st.write(df_user.style.apply(_style_wrong, axis=None))

    # Feedback on screen
    if feedback_lines:
        st.error("Some entries need review:")
        st.markdown("\n".join([f"- {ln}" for ln in feedback_lines]))
    else:
        st.success("🎉 All correct!")

    st.divider()

    # Generate & Download PDF (two-step; unique keys)
    colg, cold = st.columns([1,1])
    with colg:
        if st.button("Generate PDF", key="btn_gen_pdf"):
            st.session_state.pdf_bytes = build_pdf(
                df_user, wrong_mask, feedback_lines, st.session_state.group_name, st.session_state.student_name
            )
            st.success("PDF generated. Use the button on the right to download.")
    with cold:
        st.download_button(
            "📥 Download PDF",
            data=st.session_state.pdf_bytes if st.session_state.pdf_bytes else b"",
            file_name=f"IPA_Practice_{(st.session_state.student_name or 'student').replace(' ', '_')}.pdf",
            mime="application/pdf",
            disabled=st.session_state.pdf_bytes is None,
            key="btn_download_pdf"
        )

    # Bottom restart controls (unique keys to avoid duplicates)
    st.divider()
    cb1, cb2 = st.columns(2)
    with cb1:
        st.button("Start Over (keep choices)", key="btn_start_over_bottom", on_click=start_over_keep)
    with cb2:
        st.button("Reset All (clear everything)", key="btn_reset_all_bottom", on_click=reset_all)
