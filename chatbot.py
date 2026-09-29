
import streamlit as st
import ollama
from pathlib import Path

# ======================================
# PAGE CONFIG
# ======================================

st.set_page_config(
    page_title="UR FRND",
    page_icon="😊👀",
    layout="wide"
)

# ======================================
# LOAD CSS
# ======================================

css_path = Path(__file__).parent / "style.css"

if css_path.exists():
    st.markdown(
        f"<style>{css_path.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True
    )

# ======================================
# SESSION STATE
# ======================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

if "mood" not in st.session_state:
    st.session_state.mood = "Chill & chat"

# ======================================
# NOVA PERSONALITY
# ======================================

SYSTEM_PROMPT = """

Your vibe:
- You sound like a fun, thoughtful friend who enjoys helping people.
- Be conversational, natural, welcoming, and encouraging.
- Use simple English unless the user speaks another language.
- Use a little humor and occasional emojis when appropriate.
- Never overdo emojis, jokes, or greetings.
- Be kind without being fake or overly enthusiastic.
- Never pretend to be human or claim real-life experiences.

Your answers:
- Answer the user's actual question first.
- Give accurate and useful information.
- Explain complicated topics in simple steps.
- Use examples, lists, and code when they help.
- Keep easy answers short and detailed requests thorough.
- Ask a brief clarifying question when essential details are missing.
- If you are unsure, clearly say so. Never invent facts.
- If the user asks for code, provide complete runnable code when possible.
- Be transparent that you can make mistakes.

Conversation:
- Use the conversation history to understand follow-up questions.
- Remember the user's chosen mood and adapt your tone naturally.
- In Brainstorm mode, help generate and develop ideas.
- In Code buddy mode, explain and debug code patiently.
- In Chill & chat mode, respond naturally and casually.
- In Teach me stuff mode, make learning engaging and step-by-step.

Your job is to make conversations useful, interesting, and enjoyable.
"""

# ======================================
# HEADER
# ======================================

st.markdown("""
        <div>
            <div class="tagline">YOUR AI</div>
        </div>
""", unsafe_allow_html=True)

# ======================================
# SIDEBAR
# ======================================

with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-symbol">😎</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("YOUR SPACE")

    if st.button("＋  New conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_prompt = None
        st.session_state.mood = "Chill & chat"
        st.rerun()

    st.markdown("---")
    st.markdown("### CURRENT MOOD")

    moods = [
        "🧠 Brainstorm mode",
        "💻 Code buddy",
        "☕ Chill & chat",
        "🚀 Teach me stuff"
    ]

    for mood_label in moods:
        mood_name = mood_label.split(" ", 1)[1]
        if st.button(
            mood_label,
            key=f"mood_{mood_name}",
            use_container_width=True
        ):
            st.session_state.mood = mood_name
            st.rerun()

    st.markdown("---")

    st.markdown("### CHAT STATS")
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-number">
                {len(st.session_state.messages)}
            </div>
            <div class="stat-label">Messages in this chat</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="sidebar-bottom">
        <div>MADE FOR CURIOUS MINDS</div>
        <p>Keep creating...</p>
    </div>
    """, unsafe_allow_html=True)

# ======================================
# WELCOME SCREEN
# ======================================

if not st.session_state.messages:

    st.markdown("""
    <div class="hero">
        <div class="hero-eyebrow">
            <span></span> YOUR PERSONAL AI UNIVERSE
        </div>
        <h1>Hey, human! <span>👀</span></h1>
        <h2>Your brain has questions.<br>
            I've got <span>ideas.</span></h2>
        <p class="hero-description">
            Need a little inspiration, a coding partner,
            or someone to talk to? I'm all ears.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="mood-title">PICK YOUR MOOD <span>✧</span></div>',
        unsafe_allow_html=True
    )

    # ==================================
    # MOOD CARDS
    # ==================================

    cards = [
        {
            "emoji": "🧠",
            "name": "Brainstorm mode",
            "desc": "Big ideas start here.",
            "prompt": "Let's brainstorm! Give me some creative ideas and ask what I'm interested in."
        },
        {
            "emoji": "💻",
            "name": "Code buddy",
            "desc": "Debug, build, repeat.",
            "prompt": "Hey Nova, be my coding buddy! Help me learn and build something cool."
        },
        {
            "emoji": "☕",
            "name": "Chill & chat",
            "desc": "No agenda. Just vibes.",
            "prompt": "Hey Nova! Let's have a fun, friendly conversation. Ask me something interesting."
        },
        {
            "emoji": "🚀",
            "name": "Teach me stuff",
            "desc": "Make learning fun.",
            "prompt": "I want to learn something interesting. Suggest a fascinating topic and teach me in simple steps."
        }
    ]

    cols = st.columns(4, gap="medium")

    for i, card in enumerate(cards):
        with cols[i]:
            st.markdown(
                f"""
                <div class="mood-card mood-{i}">
                    <div class="mood-emoji">{card["emoji"]}</div>
                    <div class="mood-name">{card["name"]}</div>
                    <div class="mood-desc">{card["desc"]}</div>
                    <div class="mood-arrow">↗</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                "Let's go →",
                key=f"start_{i}",
                use_container_width=True
            ):
                st.session_state.mood = card["name"]
                st.session_state.pending_prompt = card["prompt"]
                st.rerun()

    st.markdown("""
    <div class="bottom-note">
        <span></span>
        OR JUST TYPE WHATEVER'S ON YOUR MIND
        <span></span>
    </div>
    """, unsafe_allow_html=True)

# ======================================
# CHAT HISTORY
# ======================================

else:
    st.markdown("""
    <div class="chat-heading">
        <div>
            <div class="chat-heading-title">Your conversation </div>
            <div class="chat-heading-sub">Let's keep the ideas flowing.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# ======================================
# CHAT INPUT
# ======================================

user_input = st.chat_input(
    "what's on your mind? "
)

if st.session_state.pending_prompt:
    user_input = st.session_state.pending_prompt
    st.session_state.pending_prompt = None

# ======================================
# SEND MESSAGE TO AI
# ======================================

if user_input and user_input.strip():

    st.session_state.messages.append({
        "role": "user",
        "content": user_input.strip()
    })

    with st.chat_message("user"):
        st.markdown(user_input.strip())

    with st.chat_message("assistant"):
        with st.spinner("Nova is cooking up a reply... ✨"):
            try:
                response = ollama.chat(
                    model="llama3.2",
                    messages=[
                        {
                            "role": "system",
                            "content": SYSTEM_PROMPT
                            + "\nCurrent conversation mood: "
                            + st.session_state.mood
                        },
                        *st.session_state.messages
                    ],
                    options={
                        "temperature": 0.75,
                        "num_ctx": 8192
                    }
                )

                ai_reply = response["message"]["content"].strip()

                if not ai_reply:
                    ai_reply = "My thoughts got a little tangled. Could you ask me that again?"

                st.markdown(ai_reply)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": ai_reply
                })

            except Exception as e:
                st.error(
                    "Oops! I couldn't reach my AI brain. "
                    "Check that Ollama is running and Llama 3.2 is installed."
                )
                st.caption(str(e))