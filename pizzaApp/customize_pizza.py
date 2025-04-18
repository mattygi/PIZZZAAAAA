
import json
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'temporary_key_for_school_project'  # Keep this secure

ORDERS_FILE = "orders.json"

# ✅ Hardcoded Menu Items
MENU_ITEMS = {
    "Cheese Pizza": {"price": 10.00, "size": "Medium"},
    "Pepperoni Pizza": {"price": 12.00, "size": "Medium"},
    "Supreme Pizza": {"price": 14.00, "size": "Large"},
    "Veggie Pizza": {"price": 13.00, "size": "Medium"},
}

# ✅ Helper Functions to Manage JSON Storage
def load_orders():
    """Load orders from JSON file, creating it if necessary."""
    global ORDERS_FILE
    if not os.path.exists(ORDERS_FILE):
        try:
            with open(ORDERS_FILE, "w") as f:
                json.dump([], f)  # Create an empty JSON file
            print(f"✅ Created orders file: {ORDERS_FILE}")
        except Exception as e:
            print(f"❌ Error creating orders file: {e}")
            return []
    try:
        with open(ORDERS_FILE, "r") as f:
            orders = json.load(f)
        print(f"✅ Loaded orders from {ORDERS_FILE}: {orders}")
        return orders
    except json.JSONDecodeError:
        print(f"⚠️  JSONDecodeError: {ORDERS_FILE} was empty or corrupted. Returning an empty list.")
        return []
    except FileNotFoundError:
        print(f"⚠️  FileNotFoundError: {ORDERS_FILE} not found.  Returning an empty list.")
        return []
    except Exception as e:
        print(f"❌ An unexpected error occurred while loading orders: {e}")
        return []

def save_orders(orders):
    """Save orders to JSON file safely."""
    global ORDERS_FILE
    try:
        with open(ORDERS_FILE, "w") as f:
            json.dump(orders, f, indent=4)
        print(f"✅ Saved orders to {ORDERS_FILE}: {orders}")
    except Exception as e:
        print(f"❌ An error occurred while saving orders to {ORDERS_FILE}: {e}")
        flash("⚠️ An error occurred while saving your order. Please try again.", "error")

@app.route('/')
def index():
    """Serve the pizza customization page."""
    if "user_id" not in session:
        session["user_id"] = os.urandom(8).hex()
    if "username" not in session:
        session["username"] = "Guest"
    return render_template('customize_pizza.html', menu=MENU_ITEMS, user_id=session["user_id"], username=session["username"])

@app.route('/customize_pizza', methods=['POST'])
def customize_pizza():
    """Handle pizza customization and store selections in JSON file."""
    global ORDERS_FILE
    print("🍕 customize_pizza route called")  # Debugging

    # Debugging: Log raw form data
    print("Form data received:", request.form)

    pizza_type = request.form.get("pizza")
    size = request.form.get("size")
    quantity = request.form.get("quantity", 1)
    meats = request.form.getlist("meats[]")
    veggies = request.form.getlist("veggies[]")

    # Validate pizza type and size
    if not pizza_type or pizza_type not in MENU_ITEMS:
        flash("⚠️ Invalid pizza type selected!", "error")
        return redirect(url_for('index'))
    if not size:
        flash("⚠️ Please select a size for your pizza.", "error")
        return redirect(url_for('index'))

    # Ensure quantity is an integer
    try:
        quantity = int(quantity)
        if quantity < 1:
            flash("⚠️ Invalid quantity. Please enter a positive number.", "error")
            return redirect(url_for('index'))
    except ValueError:
        flash("⚠️ Invalid quantity! Defaulting to 1.", "error")
        quantity = 1

    # Calculate total price
    price_per_pizza = MENU_ITEMS[pizza_type]["price"]
    total_price = price_per_pizza * quantity

    # Get user information
    user_id = session.get("user_id", "guest_user")
    username = session.get("username", "Guest")

    # Construct order data
    order_data = {
        "order_id": len(load_orders()) + 1,
        "user_id": user_id,
        "username": username,
        "items": [
            {
                "Item": pizza_type,
                "Size": size,
                "Meats": ", ".join(meats) or "No meats",
                "Veggies": ", ".join(veggies) or "No veggies",
                "Quantity": quantity,
                "Price": total_price,
            }
        ],
        "status": "Pending",
    }

    # Debugging: Log constructed order data
    print("Constructed order data:", order_data)

    # Save order data
    orders = load_orders()  # Load the current orders
    orders.append(order_data)  # Append the new order
    save_orders(orders)  # Save the updated orders

    flash(f"✅ {quantity} {size} {pizza_type} Pizza(s) added to your cart!", "success")
    return redirect(url_for('cart'))
