from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "login/register"
content_type = {'Content-Type': 'application/json'}

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '290826'
app.config['MYSQL_DB'] = "Expense_App_Login"

mysql = MySQL(app)

@app.route('/register/', methods=['GET', 'POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        mysql.connection.commit()
        return jsonify({'message': 'Registration successful'}), 201
    except Exception as e:
        return jsonify({'message': 'Registration failed'}), 400

@app.route('/check_user/', methods=['GET', 'POST'])
def check_user():
    data = request.json
    username = data.get('username')
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            return jsonify({'exists': True}), 200
        return jsonify({'exists': False}), 200
    except Exception as e:
        return jsonify({'message': 'Database error'}), 500

@app.route('/login/', methods=['GET', 'POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT username, password FROM users WHERE username = %s", (username,))

        existing_user = cursor.fetchone()
        if existing_user:
            stored_password = existing_user[1]
            if stored_password != password:
                print("wrong password")
                return jsonify({'wrong_password': True}), 200
            return jsonify({'exists': True}), 200
        return jsonify({'exists': False}), 401
    except Exception as e:
        return jsonify({'message': 'Database error'}), 500

@app.route('/save_expenses/', methods=['GET', 'POST'])
def save_expenses():
    data = request.json
    username = data.get('username')
    expenses = data.get('expenses')
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if not user:
            return jsonify({'message': 'User not found'}), 404
        user_id = user[0]

        for expense in expenses:
            expense_name = expense['name']
            expense_amount = expense['amount']
            cursor.execute("SELECT * FROM expenses WHERE user_id = %s AND expense = %s AND amount = %s", (user_id, expense_name, expense_amount))
            existing_expense = cursor.fetchone()

            if not existing_expense:
                cursor.execute("INSERT INTO expenses (user_id, expense, amount) VALUES (%s, %s, %s)", (user_id, expense_name, expense_amount))

        mysql.connection.commit()
        return jsonify({'message': 'Expenses saved successfully'}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'Database error'}), 500

@app.route('/get_expenses/', methods=['GET', 'POST'])
def get_expenses():
    data = request.json
    username = data.get('username')
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        if not user:
            return jsonify({'message': 'User not found'}), 404
        user_id = user[0]
        cursor.execute("SELECT expense, amount FROM expenses WHERE user_id = %s", (user_id,))
        expenses = cursor.fetchall()
        expense_list = [{"name": expense[0], "amount": expense[1]} for expense in expenses]
        return jsonify({'expenses': expense_list}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'Database error'}), 500
@app.route('/remove_expense/', methods=['GET', 'POST'])
def remove_expense():
    data = request.json
    username = data.get('username')
    expense_name = data.get('expense_name')
    expense_amount = data.get('expense_amount')
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        if not user:
            return jsonify({'message': 'User not found'}), 404
        user_id = user[0]

        cursor.execute("DELETE FROM expenses WHERE user_id = %s AND expense = %s AND amount = %s", (user_id, expense_name, expense_amount))
        mysql.connection.commit()

        return jsonify({'message': 'Expense removed successfully'}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'Database error'}), 500



if __name__ == '__main__':
    app.run(debug=True)