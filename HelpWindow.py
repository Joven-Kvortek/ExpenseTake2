from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QDialog, QMainWindow, QLineEdit, QLabel, QVBoxLayout


class HelpWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Help")
        self.setGeometry(50, 50, 500, 500)
        self.setFixedSize(600, 500)
        layout = QVBoxLayout()

        add_help_button = QLabel("To add an expense, press the Add Expense Button, or press CTRL + A on your keyboard. Then, make sure to enter a name and cost for the expense.", self)
        add_help_button.setWordWrap(True)
        add_help_button.setStyleSheet("font-size: 12pt; font-weight: bold;")
        layout.addWidget(add_help_button)

        remove_help_button = QLabel("To remove an expense, press the Remove Expense Button, or press CTRL + R on your keyboard. Then, select the expense you want to remove from the list.", self)
        remove_help_button.setWordWrap(True)
        remove_help_button.setStyleSheet("font-size: 12pt; font-weight: bold;")
        layout.addWidget(remove_help_button)

        self.setLayout(layout)