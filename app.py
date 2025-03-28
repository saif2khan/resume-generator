# app.py
from flask import Flask, request, send_file
from docxtpl import DocxTemplate
import tempfile
import json
import os

app = Flask(__name__)

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
    app.run(debug=True)
