# import pyttsx3
# import tempfile

# class SpeechGenerator:
#     def __init__(self, rate=175, voice_index=1):
#         """Initialize the text-to-speech engine with configurable parameters."""
#         self.engine = pyttsx3.init()
#         self.set_rate(rate)
#         self.set_voice(voice_index)
    
#     def set_rate(self, rate):
#         """Set the speech rate."""
#         self.engine.setProperty('rate', rate)
    
#     def set_voice(self, voice_index):
#         """Set the voice based on the provided index (0 for male, 1 for female)."""
#         voices = self.engine.getProperty('voices')
#         if 0 <= voice_index < len(voices):
#             self.engine.setProperty('voice', voices[voice_index].id)
    
#     def generate_speech(self, transcription):
#         """
#         Convert text to speech and save to a wav file.
        
#         Args:
#             transcription (str): Text to convert to speech
        
#         Returns:
#             str: Path to the generated audio file
#         """
#         if not transcription:
#             return None
        
#         # Create a temporary file to save the audio
#         temp_audio = tempfile.mktemp(suffix=".wav")
        
#         # Save the speech to the temporary file
#         self.engine.save_to_file(transcription, temp_audio)
#         self.engine.runAndWait()
        
#         return temp_audio
    
#     def stop_speech(self):
#         """Stop the speech engine."""
#         self.engine.stop()


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# using gtts 
from gtts import gTTS
import tempfile
import os
import streamlit as st

class SpeechGenerator:
    def __init__(self, language="en", tld="co.uk", slow=False):    # TLD	Effect-> "com"	Default English voice-> "com.au"	Faster Australian English-> "co.uk"	Slightly different UK accent-> "in"	Indian English (sometimes faster)
        self.language = language
        self.tld = tld  # Use a different TLD for faster voices
        self.slow = slow  # Controls speech rate

    def generate_speech(self, text):
        if not text or not text.strip():
            return None
        try:
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
                tts = gTTS(text=text, lang=self.language, tld=self.tld, slow=self.slow)
                tts.save(temp_file.name)
                return temp_file.name
        except Exception as e:
            st.error(f"Error generating speech: {e}")
            return None

    def cleanup_audio(self, audio_path):
        try:
            if audio_path and os.path.exists(audio_path):
                os.unlink(audio_path)
        except Exception as e:
            st.error(f"Error cleaning up audio file: {e}")

# # Example Usage
# speech_gen = SpeechGenerator(language="en", tld="co.uk", slow=False)  # Faster Aussie English
# audio_file = speech_gen.generate_speech("Hello, this is a fast test.")
# print(f"Audio saved at: {audio_file}")

