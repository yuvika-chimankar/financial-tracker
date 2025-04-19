from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import mysql.connector
import matplotlib.pyplot as plt
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Allows cross-origin requests from frontend
# app.secret_key = 'your_secret_key'

# Database connection
conn = mysql.connector.connect(host='localhost', user='root', password='sHj@6378#jw', database='finance_db_1')
cursor = conn.cursor()

# Create tables
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    dob DATE,
    gender VARCHAR(100)
)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS income (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    salary FLOAT NOT NULL,
    budget FLOAT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    category VARCHAR(100) NOT NULL,
    item VARCHAR(100) NOT NULL,
    amount FLOAT NOT NULL,
    date DATE NOT NULL,
    description TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
)''')
conn.commit()

# @app.route('/')
# def home():
#     return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    # Check if user with the email already exists
    check_query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(check_query, (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        return jsonify({"message": "Email already registered"}), 400

    # Insert new user
    insert_query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    cursor.execute(insert_query, (name, email, password))
    conn.commit()  # Save the changes

    return jsonify({"message": "Registration successful"}), 201


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         password = request.form['password']
#         cursor.execute('INSERT INTO users (name, email, password) VALUES (%s, %s)', (name, email, password))
#         conn.commit()
#         return redirect(url_for('login'))
#     return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Query to check user credentials
    query = "SELECT * FROM users WHERE email = %s AND password = %s"
    cursor.execute(query, (email, password))
    user = cursor.fetchone()

    if user:
        return jsonify({"message": "Login successful", "user": user}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#         cursor.execute('SELECT * FROM users WHERE email=%s AND password=%s', (email, password))
#         user = cursor.fetchone()
#         if user:
#             session['user_id'] = user[0]
#             return redirect(url_for('dashboard'))
#     return render_template('login.html')

# @app.route('/dashboard')
# def dashboard():
#     if 'user_id' not in session:
#         return redirect(url_for('login'))
#     cursor.execute('SELECT * FROM expenses WHERE user_id=%s', (session['user_id'],))
#     expenses = cursor.fetchall()
#     return render_template('dashboard.html', expenses=expenses)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    # Fetch latest budget of user (assuming user enters budget with every expense)
    cursor.execute('SELECT budget FROM expenses WHERE user_id = %s ORDER BY id DESC LIMIT 1', (user_id,))
    budget_data = cursor.fetchone()
    budget = budget_data[0] if budget_data else 0  # Default to 0 if no budget found

    # Calculate total expenses
    cursor.execute('SELECT SUM(amount) FROM expenses WHERE user_id = %s', (user_id,))
    total_expenses = cursor.fetchone()[0] or 0  # Default to 0 if no expenses

    remaining_budget = budget - total_expenses  # Calculate remaining budget

    # Define alert message
    alert_message = None
    if remaining_budget < 0:
        alert_message = "⚠️ Budget Exceeded! You have spent more than your allocated budget."
    elif remaining_budget <= (0.2 * budget):  # If remaining budget is less than 20% of total budget
        alert_message = "⚠️ Warning: Your budget is running low!"

    # Find the category with the highest spending
    cursor.execute('SELECT category, SUM(amount) FROM expenses WHERE user_id=%s GROUP BY category ORDER BY SUM(amount) DESC LIMIT 1', (user_id,))
    top_category = cursor.fetchone()
    highest_spending_category = top_category[0] if top_category else None
    highest_spending_amount = top_category[1] if top_category else 0

    # Generate AI-based recommendations
    recommendations = []

    if remaining_budget > (0.3 * budget):  # If more than 30% of budget is left
        recommendations.append("✅ You have a good amount left in your budget! Consider saving or investing in mutual funds, stocks, or an emergency fund.")

    if remaining_budget < 0:  # If budget is exceeded
        recommendations.append("⚠️ You have exceeded your budget! Try to cut down on unnecessary expenses like dining out or impulse shopping.")

    if highest_spending_category and highest_spending_amount > (0.5 * total_expenses):  # If one category has more than 50% of expenses
        recommendations.append(f"🔍 You are spending a lot on {highest_spending_category}. Consider reducing these expenses to balance your budget.")
    
    # Fetch all expenses
    cursor.execute('SELECT * FROM expenses WHERE user_id=%s', (user_id,))
    expenses = cursor.fetchall()

    return render_template('dashboard.html', budget=budget, remaining_budget=remaining_budget, expenses=expenses, recommendations=recommendations)


@app.route('/add-expense', methods=['POST'])
def add_expense():
    data = request.get_json()

    user_id = data.get('userId')
    category = data.get('category')
    item = data.get('item')
    amount = data.get('amount')
    date = data.get('date')
    description = data.get('description')

    insert_query = "INSERT INTO expenses (user_id, category, item, amount, date, description) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(insert_query, (user_id, category, item, amount, date, description))
    conn.commit()  # Save the changes

    return jsonify({"message": "Added Expense successfully" }), 201

# @app.route('/add-expense', methods=['POST'])
# def add_expense():
#     if 'user_id' in session:
#         category = request.form['category']
#         item = request.form['item']
#         amount = request.form['amount']
#         date = request.form['date']
#         description = request.form['description']
#         cursor.execute('INSERT INTO expenses (user_id, salary, budget, category, item, amount, date, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
#                        (session['user_id'], salary, budget, category, item, amount, date, description))
#         conn.commit()
#     return redirect(url_for('dashboard'))

@app.route('/get-expenses', methods=['GET'])
def get_expenses():
    try:
        cursor.execute("SELECT id, category, item, amount, date, description FROM expenses")
        rows = cursor.fetchall()

        # Convert the result into a list of dictionaries
        expenses = []
        for row in rows:
            expenses.append({
                "id": row[0],
                "category": row[1],
                "item": row[2],
                "amount": row[3],
                "date": row[4].strftime('%Y-%m-%d') if hasattr(row[4], 'strftime') else row[4],
                "description": row[5]
            })

        return jsonify(expenses), 200

    except Exception as e:
        print("Error fetching expenses:", e)
        return jsonify({"message": "Failed to fetch expenses"}), 500


@app.route('/visualize')
def visualize():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    cursor.execute('SELECT category, SUM(amount) FROM expenses WHERE user_id=%s GROUP BY category', (session['user_id'],))
    data = cursor.fetchall()

    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]

    plt.figure(figsize=(8, 6))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title('Expense Distribution')
    plt.savefig('static/expense_chart.png')
    plt.close()

    return render_template('visualization.html', chart='static/expense_chart.png')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
