from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)

def match_opportunities(user_data):
    conn = sqlite3.connect("opportunities.db")
    cursor = conn.cursor()
    
    # Fetch the enhanced columns from the database
    cursor.execute("SELECT title, company, deadline, link, source, score FROM opportunities")
    data = cursor.fetchall()
    conn.close()

    if not data:
        return []

    # Prepare data for vectorization
    df = pd.DataFrame(data, columns=["title", "company", "deadline", "link", "source", "db_score"])

    # Create user query from multiple inputs
    user_query = f"{user_data.get('study_field', '')} {user_data.get('research_interests', '')} {user_data.get('skills', '')} {user_data.get('job_role', '')} {user_data.get('location', '')}"

    # TF-IDF vectorization for semantic similarity
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([user_query] + df['title'].tolist())
    similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    # Combine database relevance score and similarity score (weighted sum)
    df['similarity_score'] = similarity_scores
    df['final_score'] = df['similarity_score'] * 0.7 + (df['db_score'] / 100) * 0.3  # Adjust weights as needed

    # Sort by the final combined score
    df_sorted = df.sort_values(by='final_score', ascending=False).head(10)

    # Format results for frontend
    results = []
    for _, row in df_sorted.iterrows():
        results.append({
            "title": row['title'],
            "company": row['company'],
            "deadline": row['deadline'],
            "link": row['link'],
            "source": row['source'],
            "score": round(row['final_score'], 2)
        })
    
    return results

@app.route("/recommend", methods=["POST"])
def recommend():
    user_data = request.json
    recommendations = match_opportunities(user_data)
    return jsonify(recommendations)

if __name__ == "__main__":
    app.run(debug=True)
