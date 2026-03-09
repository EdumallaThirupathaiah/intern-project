
import streamlit as st
import pandas as pd
import sqlite3
import time
import matplotlib.pyplot as plt
import smtplib
from email.message import EmailMessage
from collections import Counter

# =============================
# CONFIG
# =============================

DB_FILE = "sentiment_data.db"
CHUNK_SIZE = 50000

SENDER_EMAIL = "239y1a0553@ksrmce.ac.in"
EMAIL_PASSWORD = "YOUR_EMAIL_PASSWORD"


# =============================
# SENTIMENT RULES
# =============================

positive_words = {"good","excellent","love","amazing","best","great","awesome","nice","perfect","fast"}
negative_words = {"bad","terrible","hate","worst","poor","slow","awful","disappointed"}

def analyze_sentiment(text):

    score = 0
    words = str(text).lower().split()

    for word in words:

        if word in positive_words:
            score += 1

        elif word in negative_words:
            score -= 1

    if score > 0:
        return score,"Positive"

    elif score < 0:
        return score,"Negative"

    else:
        return score,"Neutral"


# =============================
# EMAIL FUNCTION
# =============================

def send_email(file_path):

    try:

        msg = EmailMessage()

        msg["Subject"] = "Sentiment Analysis Report"
        msg["From"] = SENDER_EMAIL
        msg["To"] = "239y1a0553@ksrmce.ac.in"

        msg.set_content(
            "Hello,\n\nAttached is the Sentiment Analysis Report.\n\nGenerated from Streamlit Dashboard."
        )

        with open(file_path,"rb") as f:

            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="csv",
                filename="sentiment_report.csv"
            )

        server = smtplib.SMTP("smtp.office365.com",587)

        server.starttls()

        server.login(SENDER_EMAIL,EMAIL_PASSWORD)

        server.send_message(msg)

        server.quit()

        return True

    except Exception as e:

        print("Email Error:",e)

        return False


# =============================
# DATABASE
# =============================

def get_conn():

    conn = sqlite3.connect(DB_FILE)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS reviews(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        review_text TEXT,
        score INTEGER,
        label TEXT
    )
    """)

    return conn


def batch_insert(conn,rows):

    conn.executemany(
        "INSERT INTO reviews (review_text,score,label) VALUES (?,?,?)",
        rows
    )


# =============================
# UI
# =============================

st.set_page_config(layout="wide")

st.title(" Sentiment Analysis Dashboard")

option = st.sidebar.radio(
    "Select Operation",
    [
        "Single Review",
        "Upload CSV",
        "Upload Text Files",
        "Database Manager"
    ]
)


# =============================
# SINGLE REVIEW
# =============================

if option == "Single Review":

    st.header("Analyze Single Review")

    review = st.text_area("Enter Review")

    if st.button("Analyze"):

        if review.strip()=="":
            st.warning("Please enter review")

        else:

            score,label = analyze_sentiment(review)

            st.success(f"Sentiment: {label}")

            st.write("Score:",score)


# =============================
# CSV ANALYSIS
# =============================

elif option == "Upload CSV":

    st.header("Upload CSV Dataset")

    file = st.file_uploader("Upload CSV File",type=["csv"])

    if file:

        preview = pd.read_csv(file,nrows=5)

        st.subheader("Preview Data")

        st.dataframe(preview)

        text_column = st.selectbox("Select Review Column",preview.columns)

        if st.button("Analyze Dataset"):

            start_time = time.time()

            sentiment_counts = Counter()

            total_rows = 0

            conn = get_conn()

            conn.execute("BEGIN TRANSACTION")

            output_file = "processed_sentiment.csv"

            first_write = True

            file.seek(0)

            for chunk in pd.read_csv(file,chunksize=CHUNK_SIZE):

                chunk[text_column] = chunk[text_column].astype(str)

                scores=[]
                labels=[]
                rows=[]

                for review in chunk[text_column]:

                    score,label = analyze_sentiment(review)

                    scores.append(score)

                    labels.append(label)

                    sentiment_counts[label]+=1

                    rows.append((review,score,label))

                chunk["score"]=scores
                chunk["label"]=labels

                batch_insert(conn,rows)

                if first_write:

                    chunk.to_csv(output_file,index=False)

                    first_write=False

                else:

                    chunk.to_csv(output_file,index=False,mode="a",header=False)

                total_rows += len(chunk)

                st.write("Processed rows:",total_rows)

            conn.commit()

            conn.close()

            end_time = time.time()

            st.success(f"Processing Complete! Rows Processed: {total_rows}")

            st.write("Time Taken:",round(end_time-start_time,2),"seconds")

            summary = pd.Series(sentiment_counts)

            st.subheader("Sentiment Summary")

            st.write(summary)

            st.subheader("Bar Chart")

            st.bar_chart(summary)

            st.subheader("Pie Chart")

            fig,ax = plt.subplots()

            summary.plot.pie(autopct="%1.1f%%",ax=ax)

            ax.set_ylabel("")

            st.pyplot(fig)

            with open(output_file,"rb") as f:

                st.download_button(
                    "Download Processed Dataset",
                    f,
                    file_name="sentiment_results.csv"
                )

            if st.button("Send Email Report"):

                success = send_email(output_file)

                if success:
                    st.success("Report sent to 239y1a0553@ksrmce.ac.in")

                else:
                    st.error("Email sending failed")


# =============================
# TXT FILES
# =============================

elif option == "Upload Text Files":

    st.header("Upload TXT Files")

    files = st.file_uploader(
        "Upload text files",
        type=["txt"],
        accept_multiple_files=True
    )

    if files:

        conn = get_conn()

        cursor = conn.cursor()

        results=[]

        for file in files:

            text=file.read().decode("utf-8")

            score,label = analyze_sentiment(text)

            results.append((file.name,label,score))

            cursor.execute(
                "INSERT INTO reviews(review_text,score,label) VALUES (?,?,?)",
                (text,score,label)
            )

        conn.commit()

        conn.close()

        df = pd.DataFrame(results,columns=["File","Label","Score"])

        st.dataframe(df)


# =============================
# DATABASE MANAGER
# =============================

elif option == "Database Manager":

    st.header("Database Manager")

    conn = get_conn()

    cursor = conn.cursor()

    db_option = st.selectbox(
        "Select Operation",
        [
            "View Data",
            "Insert Data",
            "Delete Data",
            "Show Record Count"
        ]
    )

    if db_option == "View Data":

        cursor.execute("SELECT * FROM reviews LIMIT 1000")

        data = cursor.fetchall()

        if data:

            df = pd.DataFrame(data,columns=["ID","Review","Score","Label"])

            st.dataframe(df)

        else:

            st.warning("Database empty")

    elif db_option == "Insert Data":

        review = st.text_area("Enter Review")

        if st.button("Insert"):

            score,label = analyze_sentiment(review)

            cursor.execute(
                "INSERT INTO reviews(review_text,score,label) VALUES (?,?,?)",
                (review,score,label)
            )

            conn.commit()

            st.success("Inserted successfully")

    elif db_option == "Delete Data":

        record_id = st.number_input("Enter Record ID",step=1)

        if st.button("Delete"):

            cursor.execute(
                "DELETE FROM reviews WHERE id=?",
                (record_id,)
            )

            conn.commit()

            st.success("Record deleted")

    elif db_option == "Show Record Count":

        cursor.execute("SELECT COUNT(*) FROM reviews")

        count = cursor.fetchone()[0]

        st.info(f"Total Records: {count}")

    conn.close()

    