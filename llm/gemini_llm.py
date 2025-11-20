import os
from google.generativeai import GenerativeModel

class GeminiLLM:
    def __init__(self, model_name="gemini-1.5-pro"):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not set in environment variables")

        self.model = GenerativeModel(model_name)

    def run(self, prompt):
        response = self.model.generate_content(prompt)
        return response.text  # crewai expects text output
