import json

from google import genai
from google.genai import types

from form import HelpdeskForm

system_instruction = """
    You are a helpful assistant. Your goal is to help the user fill out a helpdesk form.

    At the end of every single response you make,
    always print the complete current form status as a JSON object in exactly the following format:
    ```json
    {
        "firstname": "John",
        "lastname": "Doe",
        "email": "johndoe@gmail.com",
        "reason_of_contact": "Technical issue",
        "urgency": 6
    }
    ```

    Replace values in the JSON with the actual data provided by the user.
    Fields without provided data yet should contain empty strings.
"""


class GeminiClient:
    conversation: list[types.Content] = []

    def __init__(self, api_key, model="gemini-2.0-flash"):
        self.system_instruction = system_instruction

        self.client = genai.Client(api_key=api_key)
        self.model = model
        self.config = types.GenerateContentConfig(
            system_instruction=types.Part.from_text(
                text=self.system_instruction
            ),
        )

        self.form = HelpdeskForm(
            firstname="Unknown",
            lastname="Unknown",
            email="example@gmail.com",
            reason_of_contact="Unknown",
            urgency=1
        )

    def generate_response(self, prompt) -> str:
        self.add_message(prompt, role="user")

        try:
            response = self.client.models.generate_content(
                model=self.model, config=self.config, contents=self.conversation
            )

            if response:
                txt = response.text
                self.add_message(txt, role="model")
                self.update_form(txt)
                return txt.split('```json')[0].strip()
        except Exception as e:
            return f"{e} | Sorry, I encountered an issue while processing your request. Please try again."

    def add_message(self, message: str, role: str = "user"):
        if role != "user" and role != "model":
            raise ValueError("Role must be 'user' or 'model'")

        content_type = types.ModelContent if role == "model" else types.UserContent
        self.conversation.append(
            content_type(
                parts=[types.Part.from_text(text=message)]
            )
        )

    def get_form_state(self) -> dict:
        return self.form.model_dump()

    def update_form(self, response: str):
        if '```json' in response:
            json_str = response.split('```json')[1].split('```')[0].strip()
            try:
                data = json.loads(json_str)
                for key, value in data.items():
                    if hasattr(self.form, key) and value is not None and value != "":
                        setattr(self.form, key, value)
            except json.JSONDecodeError:
                return  # Do nothing if JSON invalid
