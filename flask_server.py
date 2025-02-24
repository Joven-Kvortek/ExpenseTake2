from tkinter.constants import INSERT

from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "login/register"

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
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            return jsonify({'message': 'Username already exists'}), 400
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        mysql.connection.commit()
        return jsonify({'message': 'Registration successful'}), 201
    except Exception as e:
        return jsonify({'message': 'Registration failed'}), 400


if __name__ == '__main__':
    app.run(debug=True)