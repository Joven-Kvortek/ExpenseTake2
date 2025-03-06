
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QDialog, QDialogButtonBox
import requests

class login_window(QWidget):
    def __init__(self, auth_manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.password = None
        self.username = None
        self.auth_manager = auth_manager
        self.setWindowTitle("User ID")
        self.layout = QVBoxLayout()

        self.setLayout(self.layout)

        self.username_line()
        self.password_line()
        self.login_button()

    def username_line(self):
        self.username = QLineEdit(self)
        self.username.setPlaceholderText("Enter username")
        self.layout.addWidget(self.username)

    def password_line(self):
        self.password = QLineEdit(self)
        self.password.setPlaceholderText("Enter password")
        self.layout.addWidget(self.password)

    def login_button(self):
        login_button = QPushButton("Login", self)
        login_button.setStyleSheet("background-color: black; color: white;")
        login_button.setFont(QFont("Times New Roman", 8))
        login_button.clicked.connect(self.login_clicked)
        self.layout.addWidget(login_button)

    def login_clicked(self):
        url = "http://127.0.0.1:5000/login/"
        data = {"username": self.username.text(), "password": self.password.text()}
        response = requests.post(url, json=data)
        print(data)
        if response.json().get('wrong_password'):
            self.wrong_password()
        elif response.json().get('exists'):
            self.auth_manager.username = self.username.text()
            self.login_successful()
            self.auth_manager.load_data(self.username.text())
        else:
            self.login_failed()

    def login_successful(self):
        msg = QDialog(self)
        msg.setWindowTitle("Login Successful")
        success = QLabel("Login Successful!", msg)
        msg.setFont(QFont("Times New Roman", 12))
        success.show()
        msg.exec()
        self.close()

    def wrong_password(self):
        msg = QDialog(self)
        msg.setWindowTitle("Wrong Password")
        fail = QLabel("Wrong Password!", msg)
        msg.setFont(QFont("Times New Roman", 12))
        fail.show()
        msg.exec()
        self.password.clear()

    def login_failed(self):
        msg = QDialog(self)
        msg.setWindowTitle("Login Failed")
        fail = QLabel("Login Failed!", msg)
        msg.setFont(QFont("Times New Roman", 12))
        fail.show()
        msg.exec()
        self.username.clear()
        self.password.clear()


class register_window(QWidget):
    def __init__(self, auth_manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = None
        self.password = None
        self.auth_manager = auth_manager
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
        self.confirm_dialog()

    def send_registered_data(self, username, password):
        url = "http://127.0.0.1:5000/register/"
        data = {"username": username, "password": password}
        response = requests.post(url, json=data)
        return response.json()


    def confirm_dialog(self):
        msg = QDialog(self)
        msg.setWindowTitle("Confirmation")
        msg.setFont(QFont("Times New Roman", 12))
        layout = QVBoxLayout()
        message = QLabel("Do you want to register with these credentials?", msg)
        layout.addWidget(message)

        msg_buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Yes | QDialogButtonBox.StandardButton.No, msg)
        msg_buttons.accepted.connect(msg.accept)
        msg_buttons.rejected.connect(msg.reject)
        check_url = "http://127.0.0.1:5000/check_user/"
        check_data = {'username': self.username.text()}
        check_response = requests.post(check_url, json=check_data)
        input_missing = False

        layout.addWidget(msg_buttons)
        msg.setLayout(layout)
        if check_response.json().get('exists'):
            warning_message = QLabel("Username already exists!", msg)
            layout.addWidget(warning_message)
            input_missing = True
        if self.username.text() == "":
            warning_message = QLabel("Please enter a username!", msg)
            layout.addWidget(warning_message)
            input_missing = True
        if self.password.text() == "":
            warning_message = QLabel("Please enter a password!", msg)
            layout.addWidget(warning_message)
            input_missing = True
        if input_missing:
            self.username.clear()
            self.password.clear()
            msg.exec()
            return



        if msg.exec() == QDialog.DialogCode.Accepted:
            username = self.username.text()
            password = self.password.text()
            self.send_registered_data(username, password)
            self.close()
        else:
            self.username.clear()
            self.password.clear()

    def closeEvent(self, event):
        self.close()





