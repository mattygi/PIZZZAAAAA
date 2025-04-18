
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'temporary_key_for_school_project'  # Secure session management

# ✅ Hardcoded Menu Items (Stored in Python)
MENU_ITEMS = {
    "1": {"name": "Cheese Pizza", "price": "$10.00"},
    "2": {"name": "Pepperoni Pizza", "price": "$12.00"},
    "3": {"name": "Supreme Pizza", "price": "$14.00"},
    "4": {"name": "Veggie Pizza", "price": "$13.00"},
}

@app.route('/edit_menu_items', methods=['GET', 'POST'])
def edit_menu_items():
    try:
        if request.method == 'POST':
            action = request.form.get('action')
            item_id = request.form.get('item_id', "").strip()
            item_name = request.form.get('item', "").strip()
            price = request.form.get('price', "").strip()

            # ✅ Ensure item_id is valid and prevent passing 'None'
            if action in ['update', 'delete'] and not item_id:
                flash("Error: Missing item ID for update/delete operations.", "error")
                return redirect(url_for('edit_menu_items'))

            if action == 'add' and item_name and price:
                new_id = str(len(MENU_ITEMS) + 1)  # ✅ Generate new ID
                MENU_ITEMS[new_id] = {"name": item_name, "price": price}
                flash(f"Added new item: {item_name}", "success")

            elif action == 'update' and item_id in MENU_ITEMS:
                MENU_ITEMS[item_id]["name"] = item_name
                MENU_ITEMS[item_id]["price"] = price
                flash(f"Updated item: {item_name}", "success")

            elif action == 'delete' and item_id in MENU_ITEMS:
                del MENU_ITEMS[item_id]
                flash("Deleted item successfully!", "success")

            return redirect(url_for('edit_menu_items'))

        return render_template('editMenuItems.html', menu=MENU_ITEMS.values())

    except Exception as e:
        flash(f"Error processing menu request: {str(e)}", "error")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
