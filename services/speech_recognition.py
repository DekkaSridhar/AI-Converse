import os
import requests
import dotenv
# Load environment variables
dotenv.load_dotenv()
from typing import Optional, BinaryIO

class SpeechRecognition:
    def __init__(self):
        
        # Retrieve API key and URL with error handling
        self.api_key = os.getenv('HUGGINGFACE_API_KEY')
        self.api_url = "https://api-inference.huggingface.co/models/openai/whisper-large-v3-turbo"

    def transcribe(self, audio_file: BinaryIO) -> Optional[str]:
        """
        Transcribe an audio file using Whisper API.
        Args:
            audio_file (BinaryIO): A file-like object containing the audio data.
        
        Returns:
            Optional[str]: Transcribed text or None if transcription fails.
        """
        try:
            # Validate input
            if not audio_file:
                raise ValueError("No audio file provided")
            
            # Ensure the file pointer is at the beginning
            audio_file.seek(0)
            
            # Prepare request headers
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/octet-stream"
            }
            
            # Send POST request to transcription API
            response = requests.post(
                self.api_url, 
                headers=headers, 
                data=audio_file.read()
            )
            
            # Check response status
            response.raise_for_status()
            
            # Parse and return transcription
            result = response.json()
            return result.get("text", "No text output available.")
        
        except requests.RequestException as e:
            print(f"API Request Error: {e}")
            return None
        except ValueError as e:
            print(f"Validation Error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error during transcription: {e}")
            return None