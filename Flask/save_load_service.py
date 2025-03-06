from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
app = Flask(__name__)
content_type = {'Content-Type': 'application/json'}

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '290826'
app.config['MYSQL_DB'] = "Expense_App_Login"

mysql = MySQL(app)




@app.route('/save_expenses/', methods=['GET', 'POST'])
def save_expenses():
    data = request.json
    if not data:
        return jsonify({'message': 'No data provided'}), 400
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

if __name__ == "__main__":
    app.run(port=5001, debug=True)
