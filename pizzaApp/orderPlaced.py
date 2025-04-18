
import json
import os
from flask import Flask, render_template, session, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'temporary_key_for_school_project'  # Secure session management

ORDERS_FILE = "orders.json"  # ✅ JSON file for storing orders

# ✅ Helper Functions for JSON Storage
def load_orders():
    """Load orders from JSON file."""
    try:
        with open(ORDERS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []  # Initialize empty list if file not found

@app.route('/order_placed', methods=['GET'])
def order_placed():
    """Retrieve confirmed orders for the logged-in user."""
    try:
        user = session.get('username', 'Guest')  # Retrieve logged-in username
        orders = load_orders()  # Load orders from JSON
        user_orders = [order for order in orders if order["user"] == user and order["status"] == "Complete"]

        if not user_orders:
            flash("No completed orders found.", "info")
            return redirect(url_for('index'))  # Redirect user if no orders exist

        return render_template('orderPlaced.html', orders=user_orders)  # Show confirmed orders

    except Exception as e:
        flash(f"Error retrieving order details: {str(e)}", "error")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
