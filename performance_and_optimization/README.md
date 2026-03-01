
# Database Performance Optimization with Indexing

## 📌 Overview

This project demonstrates the impact of database indexing on query performance using SQLite with 1 million Amazon product reviews.

The goal is to compare query execution time before and after applying database indexing and analyze the performance improvement.

---

## 🎯 Objectives

- Process and insert 1 million records into SQLite database
- Apply rule-based sentiment scoring
- Measure query execution time (Before optimization)
- Apply indexing on frequently queried columns
- Measure query execution time (After optimization)
- Compare and analyze performance improvement

---

## 📂 Project Structure

Performane_and_optimization/
│
├── scoring_engine.py              # Sentiment scoring logic
├── process_and_insert.py          # Insert 1M records into database
├── query_before_optimization.py   # Run queries without indexes
├── apply_optimization.py          # Create indexes
├── query_after_optimization.py    # Run queries with indexes
├── performance_report.txt         # Performance results
├── 7817_1.csv                     # Original dataset
├── amazon_reviews.db              # Auto-created database file
└── .gitignore

---

## ⚙️ Technologies Used

- Python
- SQLite3
- CSV Processing
- Database Indexing

---

## 🚀 How to Run

### Step 1: Insert 1 Million Records

```bash
python process_and_insert.py
