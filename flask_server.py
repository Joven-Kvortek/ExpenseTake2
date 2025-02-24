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
    print(username)
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()
        print(existing_user)
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



if __name__ == '__main__':
    app.run(debug=True)