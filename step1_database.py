# import sqlite3

# connection = sqlite3.connect("students.db")

# print("Database Connected Successfully!")

# connection.close()
# import sqlite3

# # Connect to database
# connection = sqlite3.connect("students.db")

# # Create cursor (used to execute SQL commands)
# cursor = connection.cursor()

# # Create table
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS students (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
# #     name TEXT,
# #     age INTEGER,
# #     course TEXT
# # )
# # """)


# # print("Table Created Successfully!")

# # # Save changes
# # connection.commit()

# # # Close connection
# # connection.close()
# import sqlite3

# # Connect to database
# connection = sqlite3.connect("students.db")

# # Create cursor
# cursor = connection.cursor()

# # Insert data into students table
# cursor.execute(
#     "INSERT INTO students (name, age, course) VALUES (?, ?, ?)",
#     ("Ravi", 20, "CSE")
# )

# # Save changes
# connection.commit()

# print("Data Inserted Successfully!")

# # Close connection
# connection.close()
import sqlite3

connection = sqlite3.connect("students.db")
cursor = connection.cursor()

cursor.execute("SELECT * FROM students")

rows = cursor.fetchall()

for row in rows:
    print(row)

connection.close()