import socket
import json
import sqlite3


# Database setup
def initialize_db():
    conn = sqlite3.connect("budget.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            amount REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# Database operations
def get_all_budgets():
    conn = sqlite3.connect("budget.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, amount FROM budgets")
    data = cursor.fetchall()
    conn.close()
    return [{"name": name, "amount": amount} for name, amount in data]


def add_budget(name, amount):
    try:
        conn = sqlite3.connect("budget.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO budgets (name, amount) VALUES (?, ?)", (name, amount))
        conn.commit()
        conn.close()
        return {"status": "success", "message": "Budget added successfully"}
    except sqlite3.IntegrityError:
        return {"status": "error", "message": "Budget already exists"}


def remove_budget(name):
    conn = sqlite3.connect("budget.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM budgets WHERE name = ?", (name,))
    conn.commit()
    deleted_count = cursor.rowcount
    conn.close()
    if deleted_count:
        return {"status": "success", "message": "Budget removed successfully"}
    else:
        return {"status": "error", "message": "Budget not found"}


# Server setup
def start_server(host="127.0.0.1", port=65432):
    initialize_db()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server started on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")

        data = client_socket.recv(1024).decode("utf-8")
        if not data:
            client_socket.close()
            continue

        try:
            request = json.loads(data)
            action = request.get("action")

            if action == "get_budgets":
                response = get_all_budgets()
            elif action == "add_budget":
                name = request.get("name")
                amount = request.get("amount")
                if name and amount is not None:
                    response = add_budget(name, amount)
                else:
                    response = {"status": "error", "message": "Invalid request format"}
            elif action == "remove_budget":
                name = request.get("name")
                if name:
                    response = remove_budget(name)
                else:
                    response = {"status": "error", "message": "Invalid request format"}
            else:
                response = {"status": "error", "message": "Unknown action"}
        except json.JSONDecodeError:
            response = {"status": "error", "message": "Invalid JSON format"}

        client_socket.send(json.dumps(response).encode("utf-8"))
        client_socket.close()


if __name__ == "__main__":
    start_server()