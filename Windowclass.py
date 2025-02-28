import requests
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QDialog, QMainWindow, QLineEdit, QLabel, \
    QDialogButtonBox, QVBoxLayout, QHBoxLayout, QComboBox, QMessageBox
from PyQt6.QtGui import QIcon, QFont
from HelpWindow import HelpWindow
from User_ID_Window import login_window, register_window
import sys





class MainWindow(QMainWindow):
    def __init__(self, auth_manager, undo_manager, total_expenses_manager):
        super().__init__()

        self.help_window = None
        self.add_expense_window = None
        self.remove_expense_window = None
        self.expenses_total_label = None
        self.expenses_total = None

        self.expenses = []
        self.action_history = []

        self.total = total_expenses_manager
        self.total.parent = self

        self.auth = auth_manager
        self.auth.parent = self

        self.undo = undo_manager
        self.undo.parent = self

        self.setup_ui()
    def setup_ui(self):

        self.setWindowTitle("Expense Tracker")
        self.setWindowIcon(QIcon("windowicon.jpg"))
        self.setGeometry(50, 50, 1000, 500)


        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        self.help_button(bottom_layout)
        self.undo.undo_button(bottom_layout)

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(5)
        self.auth.register_button(top_layout)
        self.auth.login_button(top_layout)

        top_layout_widget = QWidget()
        top_layout_widget.setLayout(top_layout)
        top_layout_widget.setContentsMargins(0, 0, 0, 0)

        self.expenses_total = 0
        self.expenses_total_label = QLabel(f"Total Expenses: ${self.expenses_total}", self)
        self.expenses_total_label.setStyleSheet(
            "font-size: 20px; font-weight: bold;"
        )

        layout.addWidget(top_layout_widget, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.expenses_total_label, alignment=Qt.AlignmentFlag.AlignCenter)



        self.add_expense_button(layout)
        self.remove_expense_button(layout)


        layout.addLayout(bottom_layout)
    def closeEvent(self, event):
        if self.close_confirmation(event):
            event.accept()
        else:
            event.ignore()

    def close_confirmation(self, event):
        msg = QDialog(self)
        msg.setWindowTitle("Confirmation")
        msg.setFont(QFont("Times New Roman", 12))
        layout = QVBoxLayout()
        message = QLabel("Would you like to save your changes?", msg)
        layout.addWidget(message)

        msg_buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Yes | QDialogButtonBox.StandardButton.No, msg)
        # noinspection PyUnresolvedReferences
        msg_buttons.accepted.connect(msg.accept)
        # noinspection PyUnresolvedReferences
        msg_buttons.rejected.connect(msg.reject)
        layout.addWidget(msg_buttons)
        msg.setLayout(layout)
        if msg.exec() == QDialog.DialogCode.Accepted:
            url = "http://127.0.0.1:5000/save_expenses/"
            data = self.expenses
            username = self.auth.login_window.username.text()
            requests.post(url, json={"username": username, "expenses": data})
            print(data)
            return True
        else:
            self.close()

    def add_expense_button(self, layout):
        add_expense_button = QPushButton("Add Expense", self)
        add_expense_button.setStyleSheet("background-color: black; color: white;")
        add_expense_button.setFont(QFont("Times New Roman", 12))
        add_expense_button.setMaximumSize(300,150)
        add_expense_button.setShortcut("Ctrl+A")
        layout.addWidget(add_expense_button)
        # noinspection PyUnresolvedReferences
        add_expense_button.clicked.connect(self.add_expense_clicked)

    def remove_expense_button(self, layout):
        remove_expense_button = QPushButton("Remove Expense", self)
        remove_expense_button.setStyleSheet("background-color: black; color: white;")
        remove_expense_button.setFont(QFont("Times New Roman", 9))
        remove_expense_button.setMaximumSize(300, 150)
        remove_expense_button.setShortcut("Ctrl+R")
        layout.addWidget(remove_expense_button)
        # noinspection PyUnresolvedReferences
        remove_expense_button.clicked.connect(self.remove_expense_clicked)

    def help_button(self, bottom_layout):
        help_button = QPushButton("Help", self)
        help_button.setStyleSheet("background-color: blue; color: white;")
        help_button.setFont(QFont("Times New Roman", 9))
        help_button.setShortcut("Ctrl+H")
        bottom_layout.addWidget(help_button)
        # noinspection PyUnresolvedReferences
        help_button.clicked.connect(self.help_clicked)
    def add_expense_clicked(self):
        self.add_expense_window = AddExpenseWindow(self.expenses)
        # noinspection PyUnresolvedReferences
        self.add_expense_window.expense_added.connect(self.total.update_expenses_total)
        self.add_expense_window.show()

    def remove_expense_clicked(self):
        try:
            if not self.auth.username:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Critical)
                msg.setWindowTitle("Error")
                msg.setText("Please login first!")
                msg.exec()
                return
            username = self.auth.login_window.username.text()
            print(username)

            self.remove_expense_window = RemoveExpenseWindow(self.expenses, self, username = username)
            # noinspection PyUnresolvedReferences
            self.remove_expense_window.expense_removed.connect(self.total.remove_expenses_total)
            self.remove_expense_window.show()
        except Exception as e:
            print(f"Error: {e}")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText("Must be logged in to remove expenses!")
            msg.exec()
            return

    def help_clicked(self):
        self.help_window = HelpWindow()
        self.help_window.show()

class total_expenses_manager:
    def __init__(self, parent):
        self.parent = parent
    def remove_expenses_total(self, selected_expense: float, selected_expense_name: str):
        self.parent.expenses_total = round(self.parent.expenses_total - selected_expense, 2)
        self.parent.expenses_total_label.setText(f"Total Expenses: ${self.parent.expenses_total}")

        self.parent.action_history.insert(0, ("remove", selected_expense_name, selected_expense))
        print(self.parent.expenses)
        print(self.parent.action_history)

    def update_expenses_total(self, expense_amount: float, expense_name: str):
        if expense_name in self.parent.expenses:
            print("Expense already exists")
            return
        if expense_name and expense_amount:
            self.parent.expenses_total = round(expense_amount + self.parent.expenses_total, 2)
            self.parent.expenses_total_label.setText(f"Total Expenses: ${self.parent.expenses_total}")
            self.parent.expenses.append({"name": expense_name, "amount": expense_amount})

            self.parent.action_history.insert(0, ("add", expense_name, expense_amount))
            print(self.parent.expenses)
            print(self.parent.action_history)

class UndoManager:
    def __init__(self, parent):
        self.parent = parent

    def undo_button(self, bottom_layout):
        undo_button = QPushButton("Undo", self.parent)
        undo_button.setStyleSheet("background-color: blue; color: white;")
        undo_button.setFont(QFont("Times New Roman", 9))
        undo_button.setShortcut("Ctrl+Z")
        bottom_layout.addWidget(undo_button)
        # noinspection PyUnresolvedReferences
        undo_button.clicked.connect(self.undo)

    def undo(self):
        print(self.parent.action_history)
        if len(self.parent.action_history) == 0:
            print("nothing to undo")
            return
        last_action = self.parent.action_history.pop(0)
        if last_action[0] == "add":
            print("undo add")
            expense_name = last_action[1]
            expense_amount = last_action[2]
            expense = next((expense for expense in self.parent.expenses if expense["name"] == expense_name), None)
            if expense is not None:
                self.parent.expenses.remove(expense)
            self.parent.expenses_total = round(self.parent.expenses_total - expense_amount, 2)
            self.parent.expenses_total_label.setText(f"Total Expenses: ${self.parent.expenses_total}")
            print(self.parent.expenses)

        if last_action[0] == "remove":
            print("undo remove")
            expense_name = last_action[1]
            expense_amount = last_action[2]
            self.parent.expenses_total = round(self.parent.expenses_total + expense_amount, 2)
            self.parent.expenses_total_label.setText(f"Total Expenses: ${self.parent.expenses_total}")
            self.parent.expenses.append({"name": expense_name, "amount": expense_amount})
            print(self.parent.expenses)

class AuthManager:
    def __init__(self, parent, username, password):
        self.register_window = None
        self.login_window = None
        self.parent = parent
        self.username = None
        self.password = None

    def login_button(self, top_layout):
        login_button = QPushButton("Login", self.parent)
        login_button.setStyleSheet("background-color: blue; color: white;")
        login_button.setFont(QFont("Times New Roman", 9))
        top_layout.addWidget(login_button, alignment=Qt.AlignmentFlag.AlignRight)
        # noinspection PyUnresolvedReferences
        login_button.clicked.connect(self.login_clicked)

    def login_clicked(self):
        self.login_window = login_window(self)
        self.login_window.show()

    def load_data(self, username):
        try:
            response = requests.get("http://127.0.0.1:5000/get_expenses/", json={"username": username})
            if response.status_code == 200:
                data = response.json()
                expenses = data.get("expenses", [])

                self.parent.expenses.clear()
                unique_expenses = {exp['name']: exp for exp in expenses}.values()

                self.parent.expenses.extend(unique_expenses)

                self.parent.expenses_total = sum([float(expense["amount"]) for expense in expenses])
                self.parent.expenses_total_label.setText(f"Total Expenses: ${self.parent.expenses_total}")
            else:
                print(f"Error: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")

    def register_button(self, top_layout):
        register_button = QPushButton("Register", self.parent)
        register_button.setStyleSheet("background-color: blue; color: white;")
        register_button.setFont(QFont("Times New Roman", 9))
        top_layout.addWidget(register_button, alignment=Qt.AlignmentFlag.AlignRight)
        # noinspection PyUnresolvedReferences
        register_button.clicked.connect(self.register_clicked)

    def register_clicked(self):
        self.register_window = register_window(self)
        self.register_window.show()

class AddExpenseWindow(QWidget):
    expense_added = pyqtSignal(float,str)
    def __init__(self, dict, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Expense")
        self.setGeometry(50, 50, 500, 500)
        layout = QVBoxLayout()
        self.expenses = dict
        self.expense_name = QLineEdit(self)
        self.expense_name.setPlaceholderText("Enter expense name")
        layout.addWidget(self.expense_name)

        self.expense_cost = QLineEdit(self)
        self.expense_cost.setPlaceholderText("Enter expense cost")
        # noinspection PyUnresolvedReferences
        layout.addWidget(self.expense_cost)



        confirm_button = QPushButton("Confirm", self)
        confirm_button.setGeometry(150, 400, 100, 25)
        confirm_button.setStyleSheet("background-color: black; color: white;")
        confirm_button.setFont(QFont("Times New Roman", 8))
        # noinspection PyUnresolvedReferences
        confirm_button.clicked.connect(self.confirm_clicked)
        layout.addWidget(confirm_button)

        self.setLayout(layout)

    def confirm_clicked(self):
        self.confirmation_dialog_amount()
        try:
            expense_amount = float(self.expense_cost.text())
            expense_name = str(self.expense_name.text())
            if expense_name in self.expenses:
                return
            else:
                # noinspection PyUnresolvedReferences
                self.expense_added.emit(expense_amount, expense_name)

        except ValueError:
            pass

    def confirmation_dialog_amount(self):
        msg = QDialog(self)
        msg.setWindowTitle("Confirmation")
        msg.setFont(QFont("Times New Roman", 12))
        layout = QVBoxLayout()
        message = QLabel("Do you want to save this expense?", msg)
        layout.addWidget(message)

        msg_buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel,
            msg)
        # noinspection PyUnresolvedReferences
        msg_buttons.accepted.connect(msg.accept)
        # noinspection PyUnresolvedReferences
        msg_buttons.rejected.connect(msg.reject)

        layout.addWidget(msg_buttons)
        msg.setLayout(layout)
        if self.expense_name.text() == "":
            warning_message = QLabel("Please enter an expense name!", msg)
            layout.addWidget(warning_message)
        if self.expense_cost.text() == "":
            warning_message = QLabel("Please enter an expense cost!", msg)
            layout.addWidget(warning_message)
        if self.expense_name.text() in self.expenses:
            warning_message = QLabel("Expense already exists!", msg)
            layout.addWidget(warning_message)

        if msg.exec() == QDialog.DialogCode.Accepted:
            self.close()
        else:
            self.expense_name.clear()
            self.expense_cost.clear()

    def closeEvent(self, event):
        self.close()

class RemoveExpenseWindow(QWidget):
    expense_removed = pyqtSignal(float, str)
    def __init__(self, expense_list, main_window, username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.MainWindow = main_window
        self.expenses = expense_list
        self.username = username
        self.setWindowTitle("Remove Expense")
        self.setGeometry(50, 50, 500, 500)


        layout = QVBoxLayout()

        self.box = QComboBox()
        self.box.setPlaceholderText("Select expense to remove")
        self.box.addItem("All Expenses")
        self.box.addItems([expense["name"] for expense in self.expenses])
        layout.addWidget(self.box)




        confirm_button = QPushButton("Confirm", self)
        confirm_button.setGeometry(150, 400, 100, 25)
        confirm_button.setStyleSheet("background-color: black; color: white;")
        confirm_button.setFont(QFont("Times New Roman", 8))
        # noinspection PyUnresolvedReferences
        confirm_button.clicked.connect(self.confirm_clicked)


        layout.addWidget(confirm_button)

        self.setLayout(layout)


    def confirm_clicked(self):
        selected_expense_name = self.box.currentText()
        if not selected_expense_name:
            print("No expense selected!")
            return

        if self.confirmation_dialog(selected_expense_name):
            try:
                if selected_expense_name == "All Expenses":
                    total_cost = sum([float(expense["amount"]) for expense in self.expenses])
                    # noinspection PyUnresolvedReferences
                    self.expense_removed.emit(total_cost, "All Expenses")
                    self.expenses.clear()
                    self.box.clear()
                else:
                    selected_expense = next((expense for expense in self.expenses if expense["name"] == selected_expense_name), None)
                    if selected_expense is not None:
                        try:
                            request_data = {"username": self.username, "expense_name": selected_expense_name, "expense_amount": selected_expense["amount"]}
                            print(f"Request data: {request_data}")
                            response = requests.post("http://127.0.0.1:5000/remove_expense/", json=request_data)
                            if response.status_code == 200:
                                print("Expense removed successfully!")
                                # noinspection PyUnresolvedReferences
                                self.expense_removed.emit(float(selected_expense["amount"]), selected_expense_name)
                                self.expenses.remove(selected_expense)
                                self.box.removeItem(self.box.currentIndex())
                            else:
                                print(f"Error: {response.status_code}")
                        except Exception as e:
                            print(f"Error with backend: {e}")
                self.close()
            except Exception as e:
                print(f"Error: {e}")

    def confirmation_dialog(self, selected_expense_name):
        msg = QDialog(self)
        msg.setWindowTitle("Confirmation")
        msg.setFont(QFont("Times New Roman", 12))
        layout = QVBoxLayout()

        msg_buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Yes | QDialogButtonBox.StandardButton.No, msg)
        layout.addWidget(msg_buttons)
        # noinspection PyUnresolvedReferences
        msg_buttons.accepted.connect(msg.accept)
        # noinspection PyUnresolvedReferences
        msg_buttons.rejected.connect(msg.reject)
        msg.setLayout(layout)
        print(selected_expense_name)
        if self.box.currentText() == "":
            print("No expense selected!")
            warning_message = QLabel("No expense selected!", msg)
            layout.addWidget(warning_message)
        elif self.box.currentText() == "All Expenses":
            warning_message = QLabel("Are you sure you want to remove all expenses?", msg)
            warning_message.setWordWrap(True)
            layout.addWidget(warning_message)
        elif self.box.currentText() != "All Expenses" and selected_expense_name != "":
            warning_message = QLabel(f"Remove expense: {self.box.currentText()}?", msg)
            layout.addWidget(warning_message)

            return msg.exec() == QDialog.DialogCode.Accepted









    def closeEvent(self, event):
        self.close()

app = QApplication([])
auth_manager = AuthManager(None, "user1", "password123")
undo_manager = UndoManager(None)
total_expenses = total_expenses_manager(None)

window = MainWindow(auth_manager, undo_manager, total_expenses)
window.show()
sys.exit(app.exec())