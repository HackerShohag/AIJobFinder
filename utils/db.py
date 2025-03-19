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
            deadline TEXT,
            link TEXT,
            source TEXT,
            score REAL
        )
    """)

    # Save all columns including company, source, score
    df.to_sql("opportunities", conn, if_exists="replace", index=False)
    
    conn.commit()
    conn.close()
    print("Data saved to database!")
