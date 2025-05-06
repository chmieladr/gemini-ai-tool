from google import genai


class GeminiClient:
    def __init__(self, api_key, model="gemini-2.0-flash"):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def generate_response(self, prompt):
        response = self.client.models.generate_content(
            model=self.model, contents=prompt
        )
        return response.text
