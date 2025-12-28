import mysql.connector
import pandas as pd
import random
from datetime import timedelta

# ---------------- DATABASE CONFIG ----------------
DB_CONFIG = {
    "host": "localhost",
    "user": "streamlit_user",
    "password": "Dharani@12345",
    "database": "Client_Query_System"
}

# ---------------- DB CONNECTION ----------------
def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

# ---------------- RANDOM TIME HELPER ----------------
def add_random_time(date_val, start_hour=9, end_hour=18):
    """
    Adds a random time between start_hour and end_hour to a date.
    """
    if pd.isna(date_val):
        return None

    random_seconds = random.randint(0, (end_hour - start_hour) * 3600)
    return date_val.replace(hour=start_hour, minute=0, second=0) + timedelta(seconds=random_seconds)

# ---------------- CSV → MYSQL INITIALIZATION ----------------
def initialize_db_from_csv(csv_file):
    """
    Load CSV data into MySQL only if queries table is empty.
    Handles date-only CSV values by assigning random times.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS cnt FROM queries")
    if cursor.fetchone()["cnt"] == 0:
        df = pd.read_csv(csv_file)

        # Convert date columns from CSV
        df["query_created_time"] = pd.to_datetime(
            df["query_created_time"], dayfirst=True, errors="coerce"
        )

        df["query_closed_time"] = pd.to_datetime(
            df["query_closed_time"], dayfirst=True, errors="coerce"
        )

        # Assign random times
        df["query_created_time"] = df["query_created_time"].apply(add_random_time)
        df["query_closed_time"] = df["query_closed_time"].apply(
            lambda x: add_random_time(x, 10, 20) if pd.notna(x) else None
        )

        # Insert into MySQL
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO queries
                (mail_id, mobile_number, category, query_heading,
                 query_description, status,
                 query_created_time, query_closed_time)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                row["mail_id"],
                row["mobile_number"],
                row["category"],
                row["query_heading"],
                row["query_description"],
                row["status"],
                row["query_created_time"].to_pydatetime() if pd.notna(row["query_created_time"]) else None,
                row["query_closed_time"].to_pydatetime() if pd.notna(row["query_closed_time"]) else None
            ))

        conn.commit()

    cursor.close()
    conn.close()

