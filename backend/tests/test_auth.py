import pytest
import sqlite3
from werkzeug.security import check_password_hash
from polly.backend.src.auth import register_user

@pytest.fixture
def db_connection():
    # Create an in-memory SQLite database for testing
    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    """)
    connection.commit()
    yield connection
    connection.close()

def test_register_user_success(db_connection):
    result = register_user("testuser", "password123", "testuser@example.com", db_connection)
    assert result["success"] is True
    assert result["message"] == "User registered successfully."

    # Verify the user is in the database
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", ("testuser",))
    user = cursor.fetchone()
    assert user is not None
    assert user[1] == "testuser"
    assert check_password_hash(user[2], "password123")
    assert user[3] == "testuser@example.com"

def test_register_user_duplicate_username(db_connection):
    # Insert a user with the same username
    register_user("testuser", "password123", "testuser@example.com", db_connection)

    # Attempt to register another user with the same username
    result = register_user("testuser", "newpassword", "newemail@example.com", db_connection)
    assert result["success"] is False
    assert result["message"] == "Username already exists."

def test_register_user_duplicate_email(db_connection):
    # Insert a user with the same email
    register_user("testuser", "password123", "testuser@example.com", db_connection)

    # Attempt to register another user with the same email
    result = register_user("newuser", "newpassword", "testuser@example.com", db_connection)
    assert result["success"] is False
    assert result["message"] == "Email already exists."

def test_register_user_invalid_db(db_connection):
    # Close the database connection to simulate an invalid DB
    db_connection.close()

    result = register_user("testuser", "password123", "testuser@example.com", db_connection)
    assert result["success"] is False
    assert "An error occurred" in result["message"]