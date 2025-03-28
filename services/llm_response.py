import os
import dotenv
from openai import AzureOpenAI
dotenv.load_dotenv()
class OpenAIGenerator:
    def __init__(self):
        self.client = AzureOpenAI(
            azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
            api_key=os.getenv('AZURE_OPENAI_API_KEY'),
            api_version=os.getenv('AZURE_OPENAI_API_VERSION')
        )
        self.deployment_name = os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME')

    def get_response(self, transcription, max_tokens=200):
        try:
            prompt = f"""Task: Provide a comprehensive and insightful response to the following query.
            Query: {transcription}
            Response Guidelines:
            1. Answer directly and comprehensively
            2. Use clear, straightforward language
            3. Maintain a professional and analytical tone
            4. Avoid using:
                - Emojis
                - Special characters
                - Unnecessary symbols
                - Overly casual language
            Specific Constraints:
            - Focus on depth of explanation
            - Provide a well-structured answer
            - Ensure the response is suitable for text-to-speech conversion
            - Aim for clarity and precision in communication
            Context Considerations:
            The response will be converted to speech, so prioritize:
            - Natural flow of language
            - Easy comprehension
            - Logical progression of ideas
            Response Format:
            - Use complete sentences
            - Organize thoughts systematically
            - Explain complex concepts in accessible terms"""
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens
            )
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"OpenAI Error: {e}")
            return "Sorry, I couldn't generate a response."


# def main():
#     # Generate bot response
#     user_text="what is ai"
#     llm = OpenAIGenerator()
#     response = llm.get_response(transcription= user_text)
#     print(response)

# if __name__ == "__main__":
#     main()