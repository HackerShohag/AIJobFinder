from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)

def match_opportunities(user_data):
    conn = sqlite3.connect("utils/opportunities.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT title, link FROM opportunities")
    data = cursor.fetchall()
    
    titles = [row[0] for row in data]
    links = [row[1] for row in data]

    user_query = user_data["study_field"] + " " + user_data["research_interests"]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([user_query] + titles)
    scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    
    ranked_results = sorted(zip(scores, titles, links), reverse=True)[:5]

    return [{"title": title, "link": link, "score": round(score, 2)} for score, title, link in ranked_results]

@app.route("/recommend", methods=["POST"])
def recommend():
    user_data = request.json
    print("User data: ", user_data)
    recommendations = match_opportunities(user_data)
    return jsonify(recommendations)

if __name__ == "__main__":
    app.run(debug=True)

