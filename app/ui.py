import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="ResearchAI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── INJECT FULL THEME ──────────────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Cabinet+Grotesk:wght@400;500;700;800;900&display=swap" rel="stylesheet">

<style>
/* ── VARIABLES ── */
:root {
  --bg:        #080c10;
  --surface:   #0d1117;
  --surface2:  #111820;
  --border:    rgba(255,255,255,0.07);
  --border-hi: rgba(0,212,255,0.35);
  --cyan:      #00d4ff;
  --cyan-dim:  rgba(0,212,255,0.12);
  --cyan-glow: rgba(0,212,255,0.25);
  --white:     #f0f6ff;
  --white-60:  rgba(240,246,255,0.60);
  --white-40:  rgba(240,246,255,0.40);
  --white-20:  rgba(240,246,255,0.20);
  --white-04:  rgba(240,246,255,0.04);
  --mono:      'DM Mono', monospace;
  --display:   'Cabinet Grotesk', sans-serif;
}

/* ── RESET & BASE ── */
*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
[data-testid="stMain"],
section[data-testid="stMain"] > div {
  background: var(--bg) !important;
  color: var(--white) !important;
  font-family: var(--display) !important;
}

/* hide streamlit chrome */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

[data-testid="stMainBlockContainer"] {
  padding: 0 !important;
  max-width: 100% !important;
}

/* ── ANIMATED BACKGROUND ORBS ── */
[data-testid="stAppViewContainer"]::before {
  content: '';
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  background:
    radial-gradient(ellipse 55% 50% at 5% 5%,   rgba(0,212,255,0.13)  0%, transparent 65%),
    radial-gradient(ellipse 50% 45% at 95% 90%,  rgba(0,80,255,0.12)   0%, transparent 65%),
    radial-gradient(ellipse 35% 35% at 50% 50%,  rgba(0,255,180,0.06)  0%, transparent 70%);
  animation: orbDrift 18s ease-in-out infinite;
}
@keyframes orbDrift {
  0%,100% { background-position: 0 0; opacity: 1; }
  50%     { opacity: 0.75; }
}

/* grid overlay */
[data-testid="stAppViewContainer"]::after {
  content: '';
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  background-image:
    linear-gradient(rgba(0,212,255,0.025) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,212,255,0.025) 1px, transparent 1px);
  background-size: 48px 48px;
}

[data-testid="stMain"] { position: relative; z-index: 1; }

/* ── TOP NAV ── */
.rp-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2.5rem;
  height: 60px;
  border-bottom: 1px solid var(--border);
  background: rgba(8,12,16,0.85);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  position: sticky;
  top: 0;
  z-index: 200;
  margin-bottom: 0;
}
.rp-logo {
  font-family: var(--display);
  font-weight: 900;
  font-size: 1.1rem;
  letter-spacing: -0.03em;
  color: var(--white);
  display: flex;
  align-items: center;
  gap: 0.55rem;
}
.rp-logo-dot {
  width: 8px; height: 8px;
  background: var(--cyan);
  border-radius: 50%;
  box-shadow: 0 0 10px var(--cyan), 0 0 20px var(--cyan-glow);
  display: inline-block;
  animation: pulseDot 2.5s ease-in-out infinite;
}
@keyframes pulseDot {
  0%,100% { opacity:1; transform:scale(1); }
  50%     { opacity:0.4; transform:scale(0.65); }
}
.rp-logo em { color: var(--cyan); font-style: normal; }
.rp-status {
  font-family: var(--mono);
  font-size: 0.65rem;
  color: var(--white-40);
  letter-spacing: 0.05em;
  display: flex;
  align-items: center;
  gap: 0.45rem;
}
.rp-status-dot {
  width: 6px; height: 6px;
  background: #00ff88;
  border-radius: 50%;
  box-shadow: 0 0 6px #00ff88;
  display: inline-block;
}

/* ── KILL ALL STREAMLIT DEFAULT SPACING ── */
[data-testid="stMainBlockContainer"],
[data-testid="stVerticalBlock"],
[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="column"] > div:first-child,
[data-testid="stColumn"] > div,
.block-container {
  padding-top: 0 !important;
  padding-bottom: 0 !important;
  gap: 0 !important;
}

/* remove gap between stacked elements inside columns */
[data-testid="stColumn"] [data-testid="stVerticalBlock"] {
  gap: 0.6rem !important;
}


[data-testid="stColumns"] {
  gap: 0 !important;
  margin: 0 !important;
}
[data-testid="stColumn"]:first-child {
  border-right: 1px solid var(--border);
  padding: 2.8rem 2.8rem 2.8rem 2.8rem !important;
}
[data-testid="stColumn"]:last-child {
  padding: 2.8rem 2.8rem 2.8rem 2.8rem !important;
}

/* ── SECTION HEADER ── */
.rp-eyebrow {
  font-family: var(--mono);
  font-size: 0.63rem;
  color: var(--cyan);
  letter-spacing: 0.18em;
  text-transform: uppercase;
  margin-bottom: 0.55rem;
  display: flex;
  align-items: center;
  gap: 0.55rem;
}
.rp-eyebrow::before {
  content: '';
  width: 18px; height: 1px;
  background: var(--cyan);
  box-shadow: 0 0 6px var(--cyan);
}
.rp-title {
  font-family: var(--display);
  font-size: 1.75rem;
  font-weight: 900;
  letter-spacing: -0.04em;
  color: var(--white);
  line-height: 1.1;
  margin-bottom: 0.35rem;
}
.rp-sub {
  font-size: 0.84rem;
  color: var(--white-40);
  margin-bottom: 2.2rem;
  line-height: 1.6;
}

/* ── UPLOAD ZONE (Streamlit file uploader) ── */
[data-testid="stFileUploader"] {
  background: var(--white-04) !important;
  border: 1.5px dashed rgba(0,212,255,0.28) !important;
  border-radius: 16px !important;
  padding: 0.5rem !important;
  transition: border-color 0.25s, box-shadow 0.25s !important;
}
[data-testid="stFileUploader"]:hover {
  border-color: var(--cyan) !important;
  border-style: solid !important;
  box-shadow: 0 0 28px var(--cyan-glow), inset 0 0 28px var(--cyan-dim) !important;
}
[data-testid="stFileUploaderDropzone"] {
  background: transparent !important;
  border: none !important;
  padding: 1.8rem 1rem !important;
  text-align: center !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] {
  color: var(--white-40) !important;
  font-family: var(--display) !important;
  font-size: 0.85rem !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] div span {
  color: var(--white-40) !important;
}
/* Browse files button inside uploader */
[data-testid="stFileUploaderDropzone"] button {
  background: var(--cyan) !important;
  color: #050810 !important;
  border: none !important;
  border-radius: 8px !important;
  font-family: var(--mono) !important;
  font-size: 0.72rem !important;
  font-weight: 500 !important;
  letter-spacing: 0.06em !important;
  padding: 0.55rem 1.3rem !important;
  box-shadow: 0 4px 20px var(--cyan-glow) !important;
  transition: all 0.2s !important;
  text-transform: uppercase !important;
}
[data-testid="stFileUploaderDropzone"] button:hover {
  background: #fff !important;
  box-shadow: 0 6px 30px rgba(0,212,255,0.5) !important;
  transform: translateY(-1px) !important;
}

/* ── OVERVIEW CARD ── */
.rp-overview {
  margin-top: 1.4rem;
  background: var(--white-04);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 1.4rem;
  position: relative;
  overflow: hidden;
}
.rp-overview::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--cyan), #0055ff, transparent);
}
.rp-overview-label {
  font-family: var(--mono);
  font-size: 0.6rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--cyan);
  margin-bottom: 0.65rem;
}
.rp-overview-label::before { content: '// '; opacity: 0.5; }
.rp-overview-text {
  font-size: 0.86rem;
  line-height: 1.85;
  color: var(--white-60);
}

/* ── TEXT INPUT ── */
[data-testid="stTextInput"] label {
  display: none !important;
}
[data-testid="stTextInput"] input {
  background: var(--white-04) !important;
  border: 1.5px solid var(--border) !important;
  border-radius: 12px !important;
  color: var(--white) !important;
  font-family: var(--display) !important;
  font-size: 0.9rem !important;
  font-weight: 500 !important;
  padding: 0.9rem 1.2rem !important;
  caret-color: var(--cyan) !important;
  transition: all 0.2s ease !important;
}
[data-testid="stTextInput"] input::placeholder {
  color: var(--white-20) !important;
}
[data-testid="stTextInput"] input:focus {
  border-color: var(--border-hi) !important;
  background: rgba(0,212,255,0.04) !important;
  box-shadow: 0 0 0 3px var(--cyan-dim), 0 0 20px rgba(0,212,255,0.08) !important;
}

/* ── SUBMIT BUTTON (Match Browse Files Style) ── */
[data-testid="stButton"] > button {
  width: 100% !important;
  background: var(--cyan) !important;
  color: #050810 !important;
  border: none !important;
  border-radius: 8px !important;
  font-family: var(--mono) !important;
  font-size: 0.72rem !important;
  font-weight: 500 !important;
  letter-spacing: 0.06em !important;
  padding: 0.55rem 1.3rem !important;
  box-shadow: 0 4px 20px var(--cyan-glow) !important;
  transition: all 0.2s !important;
  text-transform: uppercase !important;
  cursor: pointer !important;
  margin-top: 0.5rem !important;
}

[data-testid="stButton"] > button:hover {
  background: #fff !important;
  box-shadow: 0 6px 30px rgba(0,212,255,0.5) !important;
  transform: translateY(-1px) !important;
}

[data-testid="stButton"] > button:active {
  transform: translateY(0) !important;
  box-shadow: 0 4px 20px var(--cyan-glow) !important;
}

/* ── ANSWER CARD ── */
.rp-answer-header {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin-bottom: 0.9rem;
  font-family: var(--mono);
  font-size: 0.6rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--white-40);
}
.rp-answer-header::before { content: '//'; color: var(--cyan); opacity: 0.7; margin-right: 0.2rem; }
.rp-answer-header::after  { content: ''; flex: 1; height: 1px; background: var(--border); }

.rp-answer-bubble {
  background: var(--white-04);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 1.4rem;
  font-size: 0.87rem;
  line-height: 1.9;
  color: var(--white-60);
  position: relative;
  overflow: hidden;
  margin-bottom: 1.5rem;
  animation: fadeUp 0.4s ease;
}
.rp-answer-bubble::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg, var(--cyan-dim), transparent);
}
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ── CITATIONS (Streamlit expanders) ── */
.rp-cite-header {
  font-family: var(--mono);
  font-size: 0.6rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--white-40);
  margin-bottom: 0.65rem;
}
.rp-cite-header::before { content: '// '; color: var(--cyan); opacity: 0.5; }

[data-testid="stExpander"] {
  background: var(--white-04) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  margin-bottom: 0.5rem !important;
  transition: border-color 0.2s !important;
}
[data-testid="stExpander"]:hover {
  border-color: rgba(0,212,255,0.22) !important;
}
[data-testid="stExpander"] summary {
  font-family: var(--mono) !important;
  font-size: 0.72rem !important;
  color: var(--white-40) !important;
  padding: 0.75rem 1rem !important;
}
[data-testid="stExpander"] summary:hover {
  color: var(--white-60) !important;
}
[data-testid="stExpander"] .streamlit-expanderContent {
  font-size: 0.8rem !important;
  font-style: italic !important;
  color: var(--white-40) !important;
  line-height: 1.75 !important;
  padding: 0.75rem 1rem 0.9rem !important;
  border-top: 1px solid var(--border) !important;
}

/* score pill */
.rp-score {
  display: inline-block;
  background: var(--cyan-dim);
  color: var(--cyan);
  border-radius: 4px;
  padding: 0.12rem 0.5rem;
  font-family: var(--mono);
  font-size: 0.65rem;
  margin-left: 0.5rem;
}

/* ── ALERTS ── */
[data-testid="stAlert"] {
  background: var(--white-04) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  color: var(--white-60) !important;
  font-family: var(--display) !important;
  font-size: 0.85rem !important;
}

/* ── SPINNER ── */
[data-testid="stSpinner"] > div {
  border-top-color: var(--cyan) !important;
}
[data-testid="stSpinner"] p {
  font-family: var(--mono) !important;
  font-size: 0.72rem !important;
  color: var(--cyan) !important;
  letter-spacing: 0.05em !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(0,212,255,0.2); border-radius: 3px; }

/* ── SUCCESS ── */
.rp-success {
  font-family: var(--mono);
  font-size: 0.72rem;
  color: #00ff88;
  display: flex;
  align-items: center;
  gap: 0.4rem;
  margin-top: 0.8rem;
  letter-spacing: 0.04em;
}
</style>
""", unsafe_allow_html=True)

# ── TOP NAV ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="rp-nav">
  <div class="rp-logo">
    <span class="rp-logo-dot"></span>
    <span>Research<em>AI</em></span>
  </div>
  <div class="rp-status">
    <span class="rp-status-dot"></span>
    System online
  </div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="small")

# ── LEFT PANEL: UPLOAD ─────────────────────────────────────────────────────
with col1:
    st.markdown("""
    <div class="rp-eyebrow">Step 01</div>
    <div class="rp-title">Upload Paper</div>
    <div class="rp-sub">Drop your PDF and we'll extract, parse, and index the full document instantly.</div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"],
        label_visibility="collapsed"
    )

    if uploaded_file is not None:
        with st.spinner("Parsing document…"):
            files = {"file": ("document.pdf", uploaded_file.getvalue(), "application/pdf")}
            try:
                response = requests.post(f"{BACKEND_URL}/upload", files=files)
                response.raise_for_status()
                data = response.json()

                st.markdown('<div class="rp-success">✦ Document indexed successfully</div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="rp-overview">
                  <div class="rp-overview-label">Overview</div>
                  <div class="rp-overview-text">{data["overview"]}</div>
                </div>
                """, unsafe_allow_html=True)

            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to backend. Make sure the server is running on port 8000.")
            except Exception as e:
                st.error(f"Upload failed: {str(e)}")

# ── RIGHT PANEL: Q&A ───────────────────────────────────────────────────────
with col2:
    st.markdown("""
    <div class="rp-eyebrow">Step 02</div>
    <div class="rp-title">Ask Anything</div>
    <div class="rp-sub">Query the paper using natural language. Get cited, sourced answers in seconds.</div>
    """, unsafe_allow_html=True)

    question = st.text_input(
        "Question",
        placeholder="What methodology did the authors use?",
        label_visibility="collapsed"
    )

    submit = st.button("Run Query →")

    if submit:
        if not question.strip():
            st.warning("Please enter a question first.")
        else:
            with st.spinner("Retrieving answer…"):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/ask",
                        params={"question": question}
                    )
                    response.raise_for_status()
                    data = response.json()

                    # Answer
                    st.markdown(f"""
                    <div class="rp-answer-header">Answer</div>
                    <div class="rp-answer-bubble">{data["answer"]}</div>
                    """, unsafe_allow_html=True)

                    # Citations
                    if data.get("citations"):
                        st.markdown('<div class="rp-cite-header">Sources</div>', unsafe_allow_html=True)
                        for citation in data["citations"]:
                            score = round(citation["score"], 3)
                            with st.expander(f"Block {citation['block']}   ·   Score {score}"):
                                st.write(citation["excerpt"])

                except requests.exceptions.ConnectionError:
                    st.error("Cannot connect to backend. Make sure the server is running on port 8000.")
                except Exception as e:
                    st.error(f"Query failed: {str(e)}")

