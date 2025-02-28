from google import genai
import os
from dotenv import load_dotenv

# Load API Key from .env file
def configure():
    load_dotenv()

configure()  # Call this function to load environment variables

from google import genai
from google.genai import types

client = genai.Client(api_key=os.getenv("GOOGLE_GENAI_API_KEY"))

def summarize_reviews(text1: str, text2: str, max_length: int = 425) -> str: 
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=["Summarize the following two reviews into one concise and engaging review with a maximum of "  
            f"{max_length} characters:\n\nReview 1: {text1}\n\nReview 2: {text2}\n\n"  
            "Make it informative, balanced, and natural"],
        config=types.GenerateContentConfig(
            max_output_tokens=500,
            temperature=0.1
        )
    )
    return response.text.strip() if response and response.text else "Error: No response generated."



# Sample input
text1 = """The laptop has an impressive battery life and a stunning display. The performance is top-notch, handling all my tasks effortlessly. However, the fan noise can get quite loud under heavy load, which is a bit annoying."""

text2 = """This laptop is lightweight and easy to carry around, making it perfect for travel. The keyboard feels great, and the screen is vibrant. My only complaint is that it gets warm after extended use, but overall, it's a great device."""

summary = summarize_reviews(text1, text2)
print(summary)
