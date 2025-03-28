import streamlit as st
from services.speech_recognition import SpeechRecognition
from services.speech_synthesize import SpeechGenerator
from services.llm_response import OpenAIGenerator


def main():
    st.title("🎙️ Voice Recorder App")

    # Create an audio input widget
    audio_file = st.audio_input("Record your voice")

    # Only process if audio is recorded
    if audio_file is not None:
        # Transcribe the audio
        transcriber = SpeechRecognition()
        transcription = transcriber.transcribe(audio_file)
        
        
        # Ensure transcription is not empty
        if transcription:
            # Generate bot response
            llm = OpenAIGenerator()
            response = llm.get_response(transcription)
            
            # Generate speech for bot response
            speech_gen = SpeechGenerator()
            bot_audio = speech_gen.generate_speech(response)
            
            # Display bot's response and audio
            st.markdown(f"**You:** {transcription}")
            st.markdown(f"**Bot:** {response}")
            st.audio(bot_audio)
        else:
            st.warning("Could not transcribe the audio. Please try again.")

# Ensure the main logic runs only when the script is directly executed
if __name__ == "__main__":
    main()     

