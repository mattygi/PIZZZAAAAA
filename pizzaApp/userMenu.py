
from flask import Flask, render_template, session, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'temporary_key_for_school_project'  # Secure session management

# ✅ Hardcoded Orders Storage (For Demo Purposes)
ORDERS = [
    {
        "id": 1,
        "user": "john_doe",
        "items": [
            {"pizza": "Pepperoni Pizza", "quantity": 1, "size": "Large", "price": 12.00},
            {"pizza": "Cheese Pizza", "quantity": 1, "size": "Large", "price": 10.00}
        ],
        "status": "Pending"
    },
    {
        "id": 2,
        "user": "john_doe",
        "items": [
            {"pizza": "Pepperoni Pizza", "quantity": 1, "size": "Large", "price": 12.00},
            {"pizza": "Cheese Pizza", "quantity": 1, "size": "Large", "price": 10.00}
        ],
        "status": "Processing"
    }
]

@app.route('/')
def index():
    """Render the user menu page."""
    return render_template('userMenu.html')

@app.route('/review_order', methods=['GET'])
def review_order():
    """Retrieve logged-in user's orders from hardcoded storage."""
    user = session.get('username', 'Guest')  # Get logged-in username
    user_orders = [order for order in ORDERS if order["user"] == user]

    if not user_orders:
        flash("No orders found, but continuing for demo purposes.", "info")
        return redirect(url_for('index'))  # Redirect if no orders exist

    return render_template('reviewOrder.html', orders=user_orders)  # ✅ Displays multiple matching orders

@app.route('/customize_pizza', methods=['GET'])
def customize_pizza():
    """Render the pizza customization page."""
    return render_template('customize_pizza.html')

@app.route('/logout')
def logout():
    """Clear the user session and redirect to the homepage."""
    session.pop('username', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
