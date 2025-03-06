import requests
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QLabel


class view_all_expenses_window(QWidget):
    def __init__(self, username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.table = None
        self.username = username
        self.setWindowTitle("View all expenses")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setupUI()
        self.load_data(self.username)
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.refresh)
        self.refresh_timer.start(1000)

    def setupUI(self):
        self.setGeometry(50, 50, 500, 500)
        self.label()
        self.setup_table()

    def load_data(self, username):
        self.table.setSortingEnabled(False)
        try:
            response = requests.post(f"http://127.0.0.1:5002/get_all_expenses/", json={"username": username})
            if response.status_code == 200:
                data = response.json()
                expenses = data.get("expenses", [])
                self.table.setRowCount(0)
                for expense in expenses:
                    name = expense.get("name", "")
                    cost = expense.get("amount", 0)
                    current_row_count = self.table.rowCount()
                    self.table.insertRow(current_row_count)
                    self.table.setItem(current_row_count, 0, QTableWidgetItem(name))
                    self.table.setItem(current_row_count, 1, FloatTableWidgetItem(cost))
        except Exception as e:
            print(f"An error occurred: {e}")
        self.table.setSortingEnabled(True)
    def refresh(self):
        self.load_data(self.username)


    def label(self):
        label = QLabel("Here is all your expenses", self)
        label.setStyleSheet("font-size: 12pt; font-weight: bold;")
        label.setAlignment(label.alignment())
        self.layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
        

    def setup_table(self):
        self.table = QTableWidget(self)
        self.table.setRowCount(0)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Name", "Cost"])
        self.table.setSortingEnabled(True)
        self.layout.addWidget(self.table)

class FloatTableWidgetItem(QTableWidgetItem):
    def __init__(self, value):
        super().__init__(str(value))

    def __lt__(self, other):
        try:
            return float(self.text()) < float(other.text())
        except ValueError:
            return super().__lt__(other)
