from mimetypes import inited

from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QDialog, QMainWindow, QLineEdit, QLabel, \
    QDialogButtonBox, QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout
from PyQt6.QtGui import QIcon, QFont
import sys

git init




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Expense Tracker")
        self.setWindowIcon(QIcon("windowicon.jpg"))
        self.setGeometry(50, 50, 1000, 500)

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

    def add_expense_clicked(self):
        self.w = AddExpenseWindow()
        # noinspection PyUnresolvedReferences
        self.w.expense_added.connect(self.update_expenses_total)
        self.w.show()

    def update_expenses_total(self, amount):
        self.expenses_total = amount + self.expenses_total
        self.expenses_total_label.setText(f"Total Expenses: ${self.expenses_total}")




class AddExpenseWindow(QWidget):
    expense_added = pyqtSignal(float)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Expense")
        self.setGeometry(50, 50, 500, 500)
        layout = QVBoxLayout()

        self.expense_name = QLineEdit(self)
        self.expense_name.setPlaceholderText("Enter expense name")
        layout.addWidget(self.expense_name)

        self.expense_cost = QLineEdit(self)
        self.expense_cost.setPlaceholderText("Enter expense cost")
        # noinspection PyUnresolvedReferences
        layout.addWidget(self.expense_cost)

        self.label1 = QLabel("Expense cost added successfully!", self)
        layout.addWidget(self.label1)
        self.label1.hide()

        self.label2 = QLabel("Expense name added successfully!", self)
        layout.addWidget(self.label2)
        self.label2.hide()

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
            amount_str = self.expense_cost.text()
            print(amount_str)
            amount = float(self.expense_cost.text())
            # noinspection PyUnresolvedReferences
            self.expense_added.emit(amount)
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
        if msg.exec() == QDialog.DialogCode.Accepted:
            self.close()
        else:
            self.expense_name.clear()
            self.expense_cost.clear()

    def closeEvent(self, event):
        self.close()



































app = QApplication([])
window = MainWindow()
window.show()
sys.exit(app.exec())