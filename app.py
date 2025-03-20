from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from utils.model import match_opportunities as fetch_opportunities
from utils.scraper import aggregate_jobs

app = Flask(__name__)
CORS(app)

def match_opportunities(user_data):

    # Aggregate job listings
    aggregate_jobs(user_data)

    # Fetch similarity scores
    ranked_results = fetch_opportunities(user_data)

    # print ranked_results
    print("Ranked Results: ", ranked_results)

    return ranked_results

@app.route("/recommend", methods=["POST"])
def recommend():
    user_data = request.json
    recommendations = match_opportunities(user_data)
    return jsonify(recommendations)

if __name__ == "__main__":
    app.run(debug=True)
