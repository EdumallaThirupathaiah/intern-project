import sqlite3
from multiprocessing import Pool
import os

positive_words = ["good", "excellent", "love", "amazing", "best"]
negative_words = ["bad", "terrible", "hate", "worst"]

# Sentiment function
def analyze_review(review):
    score = 0
    words = review.lower().split()

    for word in words:
        if word in positive_words:
            score += 1
        elif word in negative_words:
            score -= 1

    if score > 0:
        label = "Positive"
    elif score < 0:
        label = "Negative"
    else:
        label = "Neutral"

    return (review.strip(), score, label)


# Process one file
def process_file(filename):
    results = []
    with open(filename, "r") as file:
        for line in file:
            results.append(analyze_review(line))
    return results


if __name__ == "__main__":

    # List of files
    files = ["text1.txt", "text2.txt", "text3.txt", "text4.txt"]

    # Multiprocessing
    with Pool(processes=4) as pool:
        all_results = pool.map(process_file, files)

    # Flatten results
    final_results = [item for sublist in all_results for item in sublist]

    # Store in database
    connection = sqlite3.connect("students.db")
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        review_text TEXT,
        sentiment_score INTEGER,
        sentiment_label TEXT
    )
    """)

    cursor.executemany(
        "INSERT INTO reviews (review_text, sentiment_score, sentiment_label) VALUES (?, ?, ?)",
        final_results
    )

    connection.commit()
    connection.close()

    print("Multiprocessing Completed & Data Stored!")