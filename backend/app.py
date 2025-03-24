import os
from flask import Flask, flash, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
from scrape_jobs import scrape_linkedin_jobs



from extractor2 import process_cv  # Importing the process_cv function


app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:3000"])  # 👈 Make sure to match the React port here

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.urandom(24)

# Check for allowed file types
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file')
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save the file to the upload folder
        file.save(file_path)

        try:
            # Process the CV to extract text and keywords
            result = process_cv(file_path)
            
            # Check if error is in the result
            if 'error' in result:
                return jsonify(result), 400

            # Log extracted keywords to the console
            print("Extracted Keywords: ", result.get('keywords', []))

            # scraped_jobs = scrape_jobs(result['keywords'])

            # print("Scraped Jobs: ", scraped_jobs)

            return jsonify({
                "success": True,
                "message": "File uploaded and processed successfully",
                "extracted_keywords": result["keywords"],
                # "jobs": scraped_jobs
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
            print("Job:", job) # Print each job in a new line
        if jobs:
            return jsonify({'jobs': jobs})
        else:
            return jsonify({'error': 'No jobs found'}), 404
    except Exception as e:
        print(f"Error during scraping: {e}")
        return jsonify({'error': 'Failed to fetch jobs'}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
