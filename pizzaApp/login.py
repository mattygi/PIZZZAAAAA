
import json
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'temporary_key_for_school_project'  # Secure session management

USERS_FILE = "users.json"  # ✅ JSON file for storing user data

# ✅ Helper Functions for JSON Storage
def load_users():
    """Load user data from JSON file."""
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"admin": {"password": generate_password_hash("admin123"), "role": "admin"}}  # Default admin

def save_users(users):
    """Save user data to JSON file."""
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login using JSON storage."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # ✅ Validate input fields
        if not username or not password:
            flash("Username and password are required.", "error")
            return redirect(url_for('login'))

        # ✅ Load users from JSON
        users = load_users()

        # ✅ Authenticate user
        user = users.get(username)
        if user and check_password_hash(user["password"], password):
            session['username'] = username
            session['role'] = user["role"]
            flash(f"Login successful! Welcome, {username}.", "success")
            return redirect(url_for('customize_pizza'))

        flash("Invalid username or password.", "error")
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration with JSON storage."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # ✅ Load existing users
        users = load_users()

        # ✅ Ensure username is unique
        if username in users:
            flash("Username already exists!", "error")
            return redirect(url_for('register'))

        # ✅ Hash password before storing
        users[username] = {"password": generate_password_hash(password), "role": "customer"}
        save_users(users)  # ✅ Store updated user list

        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/customize_pizza')
def customize_pizza():
    if 'username' in session:
        return render_template('customize_pizza.html', username=session['username'])
    flash("Please log in first.", "error")
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    """Log out user and clear session."""
    session.pop('username', None)
    session.pop('role', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
