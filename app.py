import logging
import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

from database import FormSubmission, db
from gemini import GeminiClient

app = Flask(__name__)
app.config.from_object('config.Config')
if app.config['DEBUG']:
    app.logger.setLevel(logging.INFO)

# Database init
db.init_app(app)
with app.app_context():
    db.create_all()

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


@app.route('/submit_form', methods=['POST'])
def submit_form():
    try:
        form_data = request.json
        submission = FormSubmission(
            firstname=form_data.get('firstname'),
            lastname=form_data.get('lastname'),
            email=form_data.get('email'),
            reason_of_contact=form_data.get('reason_of_contact'),
            urgency=form_data.get('urgency')
        )
        db.session.add(submission)
        db.session.commit()
        return jsonify({"success": True, "id": submission.id})
    except Exception as e:
        app.logger.error(f"Couldn't submit the form: {str(e)}")
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/submissions')
def view_submissions():
    submissions = FormSubmission.query.all()
    return render_template('submissions.html', submissions=submissions)


@app.route('/')
def hello_world():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
