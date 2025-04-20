from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import mysql.connector
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='static')
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

# Get user
@app.route('/account/<user_id>', methods=['GET'])
def get_user(user_id):
    # print('User Id ' + user_id)
    query = "SELECT * FROM users WHERE id = %s"
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()

    if user:
        return jsonify({
            "id": user[0],
            "name": user[1],
            "email": user[2],
            "dob": user[4],
            "gender": user[5]
        })
    else:
        return jsonify({"message": "User not found"}), 404

# Update User
@app.route('/update-account/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    dob = data.get('dob')
    gender = data.get('gender')

    update_query = """
        UPDATE users
        SET dob = %s, gender = %s
        WHERE id = %s
    """
    cursor.execute(update_query, (dob, gender, user_id))
    conn.commit()

    return jsonify({"message": "User updated successfully"}), 200


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

# Add Expense 
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

# Get Expense 
@app.route('/get-expenses/<user_id>', methods=['GET'])
def get_expenses(user_id):
    try:
        cursor.execute("SELECT id, category, item, amount, date, description FROM expenses where user_id = %s", (user_id,))
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
        # print("Error fetching expenses:", e)
        return jsonify({"message": "Failed to fetch expenses"}), 500

# Update salary 
@app.route('/update-salary', methods=['PATCH'])
def update_salary():
    data = request.get_json()
    user_id = data.get('userId')
    salary = data.get('salary')

    if not user_id or salary is None:
        return jsonify({'message': 'Missing userId or salary'}), 400

    # Check if income entry exists for this user
    cursor.execute("SELECT * FROM income WHERE user_id = %s", (user_id,))
    existing_income = cursor.fetchone()

    if existing_income:
        # Update salary
        update_query = "UPDATE income SET salary = %s WHERE user_id = %s"
        cursor.execute(update_query, (salary, user_id))
    else:
        # Insert new row with default budget 0
        insert_query = "INSERT INTO income (user_id, salary, budget) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (user_id, salary, 0.0))

    conn.commit()
    return jsonify({'message': 'Salary updated successfully'}), 200

# Update budget 
@app.route('/update-budget', methods=['PATCH'])
def update_budget():
    data = request.get_json()
    user_id = data.get('userId')
    budget = data.get('budget')

    if not user_id or budget is None:
        return jsonify({'message': 'Missing userId or budget'}), 400

    # Check if income entry exists for this user
    cursor.execute("SELECT * FROM income WHERE user_id = %s", (user_id,))
    existing_income = cursor.fetchone()

    if existing_income:
        # Update budget
        update_query = "UPDATE income SET budget = %s WHERE user_id = %s"
        cursor.execute(update_query, (budget, user_id))
    else:
        # Insert new row with default budget 0
        insert_query = "INSERT INTO income (user_id, budget, salary) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (user_id, budget, 0.0))

    conn.commit()
    return jsonify({'message': 'Budget updated successfully'}), 200

# fetch salary and budget 
@app.route('/get-income', methods=['POST'])
def get_income():
    data = request.get_json()
    user_id = data.get('userId')
    cursor.execute("SELECT salary, budget FROM income WHERE user_id = %s", (user_id,))
    income_data = cursor.fetchone()

    if income_data:
        salary, budget = income_data
        return jsonify({'salary': salary, 'budget': budget}), 200
    else:
        return jsonify({'message': 'Income details not found for this user'}), 404


# fetch salary, budget and remaining budget
@app.route('/get-remaining-budget', methods=['POST'])
def get_remaining_budget():
    data = request.get_json()
    user_id = data.get('userId')
    cursor.execute("SELECT salary, budget FROM income WHERE user_id = %s", (user_id,))
    income_data = cursor.fetchone()

    if income_data:
        salary, budget = income_data

        cursor.execute('SELECT SUM(amount) FROM expenses WHERE user_id=%s', (user_id,))
        total_expenses_result = cursor.fetchone()
        spent = total_expenses_result[0] if total_expenses_result and total_expenses_result[0] else 0

        remaining_budget = budget - spent

        return jsonify({'salary': salary, 'budget': budget, 'remaining_budget': remaining_budget, 'spent': spent}), 200
    else:
        return jsonify({'message': 'Income details not found for this user'}), 404

# Get recommendations 
@app.route('/recommendations/<user_id>', methods=['GET'])
def get_recommendations(user_id):
    try:
        conn4 = mysql.connector.connect(host='localhost', user='root', password='sHj@6378#jw', database='finance_db_1',ssl_disabled=True)
        cursor4 = conn4.cursor()

        user_id = int(user_id)  # Ensure it's an integer

        cursor4.execute("SELECT salary, budget FROM income WHERE user_id = %s", (user_id,))
        income_data = cursor4.fetchone()

        if income_data:
            salary, budget = income_data
            
            # Calculate total expenses
            cursor4.execute('SELECT SUM(amount) FROM expenses WHERE user_id=%s', (user_id,))
            total_expenses_result = cursor4.fetchone()
            total_expenses = total_expenses_result[0] if total_expenses_result and total_expenses_result[0] else 0
            
            # Calculate remaining budget
            remaining_budget = budget - total_expenses

            # Find the category with the highest spending
            cursor4.execute('SELECT category, SUM(amount) FROM expenses WHERE user_id=%s GROUP BY category ORDER BY SUM(amount) DESC LIMIT 1', (user_id,))
            top_category = cursor4.fetchone()
            highest_spending_category = top_category[0] if top_category else None
            highest_spending_amount = top_category[1] if top_category else 0

            # print('total_expenses')
            # print(total_expenses)
            # print('remaining_budget')
            # print(remaining_budget)
            # print('highest_spending_category')
            # print(highest_spending_category)
            # print("highest_spending_amount")
            # print(highest_spending_amount)

            recommendations = []

            if remaining_budget > (0.3 * budget):  # If more than 30% of budget is left
                recommendations.append("You have a good amount left in your budget! Consider saving or investing in mutual funds, stocks, or an emergency fund.")

            if remaining_budget < 0:  # If budget is exceeded
                recommendations.append("You have exceeded your budget! Try to cut down on unnecessary expenses like dining out or impulse shopping.")

            if highest_spending_category and total_expenses > 0 and highest_spending_amount > (0.5 * total_expenses):
                recommendations.append(f"You are spending a lot on {highest_spending_category}. Consider reducing these expenses to balance your budget.")

            # Step 4: Close connection
            cursor4.close()
            conn4.close()

            return jsonify({'recommendations': recommendations}), 200
        else:
            return jsonify({'message': 'Income details not found for this user'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# @app.route('/pie-chart', methods=['POST'])
# def pie_chart():
    try:
        conn1 = mysql.connector.connect(host='localhost', user='root', password='sHj@6378#jw', database='finance_db_1',ssl_disabled=True)
        cursor1 = conn1.cursor()
        data = request.get_json()
        user_id = data.get('userId')

        if not user_id:
            return jsonify({'error': 'User ID is required'}), 400

        cursor1.execute('SELECT category, SUM(amount) FROM expenses WHERE user_id=%s GROUP BY category',(user_id,))
        result = cursor1.fetchall()
        # print("DB Result:", result)

        if not result or all(len(row) < 2 for row in result):
            return jsonify({'error': 'No expense data found for this user'}), 404

        categories = [row[0] for row in result if row and len(row) > 1]
        amounts = [row[1] for row in result if row and len(row) > 1]

        plt.figure(figsize=(8, 6))
        plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
        plt.title('Expense Distribution')
        os.makedirs('static', exist_ok=True)
        chart_path = 'static/expense_chart-'+user_id+'.png'
        plt.savefig(chart_path)
        plt.close()

        # Step 4: Close connection
        cursor1.close()
        conn1.close()

        return jsonify({'chart_url': '/static/expense_chart-'+user_id+'.png'})

    except Exception as e:
        # print("Error:", e)
        return jsonify({'error': str(e)}), 500


# @app.route('/bar-chart', methods=['POST'])
# def bar_chart():
#     try:
#         conn2 = mysql.connector.connect(host='localhost', user='root', password='sHj@6378#jw', database='finance_db_1',ssl_disabled=True)
#         cursor2 = conn2.cursor()
#         data = request.get_json()
#         user_id = data.get('userId')

#         if not user_id:
#             return jsonify({'error': 'User ID is required'}), 400

#         cursor2.execute('''
#         SELECT DATE_FORMAT(date, '%Y-%m') AS month, SUM(amount) 
#         FROM expenses 
#         WHERE user_id = %s 
#         GROUP BY month 
#         ORDER BY month
#         ''', (user_id,))
#         result = cursor2.fetchall()
#         # print("DB Result:", result)

#         months = [row[0] for row in result]
#         expenses = [row[1] for row in result]

#         plt.figure(figsize=(10, 6))
#         plt.bar(months, expenses, color='skyblue')
#         plt.xlabel('Month')
#         plt.ylabel('Total Expenses (₹)')
#         plt.title('Monthly Expense Overview')
#         plt.xticks(rotation=45)
#         plt.tight_layout()

#         os.makedirs('static', exist_ok=True)
#         chart_path = 'static/bar_chart-'+user_id+'.png'
#         plt.savefig(chart_path)
#         plt.close()

#         # Step 4: Close connection
#         cursor2.close()
#         conn2.close()

#         return jsonify({'chart_url': '/static/bar_chart-'+user_id+'.png'})

#     except Exception as e:
#         # print("Error:", e)
#         return jsonify({'error': str(e)}), 500


@app.route('/charts', methods=['POST'])
def generate_charts():
    try:
        # Step 1: Connect to DB
        conn1 = mysql.connector.connect(
            host='localhost',
            user='root',
            password='sHj@6378#jw',
            database='finance_db_1',
            ssl_disabled=True
        )
        cursor1 = conn1.cursor()
        data = request.get_json()
        user_id = data.get('userId')

        if not user_id:
            return jsonify({'error': 'User ID is required'}), 400

        os.makedirs('static', exist_ok=True)

        ### ---------- PIE CHART: Expense Distribution by Category ----------
        cursor1.execute('SELECT category, SUM(amount) FROM expenses WHERE user_id=%s GROUP BY category', (user_id,))
        pie_data = cursor1.fetchall()

        if pie_data and any(len(row) >= 2 for row in pie_data):
            categories = [row[0] for row in pie_data if row and len(row) > 1]
            amounts = [row[1] for row in pie_data if row and len(row) > 1]

            plt.figure(figsize=(8, 6))
            plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
            plt.title('Expense Distribution')
            pie_path = f'static/expense_chart-{user_id}.png'
            plt.savefig(pie_path)
            plt.close()
        else:
            pie_path = None

        ### ---------- BAR CHART: Monthly Expense ----------
        cursor1.execute('''
            SELECT DATE_FORMAT(date, '%Y-%m') AS month, SUM(amount) 
            FROM expenses 
            WHERE user_id = %s 
            GROUP BY month 
            ORDER BY month
        ''', (user_id,))
        bar_data = cursor1.fetchall()

        if bar_data:
            months = [row[0] for row in bar_data]
            expenses = [row[1] for row in bar_data]

            plt.figure(figsize=(10, 6))
            plt.bar(months, expenses, color='skyblue')
            plt.xlabel('Month')
            plt.ylabel('Total Expenses (₹)')
            plt.title('Monthly Expense Overview')
            plt.xticks(rotation=45)
            plt.tight_layout()

            bar_path = f'static/bar_chart-{user_id}.png'
            plt.savefig(bar_path)
            plt.close()
        else:
            bar_path = None

        # Step 3: Close connection
        cursor1.close()
        conn1.close()

        # Step 4: Return both chart URLs
        return jsonify({
            'pie_chart_url': f'/{pie_path}' if pie_path else None,
            'bar_chart_url': f'/{bar_path}' if bar_path else None
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500



# @app.route('/line-chart', methods=['POST'])
# def line_chart():
#     try:
#         conn3 = mysql.connector.connect(host='localhost', user='root', 
#                       password='sHj@6378#jw', database='finance_db_1', ssl_disabled=True)
#         cursor3 = conn3.cursor()
#         data = request.get_json()
#         user_id = data.get('userId')

#         if not user_id:
#             return jsonify({'error': 'User ID is required'}), 400

#         # Get dates as strings in YYYY-MM-DD format directly from DB
#         cursor3.execute('''
#             SELECT DATE_FORMAT(date, '%Y-%m') AS date_str, SUM(amount) as total_amount
#             FROM expenses 
#             WHERE user_id = %s 
#             GROUP BY date 
#             ORDER BY date
#         ''', (user_id,))
#         result = cursor3.fetchall()
        
#         if not result:
#             return jsonify({'error': 'No data available for this user'}), 404

#         # Extract dates (as strings) and amounts
#         date_strings = [row[0] for row in result]
#         expenses = [float(row[1]) for row in result]

#         plt.figure(figsize=(12, 6))
        
#         # Plot using string dates directly
#         plt.plot(date_strings, expenses, color='blue', marker='o', linestyle='-', linewidth=2, markersize=8)
#         plt.xlabel('Date', fontsize=12)
#         plt.ylabel('Expense Amount (₹)', fontsize=12)
#         plt.title('Daily Expense Overview', fontsize=14, pad=20)
        
#         # Auto-format the x-axis labels
#         plt.xticks(rotation=45, ha='right')  # Rotate labels for better readability
#         plt.grid(True, linestyle='--', alpha=0.7)
#         plt.tight_layout()  # Adjust layout to prevent label cutoff

#         # Save the chart
#         os.makedirs('static', exist_ok=True)
#         chart_path = f'static/line_chart_{user_id}.png'
#         plt.savefig(chart_path, dpi=100, bbox_inches='tight')
#         plt.close()

#         cursor3.close()
#         conn3.close()

#         return jsonify({'chart_url': f'/static/line_chart_{user_id}.png'})

#     except Exception as e:
#         print("Error:", e)
#         return jsonify({'error': str(e)}), 500

# @app.route('/logout')
# def logout():
#     session.pop('user_id', None)
#     return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)


[('2025-01-01', 7000.0), 
('2025-01-02', 150.0), 
('2025-01-05', 510.0), ('2025-01-12', 3000.0), ('2025-01-14', 200.0), ('2025-01-21', 120.0), ('2025-01-25', 3000.0), ('2025-04-01', 100.0), ('2025-04-07', 2000.0), ('2025-04-08', 500.0), ('2025-04-09', 150.0), ('2025-04-10', 10.0), ('2025-04-15', 100.0), ('2025-04-16', 100.0), ('2025-04-17', 2000.0), ('2025-04-18', 120.0), ('2025-04-24', 100.0)]