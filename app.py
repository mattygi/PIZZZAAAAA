import os
from datetime import datetime
import sqlite3
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, render_template, request, redirect, session, flash, jsonify
from flask_session import Session
from helpers import login_required, eur
from werkzeug.security import generate_password_hash, check_password_hash
from cs50 import SQL

# Configure application
app = Flask(__name__)


# Custom filter
app.jinja_env.filters["eur"] = eur


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# Configure CS50 Library to use SQLite database
dbcs = SQL("sqlite:///project.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    return render_template("index.html")


@app.route("/order", methods=["GET", "POST"])
@login_required
def order():
    """CREATE A HTML PAGE, DROPDOWN LIST, TO ADD ITEMS TO MENU"""
    # Get user's id from the session
    user_id = session["user_id"]
    if user_id is None:
        return redirect("/login")

    if request.method == "GET":
        pizza_data = dbcs.execute("SELECT id_pizza,p.pizza_name, p.ingredients, pv.normal_price, pv.maxi_price \
        FROM pizzas p \
        JOIN price_variations pv ON p.price_variation = pv.variation_name")
        return render_template("order.html", pizza_data=pizza_data)

    if request.method == "POST":
        pizza_name = request.form.get("pizza_name")
        normal_qty = int(request.form.get("normal_qty"))
        maxi_qty = int(request.form.get("maxi_qty"))

        # Retrieve price from the price_variations table using JOIN
        query = """
            SELECT p.pizza_name, pv.size, pv.price
            FROM pizzas p
            JOIN price_variations pv ON p.price_variation = pv.variation_name
            WHERE p.pizza_name = :pizza_name
        """
        pizza_price = dbcs.execute(query, pizza_name=pizza_name).fetchone()
        if not pizza_price:
            return apology("Pizza not found", 404)

        total_price = (normal_qty + maxi_qty) * pizza_price["price"]

        # Insert order details into the orders table
        dbcs.execute(
            "INSERT INTO orders (user_id, pizza_name, normal_qty, maxi_qty, total_price) VALUES (?, ?, ?, ?, ?)",
            user_id, pizza_name, normal_qty, maxi_qty, total_price
        )

        return render_template("order_success.html", total_price=total_price)


@app.route('/insert_order', methods=['POST'])
def insert_order():
    if request.method == 'POST':
        try:
            order_data = request.get_json()
            print("Received order data:", order_data)  # Add this line to print order_data

            # Extract temporaryOrders list from order_data
            temporary_orders = order_data.get('temporaryOrders', [])

            # Extract order details from JSON data
            user_id = session.get('user_id')  # Get user_id from session
            order_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Get current date and time
            # Construct the items string by iterating through each order
            items = ', '.join([f"{order['pizzaQuantity']}x {order['pizzaSize']} {order['pizzaName']}" for order in temporary_orders])
            total_amount = sum(float(order['pizzaPrice']) * int(order['pizzaQuantity']) for order in temporary_orders)

            print("user_id:", user_id)
            print("order_date:", order_date)
            print("items:", items)
            print("total_amount:", total_amount)

            # Insert order details into the order_history table
            dbcs.execute(
                "INSERT INTO order_history (user_id, order_date, items, total_amount) VALUES (?, ?, ?, ?)",
                (user_id),(order_date),(items),(total_amount)
            )

            return jsonify({'message': 'Order inserted successfully'})
        except Exception as e:

            error_message = str(e)  # Extract error message from the exception
            print("Error:", error_message)
            return jsonify({'error': error_message}), 500  # Return JSON error response with 500 status code


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username") or not request.form.get("password"):
            apology_message = "Must provide username or password."
            return render_template("login.html", apology_message=apology_message)

        # Query database for username
        rows = dbcs.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            apology_message = "Incorrect username or password."
            return render_template("login.html", apology_message=apology_message)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route('/get_user_id', methods=['GET'])
def get_user_id():
    if 'user_id' in session:
        user_id = session['user_id']
        return jsonify({'user_id': user_id})
    return jsonify({'user_id': None})


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    apology_message = "Please provide both username and password."

    if request.method == "GET":
        return render_template("register.html")

    # as by submitting a form via POST
    elif request.method == "POST":
        if not request.form.get("username") or \
        not request.form.get("password") or \
        not request.form.get("password1"):
            apology_message = "Please provide both username and password."
            return render_template("register.html", apology_message=apology_message)

    # Check if passwords are identical
    if request.form.get("password") != request.form.get("password1"):
        return render_template("register.html", apology_message="Passwords must be identical")

    # Protect users password by hashing it
    plaintext_password = request.form.get("password")
    hashed_password = generate_password_hash(plaintext_password)

    new_username = request.form.get("username")

    check_username = dbcs.execute(
    "SELECT * FROM users WHERE username = ?", new_username
    )
    if len(check_username) >= 1:
        return render_template("register.html", apology_message="Username not available")

    # Adding the user's username and password hash to the DATABASE
    dbcs.execute(
        "INSERT INTO users (username, hash) VALUES (?, ?)",
        new_username, hashed_password
    )

    return redirect("/")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route('/order_summary')
@login_required
def place_order():
    return render_template('order_summary.html')

@app.route('/order_history')
def order_history():

    order_history = dbcs.execute("SELECT * FROM order_history")
    print(order_history)

    return render_template("order_history.html", order_history=order_history)