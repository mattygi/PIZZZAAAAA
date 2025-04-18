import json
from flask import Flask, render_template, request, redirect, url_for, session, flash
import os

app = Flask(__name__)
app.secret_key = 'temporary_key_for_school_project'  # Keep this secure in production

# ✅ Hardcoded Admin Credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# ✅ Hardcoded Menu Items (No Database Needed)
MENU_ITEMS = {
    "Cheese Pizza": "$10.00",
    "Pepperoni Pizza": "$12.00",
    "Supreme Pizza": "$14.00",
    "Veggie Pizza": "$13.00"
}

# ✅ JSON Files for Persistent User & Order Storage
USERS_FILE = "users.json"
ORDERS_FILE = "orders.json"

# ✅ Helper Functions for JSON Storage
def load_json(file):
    """Load data from JSON file."""
    try:
        with open(file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []  # Initialize empty list if file not found
    except json.JSONDecodeError:
        return [] # Handle empty or corrupted JSON file

def save_json(file, data):
    """Save data to JSON file."""
    try:
        with open(file, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving to {file}: {e}")
        flash("Failed to save data. Please try again.", "error") # inform the user

@app.route('/review_order')
def review_order():
    return render_template('reviewOrder.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    return render_template('adminLogin.html')

@app.route('/edit_menu_items', methods=['GET', 'POST'])
def edit_menu_items():
    return render_template('editMenuItems.html')

@app.route('/customize_pizza', methods=['GET', 'POST'])
def customize_pizza():
    if request.method == 'POST':
        # ✅ Retrieve pizza details from form submission
        pizza = request.form.get('pizza')
        size = request.form.get('size')
        quantity = request.form.get('quantity')
        username = session.get('username') # Get username.

        # ✅ Create order data
        order_data = {
            "order_id": len(load_json(ORDERS_FILE)) + 1,
            "user_id": session.get("user_id", "guest_user"),  # Use user_id if available
            "username": username,
            "items": [
                {
                    "Item": pizza,
                    "Size": size,
                    "Quantity": int(quantity),
                    "Price": float(MENU_ITEMS[pizza].replace("$", "")) * int(quantity) # calculate price
                }
            ],
            "status": "Pending"
        }

        orders = load_json(ORDERS_FILE)
        orders.append(order_data)
        save_json(ORDERS_FILE, orders)

        flash(f"{quantity}x {size} {pizza} added to cart!", "success")
        return redirect(url_for('cart'))  # ✅ Redirect user after adding to cart

    return render_template('customize_pizza.html', menu=MENU_ITEMS)  # ✅ Pass menu items dynamically


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["role"] = "store_owner"
            session["username"] = username
            flash("Admin login successful!", "success")
            return redirect(url_for('admin_menu'))

        users = load_json(USERS_FILE)
        user = next((u for u in users if u["username"] == username and u["password"] == password), None)

        if user:
            session["role"] = "customer"
            session["username"] = username
            session["user_id"] = user.get("user_id", os.urandom(8).hex()) # set user_id
            flash("Login successful!", "success")
            return redirect(url_for('user_menu'))

        flash("Invalid credentials. Please try again.", "error")
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        users = load_json(USERS_FILE)

        if any(u["username"] == username for u in users):
            flash("Username already exists!", "error")
            return redirect(url_for('register'))

        user_id = os.urandom(8).hex() # generate user_id
        users.append({"username": username, "password": password, "role": "customer", "user_id": user_id})
        save_json(USERS_FILE, users)
        session["user_id"] = user_id # set user_id
        session["username"] = username # set username
        flash("Registration successful!", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/cart', methods=['GET'])
def cart():
    """Show only pending orders for the logged-in user."""
    orders = load_json(ORDERS_FILE)
    username = session.get("username")
    pending_orders = [order for order in orders if order["username"] == username and order["status"] == "Pending"]
    if not pending_orders:
        flash("Your cart is empty!", "info")
    return render_template('cart.html', cart=pending_orders)

@app.route('/checkout', methods=['GET'])
def checkout():
    """Change order status from 'Pending' to 'Complete'."""
    orders = load_json(ORDERS_FILE)
    username = session.get("username")

    updated_orders = [] # create a new list
    for order in orders:
        if order["username"] == username and order["status"] == "Pending":
            order["status"] = "Complete"
            updated_orders.append(order) # add updated order
        else:
            updated_orders.append(order) # keep the other orders unchanged

    save_json(ORDERS_FILE, updated_orders) #save the updated list
    flash("Order placed successfully!", "success")
    return redirect(url_for('store_orders'))

@app.route('/store_orders', methods=['GET'])
def store_orders():
    """Show completed orders for the logged-in user."""
    orders = load_json(ORDERS_FILE)
    username = session.get("username")
    completed_orders = [order for order in orders if order["username"] == username and order["status"] == "Complete"]
    return render_template('storeOrders.html', orders=completed_orders)

@app.route('/admin_menu')
def admin_menu():
    if session.get('role') != 'store_owner':
        flash("Access denied. Store owners only.", "error")
        return redirect(url_for('login'))
    return render_template('adminMenu.html')

@app.route('/user_menu')
def user_menu():
    return render_template('userMenu.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
