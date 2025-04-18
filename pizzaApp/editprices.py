
from flask import Flask, request, jsonify, render_template, flash

app = Flask(__name__)
app.secret_key = 'temporary_key_for_school_project'  # Secure session management

# ✅ Hardcoded Menu Items (Stored in Python)
MENU_ITEMS = {
    "Cheese Pizza": {"price": 10.00},
    "Pepperoni Pizza": {"price": 12.00},
    "Supreme Pizza": {"price": 14.00},
    "Veggie Pizza": {"price": 13.00},
}

@app.route('/editprices')
def edit_prices():
    """Render the menu price editing page."""
    return render_template('editPrices.html', menu=MENU_ITEMS)

@app.route('/update_prices', methods=['POST'])
def update_prices():
    """Update pizza prices without Airtable."""
    try:
        form_data = request.json  # Expect JSON input

        if not form_data:
            return jsonify({"error": "No data provided."}), 400

        for pizza_name, new_price in form_data.items():
            if pizza_name not in MENU_ITEMS:
                return jsonify({"error": f"Pizza '{pizza_name}' not found in menu."}), 404
            
            try:
                new_price = float(new_price)
                if new_price < 0:
                    raise ValueError("Price must be a non-negative number.")
            except ValueError:
                return jsonify({"error": f"Invalid price format for '{pizza_name}'."}), 400

            # ✅ Update price in Python dictionary
            MENU_ITEMS[pizza_name]["price"] = new_price

        flash("Prices updated successfully!", "success")
        return jsonify({"message": "Prices updated successfully"}), 200

    except Exception as e:
        flash(f"Error updating prices: {str(e)}", "error")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
