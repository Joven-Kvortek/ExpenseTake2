from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
app = Flask(__name__)
content_type = {'Content-Type': 'application/json'}

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '290826'
app.config['MYSQL_DB'] = "Expense_App_Login"

mysql = MySQL(app)

@app.route('/get_all_expenses/', methods=['GET', 'POST'])
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
    app.run(port=5002, debug=True)