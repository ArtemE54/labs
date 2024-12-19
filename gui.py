import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QTextEdit)
from sqlalchemy import func, desc
from alch import setup_database, create_session
from CRUD import add_person, update_person_name, search_person_by_name, add_email, delete_person, delete_email, most_frequent_email_recipient, get_emails_by_person_id

# Инициализация базы данных
engine = setup_database("sqlite:///database.sqlite")
session = create_session(engine)

#ГЛавный класс приложения
class EmailManagerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Email Manager")
        layout = QVBoxLayout()

        # Добавление персоны
        self.person_name_input = QLineEdit(self)
        self.person_name_input.setPlaceholderText("Enter Person Name")
        layout.addWidget(self.person_name_input)

        add_person_btn = QPushButton("Add Person", self)
        add_person_btn.clicked.connect(self.add_person)
        layout.addWidget(add_person_btn)
