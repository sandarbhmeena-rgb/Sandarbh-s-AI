
import streamlit as st
import json
import uuid
import hashlib
from pathlib import Path

from ai_engine import get_response
from memory import setup_memory, save_memory, get_memories, delete_memory
from voice import speech_to_text, text_to_speech


# ==========================================
# CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Sandarbh's AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

APP_NAME = "Sandarbh's AI"

DATABASE_DIR = Path("database")
DATABASE_DIR.mkdir(exist_ok=True)

HISTORY_FILE = DATABASE_DIR / "chat_history.json"

setup_memory()


# ==========================================
# SESSION STATE
# ==========================================

if "chats" not in st.session_state:
    if HISTORY_FILE.exists():
        try:
            st.session_state.chats = json.loads(
                HISTORY_FILE.read_text(encoding="utf-8")
            )
        except (json.JSONDecodeError, OSError):
            st.session_state.chats = []
    else:
        st.session_state.chats = []

if "current_chat" not in st.session_state:
    st.session_state.current_chat = []

if "chat_id" not in st.session_state:
    st.session_state.chat_id = None

if "processed_audio_hash" not in st.session_state:
    st.session_state.processed_audio_hash = None


# ==========================================
# CHAT HISTORY FUNCTIONS
# ==========================================

def save_chats():

    HISTORY_FILE.write_text(
        json.dumps(
            st.session_state.chats,
            indent=4,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )


def start_new_chat():

    st.session_state.current_chat = []
    st.session_state.chat_id = None


def open_chat(chat):

    st.session_state.current_chat = chat["messages"]
    st.session_state.chat_id = chat["id"]


def update_chat_history():

    if st.session_state.chat_id is None:
        st.session_state.chat_id = str(uuid.uuid4())

    existing_chat = next(
        (
            chat for chat in st.session_state.chats
            if chat["id"] == st.session_state.chat_id
        ),
        None
    )

    title = next(
        (
            message["content"][:35]
            for message in st.session_state.current_chat
            if message["role"] == "user"
        ),
        "New conversation"
    )

    updated_chat = {
        "id": st.session_state.chat_id,
        "title": title,
        "messages": st.session_state.current_chat
    }

    if existing_chat:

        index = st.session_state.chats.index(existing_chat)
        st.session_state.chats[index] = updated_chat

    else:

        st.session_state.chats.append(updated_chat)

    save_chats()


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.stApp {
    background-color: #212121;
    color: #eeeeee;
}

header[data-testid="stHeader"] {
    background-color: #212121;
}

section[data-testid="stSidebar"] {
    background-color: #171717;
    border-right: 1px solid #333333;
}

section[data-testid="stSidebar"] * {
    color: #eeeeee;
}

.main-title {
    font-size: 32px;
    font-weight: 700;
    color: white;
}

.subtitle {
    color: #999999;
    font-size: 15px;
}

.welcome {
    text-align: center;
    padding-top: 100px;
}

.welcome h1 {
    font-size: 36px;
    color: white;
}

.welcome p {
    color: #aaaaaa;
    font-size: 17px;
}

.stChatMessage {
    background-color: transparent;
    border: none;
}

.stChatInput {
    background-color: #303030;
    border: 1px solid #505050;
    border-radius: 20px;
}

.stChatInput textarea {
    color: white;
}

button {
    border-radius: 10px !important;
}

footer {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown("# 🤖 Sandarbh's AI")
    st.caption("Your intelligent AI assistant")

    st.divider()

    if st.button("＋ New Chat", use_container_width=True):

        start_new_chat()
        st.rerun()

    st.divider()

    st.markdown("### Recent conversations")

    if not st.session_state.chats:

        st.caption("No conversations yet.")

    else:

        for chat in reversed(st.session_state.chats):

            if st.button(
                chat.get("title", "New chat")[:35],
                key=f"open_{chat['id']}",
                use_container_width=True
            ):

                open_chat(chat)
                st.rerun()

    st.divider()

    st.markdown("### AI information")

    st.caption("☁️ Cloud AI: Gemini")
    st.caption("💻 Local AI: Ollama Qwen3 1.7B")
    st.caption("🌐 Online research: Enabled")

    st.divider()

    st.markdown("### 🔊 Voice settings")

    speak_responses = st.checkbox(
        "Speak AI responses",
        value=True
    )

    st.caption("Microphone input requires internet.")
    st.caption("AI voice output works offline.")

    st.divider()

    with st.expander("🧠 Personal memory"):

        st.caption("Information saved by you")

        memories = get_memories()

        if not memories:
            st.caption("No memories saved.")

        for memory_id, information in memories:

            st.write(information)

            if st.button(
                "Delete",
                key=f"delete_{memory_id}"
            ):

                delete_memory(memory_id)
                st.rerun()

        st.divider()

        memory_input = st.text_input(
            "Save something to memory",
            key="memory_input"
        )

        if st.button("Save memory"):

            if memory_input.strip():

                save_memory(memory_input.strip())
                st.success("Memory saved!")
                st.rerun()


# ==========================================
# MAIN INTERFACE
# ==========================================

st.markdown(
    '<div class="main-title">Sandarbh\'s AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Ask anything. Explore the world. Learn something new.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ==========================================
# WELCOME SCREEN
# ==========================================

if not st.session_state.current_chat:

    st.markdown("""
    <div class="welcome">

        <h1>What can I help you with?</h1>

        <p>
        Your personal AI for knowledge, creativity,
        learning and discovery.
        </p>

    </div>
    """, unsafe_allow_html=True)


# ==========================================
# DISPLAY CHAT
# ==========================================

for message in st.session_state.current_chat:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ==========================================
# VOICE INPUT
# ==========================================

st.markdown("### 🎤 Ask using your voice")

audio_input = st.audio_input(
    "Record your question"
)

voice_prompt = None

if audio_input is not None:

    audio_bytes = audio_input.getvalue()

    audio_hash = hashlib.sha256(
        audio_bytes
    ).hexdigest()

    if audio_hash != st.session_state.processed_audio_hash:

        st.session_state.processed_audio_hash = audio_hash

        with st.spinner("Understanding your voice..."):

            voice_prompt, voice_error = speech_to_text(
                audio_bytes
            )

        if voice_error:

            st.error(voice_error)

        elif voice_prompt:

            st.success(f"You said: {voice_prompt}")


# ==========================================
# CHAT INPUT
# ==========================================

prompt = st.chat_input(
    "Message Sandarbh's AI..."
)

if not prompt and voice_prompt:
    prompt = voice_prompt


# ==========================================
# GENERATE AI RESPONSE
# ==========================================

if prompt:

    user_message = {
        "role": "user",
        "content": prompt
    }

    st.session_state.current_chat.append(user_message)

    with st.chat_message("user"):
        st.markdown(prompt)

    # Remember command

    if prompt.lower().startswith("remember:"):

        information = prompt[len("remember:"):].strip()

        if information:

            save_memory(information)

            answer = (
                "I've saved that information in "
                "my personal memory. 🧠"
            )

        else:

            answer = "Please tell me what you want me to remember."

    else:

        with st.chat_message("assistant"):

            with st.spinner("Sandarbh's AI is thinking..."):

                answer = get_response(
                    st.session_state.current_chat
                )

            st.markdown(answer)

            # ==================================
            # AI VOICE OUTPUT
            # ==================================

            if speak_responses and answer:

                with st.spinner("Generating voice..."):

                    audio_path, voice_error = text_to_speech(
                        answer
                    )

                if audio_path:

                    try:

                        audio_bytes = Path(audio_path).read_bytes()

                        st.audio(
    audio_bytes,
    format="audio/wav",
    autoplay=True
)

                        Path(audio_path).unlink(missing_ok=True)

                    except Exception as error:

                        st.warning(
                            f"Audio playback error: {error}"
                        )

                elif voice_error:

                    st.warning(voice_error)

    # Save assistant response

    if not answer.startswith("CLOUD_ERROR:"):

        st.session_state.current_chat.append({
            "role": "assistant",
            "content": answer
        })

    else:

        st.error(answer)

    # Save conversation

    update_chat_history()

    st.rerun()
