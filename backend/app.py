import os
from flask import Flask, flash, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
from llm_test import compare_cv_and_job
from scrape_jobs import scrape_linkedin_jobs
from extractor2 import process_cv

app = Flask(__name__)
CORS(app, supports_credentials=True)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.urandom(24)

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Flask server running"}), 200

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        try:
            result = process_cv(file_path)
            if 'error' in result:
                return jsonify(result), 400
            # print("Extracted Keywords: ", result)
            return jsonify({
                "success": True,
                "message": "File uploaded and processed successfully",
                "extracted_keywords": result["keywords"],
                "extracted_text": result["extracted_text"]
            }), 200
        except Exception as e:
            print(f"Error during keyword extraction: {e}")
            return jsonify({"error": "Error during keyword extraction"}), 500

    return jsonify({"error": "File type not allowed"}), 400

@app.route('/scrape_jobs', methods=['POST'])
def scrape_jobs():
    data = request.get_json()
    keywords = data.get('keywords', [])
    location = data.get('location', 'Remote')

    if not keywords:
        return jsonify({"error": "No keywords provided"}), 400

    try:
        jobs = scrape_linkedin_jobs(keywords, location)
        for job in jobs:
            print("Job:", job)
        if jobs:
            return jsonify({'jobs': jobs})
        else:
            return jsonify({'error': 'No jobs found'}), 404
    except Exception as e:
        print(f"Error during scraping: {e}")
        return jsonify({'error': 'Failed to fetch jobs'}), 500

@app.route('/compare', methods=['POST'])
def compare():
    data = request.get_json()
    originalText = data.get('cv_text', [])
    jobUrl = data.get('job_url', [])

    print("Original Text:", originalText)
    print("Job URL:", jobUrl)

    data = compare_cv_and_job(originalText, jobUrl)

    return jsonify({"message": "Comparison successful", "response": data}), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)
