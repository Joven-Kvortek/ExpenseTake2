from os import remove

from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QDialog, QMainWindow, QLineEdit, QLabel, QListWidget, \
    QDialogButtonBox, QVBoxLayout, QHBoxLayout, QCheckBox, QComboBox
from PyQt6.QtGui import QIcon, QFont
import sys





class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Expense Tracker")
        self.setWindowIcon(QIcon("windowicon.jpg"))
        self.setGeometry(50, 50, 1000, 500)

        self.expenses = {}

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.expenses_total = 0
        self.expenses_total_label = QLabel(f"Total Expenses: ${self.expenses_total}", self)
        self.expenses_total_label.setStyleSheet(
            "font-size: 20px; font-weight: bold;"
        )
        layout.addWidget(self.expenses_total_label)
        layout.setAlignment(self.expenses_total_label, Qt.AlignmentFlag.AlignCenter)


        self.add_expense_button(layout)

        self.remove_expense_button(layout)

        self.setLayout(layout)


    def add_expense_button(self, layout):
        add_expense_button = QPushButton("Add Expense", self)
        add_expense_button.setStyleSheet("background-color: black; color: white;")
        add_expense_button.setFont(QFont("Times New Roman", 12))
        add_expense_button.setMaximumSize(300,150)
        layout.addWidget(add_expense_button)
        # noinspection PyUnresolvedReferences
        add_expense_button.clicked.connect(self.add_expense_clicked)

    def remove_expense_button(self, layout):
        remove_expense_button = QPushButton("Remove Expense", self)
        remove_expense_button.setStyleSheet("background-color: black; color: white;")
        remove_expense_button.setFont(QFont("Times New Roman", 9))
        remove_expense_button.setMaximumSize(300, 150)
        layout.addWidget(remove_expense_button)
        # noinspection PyUnresolvedReferences
        remove_expense_button.clicked.connect(self.remove_expense_clicked)

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

    def update_expenses_total(self, expense_amount, expense_name):
        if expense_name in self.expenses:
            print("Expense already exists")
            return
        if expense_name and expense_amount:
            self.expenses_total = round(expense_amount + self.expenses_total, 2)
            self.expenses_total_label.setText(f"Total Expenses: ${self.expenses_total}")
            self.expenses[expense_name] = expense_amount




    def remove_expenses_total(self, expense_removed):
        self.expenses_total = round(self.expenses_total - expense_removed, 2)
        self.expenses_total_label.setText(f"Total Expenses: ${self.expenses_total}")




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
    expense_removed = pyqtSignal(float)
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
        self.confirmation_dialog()
        try:
            selected_expense = self.box.currentText()
            selected_value = self.expenses.get(selected_expense)
            if selected_value is not None:
                self.expense_removed.emit(selected_value)
                self.expenses.pop(selected_expense)
                self.box.removeItem(self.box.currentIndex())
            if selected_expense == "All Expenses":
                self.expense_removed.emit(sum(self.expenses.values()))
                self.expenses.clear()
                self.box.clear()


        except ValueError:
            pass

    def confirmation_dialog(self):
        msg = QDialog(self)
        msg.setWindowTitle("Confirmation")
        msg.setFont(QFont("Times New Roman", 12))
        layout = QVBoxLayout()

        msg_buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Yes | QDialogButtonBox.StandardButton.No, msg)
        layout.addWidget(msg_buttons)
        msg_buttons.accepted.connect(msg.accept)
        msg_buttons.rejected.connect(msg.reject)
        msg.setLayout(layout)
        if self.box.currentText() == "":
            warning_message = QLabel("No expense selected!", msg)
            warning_message.setStyleSheet(
                "font-weight: bold;")
            layout.addWidget(warning_message)
        if self.box.currentText() == "All Expenses":
            warning_message = QLabel("Remove all expenses?", msg)
            layout.addWidget(warning_message)
            warning_message_2 = QLabel("This action cannot be undone!", msg)
            layout.addWidget(warning_message_2)
        if self.box.currentText() != "All Expenses" and self.box.currentText() != "":
            warning_message = QLabel(f"Remove expense: {self.box.currentText()}?", msg)
            layout.addWidget(warning_message)
            warning_message_2 = QLabel("This action cannot be undone!", msg)
            layout.addWidget(warning_message_2)

        if msg.exec() == QDialog.DialogCode.Accepted:
            self.close()
        else:
            self.box.clear()






    def closeEvent(self, event):
        self.close()












































app = QApplication([])
window = MainWindow()
window.show()
sys.exit(app.exec())