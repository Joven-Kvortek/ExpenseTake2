import socket
import json
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem


class budget_window(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.table = None
        self.budget_amount = None
        self.budget_name = None

        self.setWindowTitle("Budget")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setup_ui()
        self.load_budgets()

    def send_request(self, request_data):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect(("127.0.0.1", 65432))
            client_socket.send(json.dumps(request_data).encode("utf-8"))
            response = client_socket.recv(1024).decode("utf-8")
        except ConnectionError as e:
            print(f"Error: Could not connect to the server. {e}")
            response = json.dumps({"error": "Connection failed"})
        finally:
            client_socket.close()
        return response

    def fetch_budgets(self):
        request_data = {"action": "get_budgets"}
        response = self.send_request(request_data)
        try:
            budgets = json.loads(response)
            if "error" in budgets:
                print(f"Error: {budgets['error']}")
                return []
            return budgets
        except json.JSONDecodeError:
            print("Error: Invalid JSON response")
            return []
    def load_budgets(self):
        budgets = self.fetch_budgets()
        self.display_budgets(budgets)
        print(
            f"Loaded {len(budgets)} budgets from the server."
        )

    def display_budgets(self, budgets):
        self.table.setRowCount(0)
        for budget in budgets:
            name = budget.get("name", "")
            amount = budget.get("amount", 0)
            current_row_count = self.table.rowCount()
            self.table.insertRow(current_row_count)
            self.table.setItem(current_row_count, 0, QTableWidgetItem(name))
            self.table.setItem(current_row_count, 1, QTableWidgetItem(str(amount)))

    def remove_budget(self):
        selected_row = self.table.currentRow()

        if selected_row == -1:
            print("No budget selected")
            return
        budget_name = self.table.item(selected_row, 0).text()
        request_data = {"action": "remove_budget", "name": budget_name}
        response = self.send_request(request_data)
        response_data = json.loads(response)
        if response_data.get("status") == "success":
            print(f"Budget '{budget_name}' removed successfully")
            self.table.removeRow(selected_row)
        else:
            print(f"Error: {response_data.get('message')}")


    def setup_ui(self):
        self.setGeometry(50, 50, 500, 500)
        self.budget_name_line()
        self.budget_amount_line()
        self.add_budget_button()
        self.remove_budget_button()
        self.budget_table()

    def budget_name_line(self):
        self.budget_name = QLineEdit(self)
        self.budget_name.setPlaceholderText("Enter budget name")
        self.layout.addWidget(self.budget_name)

    def budget_amount_line(self):
        self.budget_amount = QLineEdit(self)
        self.budget_amount.setPlaceholderText("Enter budget amount")
        self.layout.addWidget(self.budget_amount)

    def add_budget_button(self):
        add_button = QPushButton("Add budget", self)
        add_button.clicked.connect(self.save_budget)
        add_button.clicked.connect(self.add_budget_to_table)
        self.layout.addWidget(add_button)

    def remove_budget_button(self):
        delete_button = QPushButton("Delete budget", self)
        delete_button.clicked.connect(self.remove_budget)
        self.layout.addWidget(delete_button)

    def save_budget(self):
        print("Saving budget")
        try:
            name = self.budget_name.text()
            amount = self.budget_amount.text()
            print(f"Name: {name}, Amount: {amount}")
            if not name or not amount:
                print("Both name and amount are required.")
                return
            else:
                try:
                    amount = float(amount)
                    response = self.send_request(
                        {"action": "add_budget", "name": name, "amount": amount}
                    )
                    print(f"Response: {response}")
                except ValueError:
                    print("Please enter a valid budget amount")
        except Exception as e:
            print(f"An error occurred: {e}")


    def budget_table(self):
        self.table = QTableWidget(self)
        self.table.setRowCount(0)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Budget Name", "Budget Amount"])
        self.layout.addWidget(self.table)

    def add_budget_to_table(self):
        budget_name = self.budget_name.text()
        budget_amount = self.budget_amount.text()
        if not budget_name or not budget_amount:
            print("Please enter a budget name and amount")
            return
        try:
            float(budget_amount)
        except ValueError:
            print("Please enter a valid budget amount")
            return
        if budget_name != '' and budget_amount != '':
            current_row_count = self.table.rowCount()
            self.table.insertRow(current_row_count)
            self.table.setItem(self.table.rowCount() - 1, 0, QTableWidgetItem(budget_name))
            self.table.setItem(self.table.rowCount() - 1, 1, QTableWidgetItem(budget_amount))
            self.budget_name.clear()
            self.budget_amount.clear()


