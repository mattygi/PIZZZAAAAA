
import json
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session

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

def save_orders(orders):
    """Save orders to JSON file."""
    with open(ORDERS_FILE, "w") as f:
        json.dump(orders, f, indent=4)

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    """Handle payment selection while allowing progression regardless of input."""
    if request.method == 'POST':
        payment_method = request.form.get('method', 'Not Provided')  # ✅ Allow missing input

        user = session.get('username', 'Guest')  
        orders = load_orders()

        # ✅ Ensure all pending orders for the user are marked as complete
        for order in orders:
            if order["user"] == user and order["status"] == "Pending":
                order["payment_method"] = payment_method  
                order["status"] = "Complete"

        save_orders(orders)  # ✅ Persist changes
        flash("Payment step completed. Proceeding to order confirmation.", "success")

        return redirect(url_for('order_placed'))

    return render_template('payment.html')

@app.route('/order_placed', methods=['GET'])
def order_placed():
    """Retrieve completed orders for the logged-in user."""
    user = session.get('username', 'Guest')
    orders = load_orders()
    user_orders = [order for order in orders if order["user"] == user and order["status"] == "Complete"]

    if not user_orders:
        flash("No completed orders found.", "info")
        return redirect(url_for('index'))  # Redirect if no completed orders

    return render_template('orderPlaced.html', orders=user_orders)

if __name__ == '__main__':
    app.run(debug=True)
