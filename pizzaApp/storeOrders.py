import os
from flask import Flask, render_template, request, session, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'temporary_key_for_school_project'  # Secure session management
app.permanent_session_lifetime = 3600  # Session expires after 1 hour

# ✅ Hardcoded Admin Credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# ✅ Hardcoded Orders Storage (For Demo Purposes)
ORDERS = [
    {
        "id": 1,
        "customer": "john_doe",
        "items": [
            {"pizza": "Pepperoni Pizza", "quantity": 1, "price": 12.00},
            {"pizza": "Cheese Pizza", "quantity": 1, "price": 10.00}
        ],
        "status": "Pending",
        "total": 22.00
    },
    {
        "id": 2,
        "customer": "john_doe",
        "items": [
            {"pizza": "Pepperoni Pizza", "quantity": 1, "price": 12.00},
            {"pizza": "Cheese Pizza", "quantity": 1, "price": 10.00}
        ],
        "status": "Processing",
        "total": 22.00
    }
]

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    """Handle admin login with hardcoded credentials."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # ✅ Hardcoded admin authentication
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True  # ✅ Set session flag for admin
            session.permanent = True  # ✅ Keep session active
            flash("Admin login successful!", "success")
            return redirect(url_for('admin_menu'))  # ✅ Redirect to admin dashboard

        flash("Invalid credentials. Please try again.", "error")
        return redirect(url_for('admin_login'))

    return render_template('adminLogin.html')  # ✅ Corrected reference

@app.route('/admin_menu')
def admin_menu():
    """Render the admin menu page."""
    if not session.get('admin_logged_in'):
        flash("Please log in as an admin.", "error")
        return redirect(url_for('admin_login'))  # ✅ Fixed typo

    return render_template('adminMenu.html')

@app.route('/admin_orders')
def admin_orders():
    """Retrieve and display all orders for admin."""
    if not session.get('admin_logged_in'):
        flash("Unauthorized access.", "error")
        return redirect(url_for('admin_login'))

    if not ORDERS:
        flash("No orders found.", "info")
        return redirect(url_for('admin_menu'))  # ✅ Redirect to admin dashboard

    return render_template('storeOrders.html', orders=ORDERS)

@app.route('/admin_logout')
def admin_logout():
    """Log out admin and clear session."""
    session.pop('admin_logged_in', None)
    flash("Admin has been logged out.", "info")
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(debug=True)
