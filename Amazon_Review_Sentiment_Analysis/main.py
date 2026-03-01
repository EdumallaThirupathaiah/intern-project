import sqlite3
import csv
import datetime
import os
from sentiment_analyzer import analyze_sentiment


def main():
    try:
        # Get current folder path
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Correct dataset file name
        dataset_path = os.path.join(base_dir, "amazon_reviews.csv")

        # Database file
        db_path = os.path.join(base_dir, "amazon_reviews.db")

        # Check if dataset exists
        if not os.path.exists(dataset_path):
            raise FileNotFoundError("amazon_reviews.csv not found.")

        # Connect to SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Create table if not exists
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            review_text TEXT,
            sentiment_score INTEGER,
            sentiment_label TEXT,
            timestamp TEXT
        )
        """)

        # Open CSV file
        with open(dataset_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            # Check if column name is correct
            if "review" not in reader.fieldnames:
                raise KeyError("'review' column missing in CSV file.")

            for row in reader:
                review = row["review"]

                # Analyze sentiment
                score, sentiment = analyze_sentiment(review)

                # Get current timestamp
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Insert into database
                cursor.execute("""
                INSERT INTO reviews 
                (review_text, sentiment_score, sentiment_label, timestamp)
                VALUES (?, ?, ?, ?)
                """, (review, score, sentiment, timestamp))

        # Save changes
        conn.commit()
        conn.close()

        print("Amazon reviews processed successfully!")

    except FileNotFoundError as e:
        print("File Error:", e)

    except KeyError as e:
        print("Column Error:", e)

    except sqlite3.Error as e:
        print("Database Error:", e)

    except Exception as e:
        print("Unexpected Error:", e)


if __name__ == "__main__":
    main()