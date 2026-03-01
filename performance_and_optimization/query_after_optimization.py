import sqlite3
import time

conn = sqlite3.connect("amazon_reviews.db")
cursor = conn.cursor()

print("AFTER OPTIMIZATION:\n")

# Query 1
start = time.time()
cursor.execute("SELECT COUNT(*) FROM reviews WHERE category='Highly Recommended'")
cursor.fetchone()
end = time.time()
q1 = end - start
print("Query 1 Time:", q1)

# Query 2
start = time.time()
cursor.execute("SELECT AVG(score) FROM reviews")
cursor.fetchone()
end = time.time()
q2 = end - start
print("Query 2 Time:", q2)

# Query 3
start = time.time()
cursor.execute("SELECT * FROM reviews WHERE rating >= 4")
cursor.fetchall()
end = time.time()
q3 = end - start
print("Query 3 Time:", q3)

conn.close()