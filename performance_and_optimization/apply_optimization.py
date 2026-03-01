import sqlite3

conn = sqlite3.connect("amazon_reviews.db")
cursor = conn.cursor()

cursor.execute("CREATE INDEX IF NOT EXISTS idx_category ON reviews(category)")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_rating ON reviews(rating)")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_score ON reviews(score)")

conn.commit()
conn.close()

print("Indexes Applied Successfully!")