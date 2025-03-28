# app.py
from flask import Flask, request, send_file, abort
from docxtpl import DocxTemplate
import tempfile
import json
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Get API key from environment variable
API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    raise ValueError("No API_KEY environment variable set")

# Middleware to check API key
def require_api_key(f):
    def decorated(*args, **kwargs):
        # Check if API key is in headers
        api_key = request.headers.get('X-API-Key')
        if api_key and api_key == API_KEY:
            return f(*args, **kwargs)
        else:
            abort(401, description="Invalid or missing API key")
    decorated.__name__ = f.__name__
    return decorated

@app.route("/generate-resume", methods=["POST"])
def generate_resume():
    data = request.get_json()

    # Load your docxtpl template
    doc = DocxTemplate("resume_template_docxtpl.docx")

    # Fill the template with incoming JSON
    doc.render(data)

    # Save to a temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
        output_path = tmp.name
        doc.save(output_path)

    return send_file(output_path, as_attachment=True, download_name="generated_resume.docx")

# Add this code to run the Flask application
if __name__ == "__main__":
    load_dotenv()  # Load variables from .env file
    app.run(debug=True)
