import streamlit as st
import pandas as pd
import sqlite3
import time
from multiprocessing import Pool

# ----------------------------
# Sentiment Logic
# ----------------------------

positive_words = ["good", "excellent", "love", "amazing", "best"]
negative_words = ["bad", "terrible", "hate", "worst"]

def analyze_sentiment(text):
    score = 0
    words = text.lower().split()

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

    return score, label


# ----------------------------
# Parallel Version
# ----------------------------

def parallel_process(reviews):
    with Pool() as pool:
        return pool.map(analyze_sentiment, reviews)


# ----------------------------
# UI
# ----------------------------

st.title("🚀 Internship Project - Unified Dashboard")

option = st.sidebar.radio(
    "Select Operation",
    [
        "Single Review",
        "Upload CSV",
        "Upload Text Files",
        "Performance Comparison"
    ]
)

# ==================================================
# 1️⃣ Single Review
# ==================================================

if option == "Single Review":
    st.header("Analyze Single Review")

    review = st.text_area("Enter Review")

    if st.button("Analyze"):
        score, label = analyze_sentiment(review)
        st.success(f"Sentiment: {label}")
        st.write("Score:", score)


# ==================================================
# 2️⃣ Upload CSV
# ==================================================

elif option == "Upload CSV":
    st.header("Upload CSV File")

    file = st.file_uploader("Upload CSV", type=["csv"])

    if file:
        df = pd.read_csv(file)

        if "review" not in df.columns:
            st.error("CSV must contain 'review' column")
        else:
            st.success("File uploaded successfully")

            results = df["review"].apply(analyze_sentiment)
            df["score"] = results.apply(lambda x: x[0])
            df["label"] = results.apply(lambda x: x[1])

            st.dataframe(df.head(10))


# ==================================================
# 3️⃣ Upload TXT Files
# ==================================================

elif option == "Upload Text Files":
    st.header("Upload Multiple Text Files")

    files = st.file_uploader(
        "Upload text files",
        type=["txt"],
        accept_multiple_files=True
    )

    if files:
        reviews = []

        for file in files:
            reviews.append(file.read().decode("utf-8"))

        results = parallel_process(reviews)

        for i, res in enumerate(results):
            st.write(f"File {i+1} → {res[1]} (Score: {res[0]})")


# ==================================================
# 4️⃣ Performance Comparison
# ==================================================

elif option == "Performance Comparison":
    st.header("Sequential vs Parallel Performance")

    sample_reviews = ["good product"] * 50000

    # Sequential
    start = time.time()
    seq_results = [analyze_sentiment(r) for r in sample_reviews]
    seq_time = time.time() - start

    # Parallel
    start = time.time()
    par_results = parallel_process(sample_reviews)
    par_time = time.time() - start

    st.write("Sequential Time:", round(seq_time, 4))
    st.write("Parallel Time:", round(par_time, 4))

    if par_time < seq_time:
        st.success("Parallel Processing is Faster 🚀")
    else:
        st.warning("Parallel Processing slower (small dataset)")