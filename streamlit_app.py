import streamlit as st
import requests
import datetime
# v4 - complete rewrite with is_loading, queued_question, thinking bubble

BASE_URL = "https://ai-trip-planner-f1dm.onrender.com"  # Backend endpoint

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --navy:        #0a0e1a;
    --purple:      #6c3fc5;
    --purple-glow: #8b5cf6;
    --violet:      #a78bfa;
    --teal:        #2dd4bf;
    --glass-bg:    rgba(255,255,255,0.04);
    --glass-border:rgba(255,255,255,0.10);
    --text-primary:#e8eaf6;
    --text-muted:  #8892b0;
}

html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0a0e1a 0%, #0d1128 45%, #130d2e 100%) !important;
    font-family: 'DM Sans', sans-serif;
    color: var(--text-primary);
}

/* Star field */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed; inset: 0; z-index: 0; pointer-events: none;
    background-image:
        radial-gradient(1px 1px at 15% 20%, rgba(255,255,255,.50) 0%, transparent 100%),
        radial-gradient(1px 1px at 72%  5%, rgba(255,255,255,.35) 0%, transparent 100%),
        radial-gradient(1px 1px at 40% 80%, rgba(255,255,255,.30) 0%, transparent 100%),
        radial-gradient(1px 1px at 88% 60%, rgba(255,255,255,.45) 0%, transparent 100%),
        radial-gradient(1px 1px at  5% 55%, rgba(255,255,255,.28) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 30% 10%, rgba(167,139,250,.65) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 80% 90%, rgba(45,212,191,.55)  0%, transparent 100%);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0c1022 0%, #11102a 100%) !important;
    border-right: 1px solid var(--glass-border);
}
[data-testid="stSidebar"] * { color: var(--text-primary) !important; }

/* Hide chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

.block-container {
    max-width: 860px !important;
    padding: 2rem 1.5rem 8rem !important;
    margin: 0 auto;
    position: relative; z-index: 1;
}

/* ── Hero ── */
.hero-wrap { text-align: center; padding: 3.2rem 1rem 2.2rem; }
.hero-globe {
    font-size: 3.8rem; display: block; margin-bottom: .5rem;
    animation: floatGlobe 4s ease-in-out infinite;
    filter: drop-shadow(0 0 20px rgba(139,92,246,.85));
}
@keyframes floatGlobe {
    0%,100% { transform: translateY(0);    }
    50%      { transform: translateY(-9px); }
}
.hero-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: clamp(2.2rem, 5vw, 3.4rem);
    font-weight: 900;
    background: linear-gradient(90deg, #c4b5fd 0%, #a78bfa 40%, #2dd4bf 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    line-height: 1.1; letter-spacing: -.02em; margin: 0;
    filter: drop-shadow(0 0 28px rgba(139,92,246,.40));
}
.hero-sub {
    margin-top: .75rem; font-size: 1rem; font-weight: 300;
    color: var(--text-muted); letter-spacing: .01em;
}
.hero-divider {
    width: 76px; height: 2px;
    background: linear-gradient(90deg, transparent, var(--purple-glow), transparent);
    margin: 1.4rem auto 0; border-radius: 2px;
}

/* ── Chat bubbles ── */
.chat-user  { display:flex; justify-content:flex-end;  margin:.75rem 0; animation:fadeUp .35s ease both; }
.chat-bot   { display:flex; justify-content:flex-start; margin:.75rem 0; animation:fadeUp .35s ease both; }
@keyframes fadeUp {
    from { opacity:0; transform:translateY(10px); }
    to   { opacity:1; transform:translateY(0);    }
}
.bubble-user {
    max-width:70%;
    background: linear-gradient(135deg,#4f46e5,#7c3aed);
    color:#fff; padding:.72rem 1.1rem;
    border-radius:18px 18px 4px 18px;
    font-size:.92rem; line-height:1.55;
    box-shadow:0 4px 18px rgba(79,70,229,.38);
    word-wrap:break-word;
}
.bubble-bot-wrap {
    max-width:84%;
    background:rgba(13,19,40,0.88);
    border:1px solid rgba(167,139,250,.22);
    color:var(--text-primary); padding:.88rem 1.2rem;
    border-radius:18px 18px 18px 4px;
    font-size:.92rem; line-height:1.68;
    box-shadow:0 4px 20px rgba(0,0,0,.42);
    word-wrap:break-word;
}
.ts        { font-size:.70rem; color:var(--text-muted); margin-top:.3rem; opacity:.68; }
.ts-right  { text-align:right; margin-right:.25rem; }
.ts-left   { text-align:left;  margin-left:.25rem;  }
.av-bot {
    width:30px; height:30px; flex-shrink:0;
    background:linear-gradient(135deg,var(--purple),var(--teal));
    border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    font-size:.95rem;
    margin-right:.55rem; margin-top:.2rem;
    box-shadow:0 0 12px rgba(139,92,246,.45);
}

/* ── Input overrides ── */
[data-testid="stTextInput"] input {
    background:rgba(255,255,255,.06)!important;
    border:1px solid rgba(139,92,246,.38)!important;
    border-radius:50px!important;
    color:var(--text-primary)!important;
    font-family:'DM Sans',sans-serif!important;
    font-size:.94rem!important;
    padding:.68rem 1.4rem!important;
    caret-color:var(--violet);
    transition:border-color .2s,box-shadow .2s;
}
[data-testid="stTextInput"] input:focus {
    border-color:var(--purple-glow)!important;
    box-shadow:0 0 0 3px rgba(139,92,246,.16)!important;
    outline:none!important;
}
[data-testid="stTextInput"] input::placeholder { color:var(--text-muted)!important; }

[data-testid="stFormSubmitButton"] button,
.stButton button {
    background:linear-gradient(135deg,#6c3fc5 0%,#8b5cf6 100%)!important;
    color:#fff!important; border:none!important;
    border-radius:50px!important;
    padding:.6rem 1.7rem!important;
    font-family:'DM Sans',sans-serif!important;
    font-weight:600!important; font-size:.88rem!important;
    letter-spacing:.04em!important;
    transition:transform .15s,box-shadow .15s!important;
    box-shadow:0 4px 16px rgba(108,63,197,.42)!important;
    white-space:nowrap!important;
}
[data-testid="stFormSubmitButton"] button:hover,
.stButton button:hover {
    transform:translateY(-2px)!important;
    box-shadow:0 8px 24px rgba(108,63,197,.58)!important;
}
[data-testid="stSidebar"] .stButton button {
    background:linear-gradient(135deg,#1e1b4b,#312e81)!important;
    border:1px solid rgba(139,92,246,.28)!important;
    width:100%;
}

/* ── Empty state ── */
.empty-state { text-align:center; padding:4rem 2rem; color:var(--text-muted); }
.empty-state .emo { font-size:3.4rem; margin-bottom:.7rem; }
.empty-state p { font-size:.93rem; }
.chip-row { display:flex; flex-wrap:wrap; gap:.5rem; justify-content:center; margin-top:1.4rem; }
.chip {
    background:rgba(139,92,246,.10);
    border:1px solid rgba(139,92,246,.28);
    border-radius:50px; padding:.38rem .95rem;
    font-size:.80rem; color:var(--violet); cursor:default;
}

/* ── Sidebar elements ── */
.sidebar-section {
    background:rgba(255,255,255,.04);
    border:1px solid rgba(255,255,255,.07);
    border-radius:12px; padding:.9rem 1rem;
    margin-bottom:.9rem; font-size:.83rem;
    color:var(--text-muted); line-height:1.6;
}
.sidebar-title {
    font-family:'Playfair Display',serif;
    font-size:1.2rem; font-weight:700;
    color:var(--violet); margin-bottom:.35rem;
}
.sidebar-prompt {
    background:rgba(255,255,255,.04);
    border-left:3px solid var(--purple);
    border-radius:0 8px 8px 0;
    padding:.45rem .7rem; margin:.35rem 0;
    font-size:.80rem; color:var(--text-primary);
    overflow:hidden; text-overflow:ellipsis;
    white-space:nowrap; max-width:100%;
}

/* ── Footer ── */
.footer {
    text-align:center; padding:2rem 0 .5rem;
    font-size:.76rem; color:var(--text-muted);
    letter-spacing:.06em; text-transform:uppercase;
}
.footer span { color:var(--violet); }

/* ── Hide "Press Enter to submit form" ── */
[data-testid="InputInstructions"] { display:none!important; }

/* ── Chip buttons ── */
.chip-label {
    text-align:center; font-size:.78rem; color:var(--text-muted);
    margin:1.6rem 0 .5rem; letter-spacing:.06em; text-transform:uppercase;
}
.chip-btn button {
    background:rgba(139,92,246,.10)!important;
    border:1px solid rgba(139,92,246,.35)!important;
    border-radius:50px!important; padding:.42rem 1rem!important;
    font-size:.82rem!important; color:var(--violet)!important;
    font-family:'DM Sans',sans-serif!important; font-weight:400!important;
    width:100%!important;
    transition:background .2s,border-color .2s,transform .15s,box-shadow .15s!important;
    box-shadow:none!important;
}
.chip-btn button:hover {
    background:rgba(139,92,246,.22)!important;
    border-color:rgba(139,92,246,.65)!important;
    transform:translateY(-2px)!important;
    box-shadow:0 4px 14px rgba(139,92,246,.28)!important;
    color:#fff!important;
}

/* ── Thinking bubble ── */
.thinking-wrap { display:flex; justify-content:flex-start; margin:.75rem 0; animation:fadeUp .3s ease both; }
.thinking-bubble {
    display:flex; align-items:center; gap:.55rem;
    background:rgba(13,19,40,0.88);
    border:1px solid rgba(167,139,250,.22);
    padding:.75rem 1.2rem; border-radius:18px 18px 18px 4px;
    font-size:.88rem; color:var(--text-muted);
    box-shadow:0 4px 20px rgba(0,0,0,.42);
}
.dot-pulse { display:flex; gap:5px; align-items:center; }
.dot-pulse span {
    width:7px; height:7px; background:var(--violet); border-radius:50%;
    animation:pulse 1.3s ease-in-out infinite;
}
.dot-pulse span:nth-child(2) { animation-delay:.2s; }
.dot-pulse span:nth-child(3) { animation-delay:.4s; }
@keyframes pulse {
    0%,80%,100% { transform:scale(.55); opacity:.35; }
    40%          { transform:scale(1.0); opacity:1;   }
}

/* ── Status card ── */
.status-card {
    background:rgba(139,92,246,.07);
    border:1px solid rgba(139,92,246,.20);
    border-radius:12px; padding:.6rem 1.1rem;
    margin:.4rem 0 .8rem; font-size:.82rem; color:var(--violet);
    display:flex; align-items:center; gap:.5rem; flex-wrap:wrap;
}
.status-step { opacity:.55; font-size:.76rem; }

/* ── Disabled states ── */
[data-testid="stTextInput"] input:disabled { opacity:.45!important; cursor:not-allowed!important; }
[data-testid="stFormSubmitButton"] button:disabled {
    opacity:.55!important; transform:none!important;
    box-shadow:none!important; cursor:not-allowed!important;
}

/* Scrollbar */
::-webkit-scrollbar { width:5px; }
::-webkit-scrollbar-track { background:transparent; }
::-webkit-scrollbar-thumb { background:rgba(139,92,246,.32); border-radius:6px; }

[data-testid="stSpinner"] { color:var(--violet)!important; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ──────────────────────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_query" not in st.session_state:
    st.session_state.pending_query = ""
if "is_loading" not in st.session_state:
    st.session_state.is_loading = False
if "queued_question" not in st.session_state:
    st.session_state.queued_question = ""

# ──────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-title">✈️ AI Travel Planner</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sidebar-section">Your intelligent travel companion.<br>'
        'Plan trips, estimate budgets, discover hidden gems &amp; offbeat destinations worldwide.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.markdown(
        '<div style="font-size:.78rem;color:#8892b0;letter-spacing:.08em;'
        'text-transform:uppercase;margin-bottom:.6rem;">🗺 Your Trips</div>',
        unsafe_allow_html=True,
    )
    user_msgs = [m for m in st.session_state.messages if m["role"] == "user"]
    if user_msgs:
        for msg in user_msgs[-6:]:
            c = msg["content"]
            short = c[:38] + "…" if len(c) > 38 else c
            st.markdown(f'<div class="sidebar-prompt">💬 {short}</div>', unsafe_allow_html=True)
    else:
        st.markdown(
            '<div style="font-size:.80rem;color:#8892b0;padding:.3rem 0;">'
            'No trips planned yet.</div>',
            unsafe_allow_html=True,
        )
    st.markdown("---")
    if st.session_state.messages:
        bot_responses = [m["content"] for m in st.session_state.messages if m["role"] == "bot"]
        if bot_responses:
            st.download_button(
                label="📥 Download Plan",
                data="\n\n---\n\n".join(bot_responses),
                file_name=f"travel_plan_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain",
                use_container_width=True,
            )
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_query = ""
        st.session_state.is_loading = False
        st.session_state.queued_question = ""
        st.rerun()
    st.markdown(
        '<div class="sidebar-section" style="margin-top:1rem;">'
        '<strong style="color:#a78bfa;">Tips 💡</strong><br>'
        '• Mention trip duration<br>• Add budget range<br>'
        '• Specify travel style<br>• Ask for offbeat options</div>',
        unsafe_allow_html=True,
    )

# ──────────────────────────────────────────────────────────────────────────────
# HERO
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <span class="hero-globe">🌍</span>
    <h1 class="hero-title">AI Travel Planner</h1>
    <p class="hero-sub">Plan your perfect journey with an intelligent AI travel agent.</p>
    <div class="hero-divider"></div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# SUGGESTION CHIPS  (only when chat is empty and not loading)
# ──────────────────────────────────────────────────────────────────────────────
SUGGESTIONS = [
    ("🏝", "Bali for 7 days"),
    ("🗼", "Paris weekend trip"),
    ("🏔", "Himalayan trek"),
    ("🌊", "Maldives honeymoon"),
    ("🏛", "Rome & Florence"),
    ("🌸", "Japan in spring"),
]

if not st.session_state.messages and not st.session_state.is_loading:
    st.markdown("""
    <div class="empty-state">
        <div class="emo">🗺️</div>
        <p>Where would you like to go?<br>
        <span style="color:#8b5cf6;">Pick a suggestion below or type your own destination.</span></p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(
        '<div class="chip-label">✦ Popular destinations — click to plan instantly</div>',
        unsafe_allow_html=True,
    )
    row1 = st.columns(3)
    for i in range(3):
        icon, label = SUGGESTIONS[i]
        with row1[i]:
            st.markdown('<div class="chip-btn">', unsafe_allow_html=True)
            if st.button(f"{icon} {label}", key=f"chip_{i}", use_container_width=True):
                now = datetime.datetime.now().strftime("%H:%M")
                st.session_state.messages.append({"role": "user", "content": label, "timestamp": now})
                st.session_state.queued_question = label
                st.session_state.pending_query = ""
                st.session_state.is_loading = True
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    row2 = st.columns(3)
    for i in range(3):
        icon, label = SUGGESTIONS[i + 3]
        with row2[i]:
            st.markdown('<div class="chip-btn">', unsafe_allow_html=True)
            if st.button(f"{icon} {label}", key=f"chip_{i+3}", use_container_width=True):
                now = datetime.datetime.now().strftime("%H:%M")
                st.session_state.messages.append({"role": "user", "content": label, "timestamp": now})
                st.session_state.queued_question = label
                st.session_state.pending_query = ""
                st.session_state.is_loading = True
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# CHAT HISTORY
# ──────────────────────────────────────────────────────────────────────────────
for message in st.session_state.messages:
    ts = message.get("timestamp", "")
    if message["role"] == "user":
        st.markdown(
            f'<div class="chat-user"><div>'
            f'<div class="bubble-user">{message["content"]}</div>'
            f'<div class="ts ts-right">{ts}</div>'
            f'</div></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="chat-bot"><div class="av-bot">✈️</div>'
            '<div class="bubble-bot-wrap">',
            unsafe_allow_html=True,
        )
        st.markdown(message["content"])
        st.markdown(
            f'</div></div>'
            f'<div class="ts ts-left" style="margin-left:2.3rem;">{ts} · AI Travel Agent</div>',
            unsafe_allow_html=True,
        )

# ──────────────────────────────────────────────────────────────────────────────
# THINKING INDICATOR  (renders immediately after submit, before API responds)
# ──────────────────────────────────────────────────────────────────────────────
if st.session_state.is_loading:
    st.markdown("""
    <div class="thinking-wrap">
        <div class="av-bot">✈️</div>
        <div class="thinking-bubble">
            <div class="dot-pulse">
                <span></span><span></span><span></span>
            </div>
            <span>Researching your destination&hellip;</span>
        </div>
    </div>
    <div class="status-card">
        🔍 Fetching weather, attractions, hotels &amp; transport info
        <span class="status-step">— usually takes 20–40 seconds</span>
    </div>
    """, unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="footer">Built with <span>FastAPI</span> + <span>Streamlit</span>'
    ' &nbsp;|&nbsp; Powered by <span>AI</span>'
    ' &nbsp;|&nbsp; LangGraph + Groq</div>',
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────────────────────────────────────
# INPUT FORM
# ──────────────────────────────────────────────────────────────────────────────
with st.form(key="query_form", clear_on_submit=True):
    cols = st.columns([6, 1])
    with cols[0]:
        user_input = st.text_input(
            label="",
            placeholder="✈️  Where do you want to go? e.g. Plan a 5-day trip to Bali...",
            label_visibility="collapsed",
            value=st.session_state.pending_query,
            disabled=st.session_state.is_loading,
        )
    with cols[1]:
        submit_button = st.form_submit_button(
            label="⏳ Wait…" if st.session_state.is_loading else "Send ➤",
            disabled=st.session_state.is_loading,
        )

    if submit_button and user_input.strip() and not st.session_state.is_loading:
        question = user_input.strip()
        now = datetime.datetime.now().strftime("%H:%M")
        st.session_state.messages.append({"role": "user", "content": question, "timestamp": now})
        st.session_state.queued_question = question
        st.session_state.pending_query = ""
        st.session_state.is_loading = True
        st.rerun()  # ← renders thinking bubble BEFORE the API call blocks

# ──────────────────────────────────────────────────────────────────────────────
# API CALL  (fires only after UI has already shown the thinking state)
# ──────────────────────────────────────────────────────────────────────────────
if st.session_state.is_loading and st.session_state.queued_question:
    question = st.session_state.queued_question
    answer = None
    error_msg = None

    try:
        response = requests.post(
            f"{BASE_URL}/query",
            json={"question": question},
            timeout=180,  # 3 min: covers Render cold-start + full LLM tool chain
        )
        if response.status_code == 200:
            answer = response.json().get("answer", "No answer returned.")
        else:
            error_msg = f"⚠️ Backend error (status {response.status_code}): {response.text}"

    except requests.exceptions.ConnectionError:
        error_msg = "⚠️ Could not connect to the backend. Make sure the server is running."
    except requests.exceptions.Timeout:
        error_msg = "⚠️ Request timed out after 3 minutes. The backend may be busy — please try again."
    except Exception as e:
        error_msg = f"⚠️ Unexpected error: {e}"

    if answer:
        formatted = (
            f"## 🌍 Your AI Travel Plan\n\n"
            f"**Generated:** {datetime.datetime.now().strftime('%d %b %Y at %H:%M')}"
            f" &nbsp;·&nbsp; **Powered by:** Atriyo's Travel Agent\n\n---\n\n"
            f"{answer}\n\n---\n"
            f"*Please verify prices, operating hours, and travel requirements before your trip.*"
        )
        st.session_state.messages.append({
            "role": "bot",
            "content": formatted,
            "timestamp": datetime.datetime.now().strftime("%H:%M"),
        })
    elif error_msg:
        st.session_state.messages.append({
            "role": "bot",
            "content": error_msg,
            "timestamp": datetime.datetime.now().strftime("%H:%M"),
        })

    # Reset and show result
    st.session_state.is_loading = False
    st.session_state.queued_question = ""
    st.session_state.pending_query = ""
    st.rerun()