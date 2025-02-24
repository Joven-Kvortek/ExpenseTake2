from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QDialog, QMainWindow, QLineEdit, QLabel, \
    QDialogButtonBox, QVBoxLayout, QHBoxLayout, QComboBox
from PyQt6.QtGui import QIcon, QFont
from HelpWindow import HelpWindow
from User_ID_Window import login, register
import sys





class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Expense Tracker")
        self.setWindowIcon(QIcon("windowicon.jpg"))
        self.setGeometry(50, 50, 1000, 500)

        self.expenses = {}
        self.action_history = []

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        self.help_button(bottom_layout)
        self.undo_button(bottom_layout)

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(5)
        self.register_button(top_layout)
        self.login_button(top_layout)

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

        self.setLayout(layout)


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

    def undo_button(self, bottom_layout):
        undo_button = QPushButton("Undo", self)
        undo_button.setStyleSheet("background-color: blue; color: white;")
        undo_button.setFont(QFont("Times New Roman", 9))
        undo_button.setShortcut("Ctrl+Z")
        # noinspection PyUnresolvedReferences
        undo_button.clicked.connect(self.undo)
        bottom_layout.addWidget(undo_button)

    def login_button(self, top_layout):
        login_button = QPushButton("Login", self)
        login_button.setStyleSheet("background-color: blue; color: white;")
        login_button.setFont(QFont("Times New Roman", 9))
        top_layout.addWidget(login_button, alignment=Qt.AlignmentFlag.AlignRight)
        # noinspection PyUnresolvedReferences
        login_button.clicked.connect(self.login_clicked)

    def register_button(self, top_layout):
        register_button = QPushButton("Register", self)
        register_button.setStyleSheet("background-color: blue; color: white;")
        register_button.setFont(QFont("Times New Roman", 9))
        top_layout.addWidget(register_button, alignment=Qt.AlignmentFlag.AlignRight)
        # noinspection PyUnresolvedReferences
        register_button.clicked.connect(self.register_clicked)
    def add_expense_clicked(self):
        self.w = AddExpenseWindow(self.expenses)
        # noinspection PyUnresolvedReferences
        self.w.expense_added.connect(self.update_expenses_total)
        self.w.show()

    def remove_expense_clicked(self):
        self.d = RemoveExpenseWindow(self.expenses)
        # noinspection PyUnresolvedReferences
        self.d.expense_removed.connect(self.remove_expenses_total)
        self.d.show()

    def help_clicked(self):
        self.h = HelpWindow()
        self.h.show()

    def login_clicked(self):
        self.l = login()
        self.l.show()
    def register_clicked(self):
        self.r = register()
        self.r.show()

    def update_expenses_total(self, expense_amount: float, expense_name: str):
        if expense_name in self.expenses:
            print("Expense already exists")
            return
        if expense_name and expense_amount:
            self.expenses_total = round(expense_amount + self.expenses_total, 2)
            self.expenses_total_label.setText(f"Total Expenses: ${self.expenses_total}")
            self.expenses[expense_name] = expense_amount

            self.action_history.insert(0, ("add", expense_name, expense_amount))
            print(self.expenses)
            print(self.action_history)


    def remove_expenses_total(self, expense_amount: float, expense_name: str):
        self.expenses_total = round(self.expenses_total - expense_amount, 2)
        self.expenses_total_label.setText(f"Total Expenses: ${self.expenses_total}")

        self.action_history.insert(0, ("remove", expense_name, expense_amount))
        print(self.expenses)
        print(self.action_history)



    def undo(self):
        print(self.action_history)
        if len(self.action_history) == 0:
            print("nothing to undo")
            return
        last_action = self.action_history.pop(0)
        if last_action[0] == "add":
            print("undo add")
            expense_name = last_action[1]
            expense_amount = last_action[2]
            self.expenses.pop(expense_name)
            self.expenses_total = round(self.expenses_total - expense_amount, 2)
            self.expenses_total_label.setText(f"Total Expenses: ${self.expenses_total}")
            print(self.expenses)

        if last_action[0] == "remove":
            print("undo remove")
            expense_name = last_action[1]
            expense_amount = last_action[2]
            self.expenses_total = round(self.expenses_total + expense_amount, 2)
            self.expenses_total_label.setText(f"Total Expenses: ${self.expenses_total}")
            self.expenses[expense_name] = expense_amount
            print(self.expenses)








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
    def __init__(self, dict, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Remove Expense")
        self.setGeometry(50, 50, 500, 500)
        self.expenses = dict


        layout = QVBoxLayout()

        self.box = QComboBox()
        self.box.setPlaceholderText("Select expense to remove")
        self.box.addItem("All Expenses")
        self.box.addItems(list(self.expenses.keys()))
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
        if self.confirmation_dialog(self):
            try:
                selected_expense = self.box.currentText()
                if selected_expense == "All Expenses":
                    # noinspection PyUnresolvedReferences
                    self.expense_removed.emit(sum(self.expenses.values()), "All Expenses")
                    print(sum(self.expenses.values(), 0))
                    self.expenses.clear()
                    self.box.clear()
                selected_value = self.expenses.get(selected_expense)
                if selected_value is not None:
                    # noinspection PyUnresolvedReferences
                    self.expense_removed.emit(selected_value, selected_expense)
                    self.expenses.pop(selected_expense)
                    self.box.removeItem(self.box.currentIndex())

                self.close()


            except ValueError:
                pass

    def confirmation_dialog(self, selected_expense):
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
        print(selected_expense)
        if self.box.currentText() == "":
            print("No expense selected!")
            warning_message = QLabel("No expense selected!", msg)
            layout.addWidget(warning_message)
        elif self.box.currentText() == "All Expenses":
            warning_message = QLabel("Are you sure you want to remove all expenses?", msg)
            warning_message.setWordWrap(True)
            layout.addWidget(warning_message)
        elif self.box.currentText() != "All Expenses" and selected_expense != "":
            warning_message = QLabel(f"Remove expense: {self.box.currentText()}?", msg)
            layout.addWidget(warning_message)

            return msg.exec() == QDialog.DialogCode.Accepted









    def closeEvent(self, event):
        self.close()












































app = QApplication([])
window = MainWindow()
window.show()
sys.exit(app.exec())