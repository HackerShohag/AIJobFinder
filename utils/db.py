import sqlite3
import pandas as pd

def save_to_db(df):
    conn = sqlite3.connect("opportunities.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS opportunities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            company TEXT,
            location TEXT,
            job_type TEXT,
            deadline TEXT,
            link TEXT,
            source TEXT,
            score REAL,
            posted_date TEXT,
            num_applicants TEXT,
            seniority_level TEXT,
            employment_type TEXT,
            job_function TEXT,
            industry TEXT
        )
    """)

    # Ensure DataFrame has all required columns; if missing, fill with "N/A"
    expected_columns = [
        "title", "company", "location", "job_type", "deadline", "link",
        "source", "score", "posted_date", "num_applicants",
        "seniority_level", "employment_type", "job_function", "industry"
    ]
    for col in expected_columns:
        if col not in df.columns:
            df[col] = "N/A"

    # Reorder columns to match the table schema
    df = df[expected_columns]

    df.to_sql("opportunities", conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()
    print("Data saved to database!")
