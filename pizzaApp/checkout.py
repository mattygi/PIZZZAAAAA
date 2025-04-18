@app.route('/checkout', methods=['POST'])
def process_checkout():
    try:
        # Extract form data
        data = request.json  # Expecting JSON data
        pizza = data.get('pizza')
        quantity = data.get('quantity')
        size = data.get('size')
        price = data.get('price')
        delivery_method = data.get('delivery_method')  # 'in_store_pickup' or 'delivery'
        payment_method = data.get('payment_method')  # 'online' or 'in_store'
        email = data.get('email')

        # Validate required fields
        if not all([pizza, quantity, size, price, delivery_method, payment_method]):
            return jsonify({"error": "Missing order details."}), 400

        # ✅ Store order details
        order_data = {
            "id": len(ORDERS) + 1,
            "Pizza": pizza,
            "Quantity": int(quantity),
            "Size": size,
            "Price": float(price),
            "Delivery Method": delivery_method,
            "Payment Method": payment_method,
            "Status": "Complete"
        }
        ORDERS.append(order_data)
        session['order_status'] = "Complete"  # Track order completion in session

        # ✅ Generate Receipt Summary
        receipt_message = f"""
        🎉 Payment received for Order #{order_data['id']}! 🎉
        
        🍕 **Pizza:** {pizza}
        📦 **Quantity:** {quantity}
        📏 **Size:** {size}
        💰 **Total Price:** ${price}
        🚚 **Pickup Option:** {delivery_method}
        💳 **Payment Method:** {payment_method}

        Thank you for your order! Enjoy your meal! 🍽️
        """

        logging.info(f"Order processed: {order_data}")
        return jsonify({"message": receipt_message, "order": order_data}), 200

    except Exception as e:
        logging.error(f"Error processing checkout: {str(e)}")
        return jsonify({"error": str(e)}), 500
