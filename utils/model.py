import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def match_opportunities(user_profile):
    conn = sqlite3.connect("opportunities.db")
    cursor = conn.cursor()

    cursor.execute("SELECT title, link FROM opportunities")
    data = cursor.fetchall()
    
    titles = [row[0] for row in data]
    links = [row[1] for row in data]

    # Combine user research interests and study field
    user_query = user_profile["study_field"] + " " + user_profile["research_interests"]

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([user_query] + titles)
    
    # Compute similarity scores
    scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    
    # Rank results
    ranked_results = sorted(zip(scores, titles, links), reverse=True)[:5]

    print("\n Recommended Opportunities:")
    for score, title, link in ranked_results:
        print(f"- {title} ({link}) [Score: {score:.2f}]")