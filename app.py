import os

from dotenv import load_dotenv
from flask import Flask

from gemini import GeminiClient

app = Flask(__name__)

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = GeminiClient(api_key=api_key)


@app.route('/')
def hello_world():  # put application's code here
    response = client.generate_response("Explain how AI works in a few words")
    return response


if __name__ == '__main__':
    app.run()
