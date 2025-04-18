
import json
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'temporary_key_for_school_project'  # Keep this secure in production

ORDERS_FILE = "orders.json"

# ✅ Helper Functions to Manage JSON Storage
def load_orders():
    """Load orders from JSON file, creating it if necessary."""
    if not os.path.exists(ORDERS_FILE):
        save_orders([])  # Initialize an empty orders.json if missing
    try:
        with open(ORDERS_FILE, "r") as f:
            orders = json.load(f)
            return orders
    except (json.JSONDecodeError, FileNotFoundError):
        print("⚠️ Error loading orders.json! Initializing empty list.")
        return []

def save_orders(orders):
    """Save orders to JSON file safely."""
    with open(ORDERS_FILE, "w") as f:
        json.dump(orders, f, indent=4)

@app.route('/cart', methods=['GET'])
def cart():
    """Display pending orders in the user's cart."""
    orders = load_orders()
    user_id = session.get("user_id")

    # ✅ Retrieve only the logged-in user's orders with correct capitalization
    user_orders = [order for order in orders if order.get("user_id") == user_id and order.get("status") == "Pending"]

    if not user_orders:
        flash("ℹ️ Your cart is empty!", "info")

    return render_template('cart.html', cart=user_orders)

@app.route('/checkout', methods=['POST'])
def checkout():
    """Process checkout for pending orders."""
    orders = load_orders()
    user_id = session.get("user_id")

    # Find user's pending orders
    user_orders = [order for order in orders if order.get("user_id") == user_id and order.get("status") == "Pending"]

    if not user_orders:
        flash("⚠️ No pending orders to checkout!", "error")
        return redirect(url_for('cart'))  # Redirect back to cart

    # Update the status of the user's orders to "Completed"
    for order in user_orders:
        order["status"] = "Completed"

    save_orders(orders)  # Save the updated orders

    flash("🎉 Your order has been placed successfully!", "success")
    return redirect(url_for('index'))  # Redirect to a confirmation page

def order_placed():
    return render_template('order_placed.html')

if __name__ == '__main__':
    app.run(debug=True)