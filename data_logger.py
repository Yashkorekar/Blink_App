import sqlite3
from datetime import datetime

class DataLogger:
    def __init__(self, db_name="face_data.db"):
        self.db_name = db_name
        self._create_table()

    def _create_table(self):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                blink_count INTEGER
            )
        ''')
        connection.commit()
        connection.close()

    def log_data(self, blink_count):
        try:
            connection = sqlite3.connect(self.db_name)  # New connection in the current thread
            cursor = connection.cursor()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute('INSERT INTO metrics (timestamp, blink_count) VALUES (?, ?)',
                           (timestamp, blink_count))
            connection.commit()
        finally:
            connection.close()
