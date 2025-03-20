import sqlite3
from typing import List, Dict
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load SBERT model (this can be loaded once in your production code)
model = SentenceTransformer("all-MiniLM-L6-v2")

def match_opportunities(user_profile: Dict[str, str]) -> List[Dict[str, str]]:
    """
    Matches user profile to opportunities from the SQLite database using SBERT embeddings.
    
    Parameters:
        user_profile (dict): A dictionary of user interests and study fields.
    
    Returns:
        List[dict]: Top 5 matching opportunities with relevant details.
    """
    user_query = " ".join(user_profile.values())
    user_embedding = model.encode(user_query, convert_to_numpy=True)

    conn = sqlite3.connect("opportunities.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM opportunities")
    rows = cursor.fetchall()
    conn.close()

    job_texts = [
        " ".join(str(field) for field in [row[1], row[2], row[12], row[13]] if field and field != "N/A")
        for row in rows
    ]

    if job_texts:
        job_embeddings = model.encode(job_texts, convert_to_numpy=True)
        scores = cosine_similarity([user_embedding], job_embeddings)[0]
    else:
        scores = []

    results = [
        {
            "title": row[0],
            "company": row[1],
            "location": row[2],
            "job_type": row[3],
            "deadline": row[4],
            "link": row[5],
            "source": row[6],
            "similarity_score": round(float(scores[i]), 2)
        }
        for i, row in enumerate(rows)
    ]

    top_results = sorted(results, key=lambda x: x["similarity_score"], reverse=True)[:10]
    return top_results

if __name__ == "__main__":
    user_profile = {
        "interest": "Machine Learning, AI",
        "study_field": "Computer Science"
    }

    top_matches = match_opportunities(user_profile)
    for match in top_matches:
        print(f"{match['title']} at {match['company']} ({match['similarity_score']:.2f}) - {match['link']}")