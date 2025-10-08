import sqlite3

conn = sqlite3.connect('customer_responses.db')
cursor = conn.cursor()

# Drop old table (CAUTION: This deletes all previous data)
cursor.execute("DROP TABLE IF EXISTS responses")

# Create new one
cursor.execute('''
    CREATE TABLE responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mobile_number TEXT NOT NULL,
        message TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

conn.commit()
conn.close()
print("Database reset successfully.")
