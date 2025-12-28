import bcrypt
from db_config import get_connection

# ---------------- Password Helpers ----------------
def hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed.decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

# ---------------- User Registration ----------------
def register_user(username, password, role):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    if cursor.fetchone():
        print(f"User '{username}' already exists, skipping...")
        cursor.close()
        conn.close()
        return

    hashed_pw = hash_password(password)
    cursor.execute(
        "INSERT INTO users (username, hashed_password, role) VALUES (%s, %s, %s)",
        (username, hashed_pw, role)
    )
    conn.commit()
    cursor.close()
    conn.close()

# ---------------- User Authentication ----------------
def authenticate_user(username, password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user and verify_password(password, user["hashed_password"]):
        return user["role"]
    return None
