from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('GOOGLE_GENAI_API_KEY')


client = genai.Client(api_key="API_KEY")
response = client.models.generate_content(
    model="gemini-2.0-flash", contents="Gave a sample review to a place"
)
print(response.text)