from flask import Flask, render_template, session, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'temporary_key_for_school_project'  # Secure session management

# ✅ Hardcoded Orders Storage (For Demo Purposes)
ORDERS = [
    {
        "id": 1,
        "user": "john_doe",
        "method": "Pickup",
        "status": "Processing",
        "items": [
            {"quantity": 1, "size": "Large", "pizza": "Pepperoni Pizza", "price": 12.00},
            {"quantity": 1, "size": "Large", "pizza": "Cheese Pizza", "price": 10.00}
        ],
        "total": 22.00
    },
    {
        "id": 2,
        "user": "john_doe",
        "method": "Delivery",
        "status": "Processing",
        "items": [
            {"quantity": 1, "size": "Large", "pizza": "Pepperoni Pizza", "price": 12.00},
            {"quantity": 1, "size": "Large", "pizza": "Cheese Pizza", "price": 10.00}
        ],
        "total": 22.00
    }
]

@app.route('/review_order', methods=['GET'])
def review_order():
    """Retrieve processing order details from hardcoded storage."""
    try:
        user = session.get('username', 'Guest')
        user_orders = [order for order in ORDERS if order["user"] == user and order["status"] == "Processing"]

        if not user_orders:
            flash("No orders found, but continuing for demo purposes.", "info")
            return redirect(url_for('index'))  # Redirect if no orders exist

        return render_template('reviewOrder.html', orders=user_orders)  # ✅ Displays multiple matching orders

    except Exception as e:
        flash(f"Error retrieving order details: {str(e)}", "error")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
