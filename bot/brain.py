from google import genai
from google.genai import types

import os

def query(pregunta):
    
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    response = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL"),
            config=types.GenerateContentConfig(
        system_instruction="say beautiful stuff be concise and try to imitate human, MAX CHARACTER 250"
    ),
    contents=pregunta
)
    return response.text # my bad g