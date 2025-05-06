from google import genai
from google.genai import types


class GeminiClient:
    conversation: list[types.Content] = []

    def __init__(self, api_key, model="gemini-2.0-flash"):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def add_message(self, message: str, role: str = "user"):
        if role != "user" and role != "model":
            raise ValueError("Role must be 'user' or 'model'")

        content_type = types.ModelContent if role == "model" else types.UserContent
        self.conversation.append(
            content_type(
                parts=[types.Part.from_text(text=message)]
            )
        )

    def generate_response(self, prompt) -> str:
        self.add_message(prompt, role="user")

        response = self.client.models.generate_content(
            model=self.model, contents=self.conversation
        )

        if response:
            self.add_message(response.text, role="model")
            return response.text
        raise Exception("No response from Gemini!")
