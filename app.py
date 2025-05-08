import logging
import os

from dotenv import load_dotenv
from flask import Flask, render_template, request

from gemini import GeminiClient

app = Flask(__name__)
app.config.from_object('config.Config')
if app.config['DEBUG']:
    app.logger.setLevel(logging.INFO)

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = GeminiClient(
    api_key=api_key,
    model=app.config['GEMINI_MODEL'],
    temperature=app.config['GEMINI_TEMPERATURE'],
    system_instruction=app.config['SYSTEM_INSTRUCTION']
)


@app.route('/get_form_state')
def get_form_state():
    form_state = client.get_form_state()
    app.logger.info(f"Current form state: {form_state}")
    return form_state


@app.route('/get_response')
def get_response():
    prompt = request.args.get('prompt')
    app.logger.info(f"Calling Gemini with prompt: {prompt}")

    response = client.generate_response(prompt)
    return response


@app.route('/')
def hello_world():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
