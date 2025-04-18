from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'temporary_key_for_school_project'  # Replace with a secure key in production

# ✅ Hardcoded Admin Credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# ✅ Hardcoded Menu Items
MENU_ITEMS = {
    "1": {"name": "Cheese Pizza", "price": "$10.00"},
    "2": {"name": "Pepperoni Pizza", "price": "$12.00"},
    "3": {"name": "Supreme Pizza", "price": "$14.00"},
    "4": {"name": "Veggie Pizza", "price": "$13.00"},
}

# ✅ Hardcoded Orders (Dynamically updated)
ORDERS = []

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_username = request.form.get('username')
        admin_password = request.form.get('password')

        if admin_username == ADMIN_USERNAME and admin_password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            flash("Admin login successful!", "success")
            return redirect(url_for('admin_menu'))  # Redirects to Admin Menu
        else:
            flash("Invalid credentials. Please try again.", "error")
            return redirect(url_for('admin_login'))

    return render_template('adminLogin.html')

@app.route('/admin_menu')
def admin_menu():
    if not session.get('admin_logged_in'):
        flash("Unauthorized access. Please log in.", "error")
        return redirect(url_for('admin_login'))

    return render_template('adminMenu.html', message="Welcome Admin! Manage store orders and menu items.")

@app.route('/store_orders')
def store_orders():
    if not session.get('admin_logged_in'):
        flash("Access denied. Only admins can review store orders.", "error")
        return redirect(url_for('admin_login'))

    return render_template('storeOrders.html', orders=ORDERS)  # ✅ Now pulling dynamic orders

@app.route('/edit_menu_items', methods=['GET', 'POST'])
def edit_menu_items():
    if not session.get('admin_logged_in'):
        flash("Access denied. Only admins can edit menu items.", "error")
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        item_id = request.form.get('item_id')
        item_name = request.form.get('item_name')
        price = request.form.get('price')
        action = request.form.get('action')

        if action == "add":
            new_id = str(len(MENU_ITEMS) + 1)
            MENU_ITEMS[new_id] = {"name": item_name, "price": price}
            flash(f"Menu item '{item_name}' has been added.", "success")

        elif action == "update" and item_id in MENU_ITEMS:
            MENU_ITEMS[item_id]["name"] = item_name
            MENU_ITEMS[item_id]["price"] = price
            flash(f"Menu item '{item_name}' has been updated.", "success")

        elif action == "delete" and item_id in MENU_ITEMS:
            del MENU_ITEMS[item_id]
            flash(f"Menu item '{item_name}' has been deleted.", "success")

        return redirect(url_for('edit_menu_items'))

    return render_template('editMenuItems.html', menu=MENU_ITEMS.values())

@app.route('/edit_prices', methods=['GET', 'POST'])
def edit_prices():
    if not session.get('admin_logged_in'):
        flash("Access denied. Only admins can edit prices.", "error")
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        item_id = request.form.get('item_id')
        new_price = request.form.get('new_price')

        if item_id in MENU_ITEMS:
            MENU_ITEMS[item_id]["price"] = new_price
            flash(f"Price for '{MENU_ITEMS[item_id]['name']}' updated to {new_price}.", "success")

        return redirect(url_for('edit_prices'))

    return render_template('editPrices.html', menu=MENU_ITEMS.values())

@app.route('/admin_logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
