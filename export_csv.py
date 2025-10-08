import sqlite3
import csv

conn = sqlite3.connect('customer_responses.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM responses")
rows = cursor.fetchall()

with open('customer_responses.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['ID', 'Mobile Number', 'Message', 'Timestamp'])
    writer.writerows(rows)

conn.close()
print("Exported to customer_responses.csv successfully.")
