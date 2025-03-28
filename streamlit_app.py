import streamlit as st
from services.speech_recognition import SpeechRecognition
from services.speech_synthesize import SpeechGenerator
from services.llm_response import OpenAIGenerator

# Configure page layout and title
st.set_page_config(page_title="AI Chatbot", layout="wide")

# Sidebar for logo and title
with st.sidebar:
    st.image("inputs//bot1.png", width=100,)  # Replace with your logo file or URL
    st.title("AI Chatbot")

# Initialize session states
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Stores chat messages

# Helper functions
def add_user_text(user_text: str):
    """Add user text to the chat and generate a bot response."""
    st.session_state.chat_history.append({"type": "user_text", "content": user_text})
    
    # Generate bot response
    llm = OpenAIGenerator()
    response = llm.get_response(user_text)
    
    st.session_state.chat_history.append({"type": "bot_text", "content": response})
    st.rerun()  # Force UI update

def add_user_audio(audio_file):
    """Add user audio to the chat and generate a bot response with audio and transcription."""
    st.session_state.chat_history.append({"type": "user_audio", "content": audio_file})  # User's audio

    # Transcribe the audio
    transcriber = SpeechRecognition()
    transcription = transcriber.transcribe(audio_file)
    
    # Generate bot response
    llm = OpenAIGenerator()
    response = llm.get_response(transcription)
    
    # Generate speech for bot response
    speech_gen = SpeechGenerator()
    bot_audio = speech_gen.generate_speech(response)

    # Bot responds with the same audio (later, replace with generated TTS)
    st.session_state.chat_history.append({"type": "bot_audio", "content": bot_audio})
    # Bot responds with transcribed text
    st.session_state.chat_history.append({"type": "bot_text", "content": response})
    st.rerun()  # Force UI update

# Main chat container
chat_container = st.container()
with chat_container:
    st.markdown("## Chat History")
    for message in st.session_state.chat_history:
        if message["type"] == "user_text":
            st.markdown(f"**You:** {message['content']}")
        elif message["type"] == "bot_text":
            st.markdown(f"**Bot:** {message['content']}")
        elif message["type"] == "user_audio":
            st.markdown("**You:**")
            st.audio(message["content"], format="audio/wav")  # Play user audio
        elif message["type"] == "bot_audio":
            st.markdown("**Bot:**")
            st.audio(message["content"], format="audio/wav")  # Play bot audio

# Input bar (single row)
input_container = st.container()
with input_container:
    col_text, col_mic, col_send = st.columns([6, 2, 1])

    with col_text:
        user_text = st.text_input("Type your message here", placeholder="Type your message here...", label_visibility="collapsed")

    with col_mic:
        audio_file = st.audio_input(label="🎤", label_visibility="collapsed")

    with col_send:
        if st.button("Send"):
            if user_text.strip():
                add_user_text(user_text.strip())
            elif audio_file is not None:
                add_user_audio(audio_file)
            else:
                st.warning("Please type a message or record audio before sending.")
