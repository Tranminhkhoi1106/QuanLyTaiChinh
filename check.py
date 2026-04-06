import sqlite3

conn = sqlite3.connect("momo_mini.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM customers")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()