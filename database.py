import sqlite3


def init_db():
  conn = sqlite3.connect("jobs.db")
  cursor = conn.cursor()
  # Drop old table so schema updates cleanly every time
  cursor.execute("DROP TABLE IF EXISTS jobs")
  cursor.execute("""
        CREATE TABLE jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            source TEXT,
            salary_min INTEGER DEFAULT 0,
            date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
  conn.commit()
  conn.close()


def save_jobs(jobs):
  conn = sqlite3.connect("jobs.db")
  cursor = conn.cursor()
  for job in jobs:
    cursor.execute(
        "INSERT INTO jobs (title, source, salary_min) VALUES (?, ?, ?)",
        (job["title"], job["source"], job["salary_min"]),
    )
  conn.commit()
  conn.close()


if __name__ == "__main__":
  init_db()
  print("Database initialized and refreshed with salary tracking!")