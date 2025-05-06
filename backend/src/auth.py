# from users import User
from werkzeug.security import generate_password_hash

def register_user(username: str, password: str, email: str, db):
    """
    Registers a new user.

    Args:
        username (str): The username of the new user.
        password (str): The password of the new user.
        email (str): The email of the new user.
        db: The SQLite database connection object.

    Returns:
        dict: A dictionary containing the result of the registration.
    """
    cursor = db.cursor()

    # Check if the username or email already exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        return {"success": False, "message": "Username already exists."}

    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    if cursor.fetchone():
        return {"success": False, "message": "Email already exists."}

    # Hash the password
    hashed_password = generate_password_hash(password)

    # Insert the new user into the database
    try:
        cursor.execute(
            "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
            (username, hashed_password, email),
        )
        db.commit()
        return {"success": True, "message": "User registered successfully."}
    except Exception as e:
        db.rollback()
        return {"success": False, "message": f"An error occurred: {str(e)}"}