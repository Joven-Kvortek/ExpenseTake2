
from PyQt6.QtGui import QFont

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
import requests

class login(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("User ID")
        self.layout = QVBoxLayout()

        self.setLayout(self.layout)

        self.username_line()
        self.password_line()
        self.login_button()

    def username_line(self):
        username = QLineEdit(self)
        username.setPlaceholderText("Enter username")
        self.layout.addWidget(username)

    def password_line(self):
        password = QLineEdit(self)
        password.setPlaceholderText("Enter password")
        self.layout.addWidget(password)

    def login_button(self):
        login_button = QPushButton("Login", self)
        login_button.setStyleSheet("background-color: black; color: white;")
        login_button.setFont(QFont("Times New Roman", 8))
        self.layout.addWidget(login_button)

class register(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Register")
        self.layout = QVBoxLayout()

        self.setLayout(self.layout)
        self.username_line()
        self.password_line()
        self.register_button()

    def username_line(self):
        self.username = QLineEdit(self)
        self.username.setPlaceholderText("Enter new username")
        self.layout.addWidget(self.username)

    def password_line(self):
        self.password = QLineEdit(self)
        self.password.setPlaceholderText("Enter new password")
        self.layout.addWidget(self.password)
    def register_button(self):
        register_button = QPushButton("Register", self)
        register_button.setStyleSheet("background-color: black; color: white;")
        register_button.setFont(QFont("Times New Roman", 8))
        register_button.clicked.connect(self.register_clicked)
        self.layout.addWidget(register_button)

    def register_clicked(self):
        username = self.username.text()
        password = self.password.text()
        self.send_registered_data(username, password)

    def send_registered_data(self, username, password):
        url = "http://127.0.0.1:5000/register"
        data = {"username": username, "password": password}
        response = requests.post(url, json=data)
        return response.json()





