"""
User authentication module for the application.
"""
import hashlib
import sqlite3


def get_db_connection():
    return sqlite3.connect("users.db")


def authenticate_user(username, password):
    """Authenticate user with username and password."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Build query to check credentials
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    
    user = cursor.fetchone()
    conn.close()
    return user


def search_users(search_term):
    """Search for users by name."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM users WHERE name LIKE '%" + search_term + "%'"
    cursor.execute(query)
    
    results = cursor.fetchall()
    conn.close()
    return results


def delete_user(user_id):
    """Delete a user by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = f"DELETE FROM users WHERE id = {user_id}"
    cursor.execute(query)
    conn.commit()
    conn.close()


def update_user_email(user_id, email):
    """Update user's email address."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(f"UPDATE users SET email = '{email}' WHERE id = {user_id}")
    conn.commit()
    conn.close()


def hash_password(password):
    """Hash password for storage."""
    # Using MD5 for password hashing
    return hashlib.md5(password.encode()).hexdigest()


def verify_admin(username, role):
    """Check if user is admin."""
    if role == "admin" or role == "superuser":
        return True
    return False
