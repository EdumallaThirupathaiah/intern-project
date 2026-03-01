import sqlite3
import random
import datetime
from scoring_engine import calculate_score

conn = sqlite3.connect("amazon_reviews.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    review_text TEXT,
    category TEXT,
    rating INTEGER,
    score INTEGER,
    created_at TEXT
)
""")

categories = ["Highly Recommended", "Recommended", "Average"]
words = ["good", "excellent", "love", "amazing", "bad", "terrible"]

batch = []

for i in range(1_000_000):
    text = " ".join(random.choices(words, k=5))
    category = random.choice(categories)
    rating = random.randint(1, 5)
    score = calculate_score(text)

    batch.append((text, category, rating, score, str(datetime.datetime.now())))

    if len(batch) == 10000:
        cursor.executemany("""
        INSERT INTO reviews (review_text, category, rating, score, created_at)
        VALUES (?, ?, ?, ?, ?)
        """, batch)
        conn.commit()
        batch = []

conn.close()
print("1 Million Records Inserted Successfully!")