import os

from dotenv import load_dotenv
from flask import Flask, render_template

from gemini import GeminiClient

app = Flask(__name__)

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = GeminiClient(api_key=api_key)


@app.route('/get_response')
def get_response():
    prompt = "Explain how AI works in a few words"
    response = client.generate_response(prompt)
    return response


@app.route('/')
def hello_world():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
