# Mr. Pizza: Flask-Based Online Pizza Ordering Platform

##### This was submited as a Final Project to the Harvard's CS50X Introduction To Computer Science.

#### Video Demo:  <https://youtu.be/bCzJjgbsmbU>
#### Description:
As a current employee at Mr. Pizza, I identified the necessity for an efficient and user-friendly online order management system. Leveraging Flask and Python programming, I've crafted a website that streamlines the pizza ordering process, providing a seamless and engaging platform for customers.

## Key Features and Routes
### The Mr. Pizza website is built upon a Flask application and employs Python programming to provide a seamless ordering experience. With nine essential routes, the website encompasses:

/: The homepage, welcoming users with a personalized message and a direct link to place orders. <br>
/order: A dedicated page where users can configure their pizza orders, including size and quantity. <br>
/insert_order: Responsible for securely adding orders to the SQL database for accurate order management.<br>
/login: The login page, ensuring secure access for registered users.<br>
/register: A user-friendly registration process to create new accounts. <br>
/get_user_id: Utilizes JSON to retrieve user IDs for effective storage in the orders database.<br>
/logout: A straightforward option to log out users and protect their privacy.<br>
/order_summary: Displays the success of the order and provides a detailed summary.<br>
/order_history: A comprehensive view of past orders, presented in an accessible table format.<br>

### User-Centric Design and Functionality

With a focus on user experience, the Mr. Pizza website features a clean and intuitive design. The layout boasts a navigation bar that adapts based on user activity—offering Home, Order History, and Logout options for logged-in users, and Login and Register options for new users.

The homepage welcomes users with a friendly message and a prominent "Order Now" button that leads directly to the ordering page. Here, a thoughtfully designed interface allows customers to select their desired pizza, customize its size and quantity, and add it to their cart. To ensure accuracy, a built-in algorithm prevents the addition of items with a quantity of zero.

##### One standout feature is the dynamic right-side tab that elegantly slides into view whenever the "Add to Order" button is clicked. This tab signals the user to review their order summary and offers convenient editing and deletion options. Upon confirming their order, customers are redirected to a dedicated page displaying their order summary. The order is also automatically stored in the order history database for future reference.

Secure Data Management
At the core of Mr. Pizza's functionality lies a robust data management system. The website employs Flask's session mechanism to securely manage user activities. All user-related data is stored in a secure SQL database, ensuring the privacy and integrity of personal information.
