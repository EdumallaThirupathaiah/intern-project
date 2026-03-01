import sqlite3
import csv
import datetime
import os

# ----------------------------
# Rule-based Keywords
# ----------------------------
positive_words = ["good", "excellent", "love", "amazing", "best"]
negative_words = ["bad", "terrible", "hate", "worst"]


# ----------------------------
# Sentiment Analysis Function
# ----------------------------
def analyze_sentiment(text):
    score = 0
    words = text.lower().split()

    for word in words:
        if word in positive_words:
            score += 1
        elif word in negative_words:
            score -= 1

    if score > 0:
        sentiment = "Positive"
    elif score < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return score, sentiment


# ----------------------------
# Main Processing
# ----------------------------
def main():
    try:
        # Get path of current script
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Dataset path (same folder as script)
        dataset_path = os.path.join(base_dir, "dataset.csv")

        # Check if file exists
        if not os.path.exists(dataset_path):
            raise FileNotFoundError("dataset.csv file not found.")

        # Connect to SQLite database (creates if not exists)
        db_path = os.path.join(base_dir, "sentiment_reviews.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Create table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            review_text TEXT,
            sentiment_score INTEGER,
            sentiment_label TEXT,
            timestamp TEXT
        )
        """)

        # Read dataset
        with open(dataset_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            if "review" not in reader.fieldnames:
                raise KeyError("'review' column not found in dataset.")

            for row in reader:
                review = row["review"]

                score, sentiment = analyze_sentiment(review)

                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                cursor.execute("""
                INSERT INTO reviews 
                (review_text, sentiment_score, sentiment_label, timestamp)
                VALUES (?, ?, ?, ?)
                """, (review, score, sentiment, timestamp))

        conn.commit()
        conn.close()

        print("All reviews processed and stored successfully!")

    except FileNotFoundError as e:
        print("File Error:", e)

    except KeyError as e:
        print("Column Error:", e)

    except sqlite3.Error as e:
        print("Database Error:", e)

    except Exception as e:
        print("Unexpected Error:", e)


# ----------------------------
# Run Program
# ----------------------------
if __name__ == "__main__":
    main()