import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QGridLayout, QLineEdit, QPushButton, QMessageBox, QTextEdit, QLabel, QListWidget, QHBoxLayout, QDialog)
from PyQt5.QtGui import QFont
from sqlalchemy import func, desc
from alch import setup_database, create_session
from CRUD import add_person, update_person_name, search_person_by_name, add_email, delete_person, delete_email, most_frequent_email_recipient, get_emails_by_person_id, get_all_persons

# Инициализация базы данных
engine = setup_database("sqlite:///database.sqlite")
session = create_session(engine)

class ViewAllPersonsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("All Persons")
        self.setFont(QFont('Arial', 10))
        self.resize(400, 300)

        layout = QVBoxLayout()

        self.persons_list = QListWidget(self)
        self.persons_list.itemClicked.connect(self.on_person_selected)
        layout.addWidget(self.persons_list)

        self.selected_person_label = QLabel("Selected Person: None", self)
        layout.addWidget(self.selected_person_label)

        self.load_persons()

        self.setLayout(layout)

    def load_persons(self):
        self.persons_list.clear()
        persons = get_all_persons()
        for person in persons:
            self.persons_list.addItem(f"ID: {person.Id}, Name: {person.Name}")

    def on_person_selected(self, item):
        self.selected_person_label.setText(f"Selected Person: {item.text()}")

class ViewEmailsByPersonDialog(QDialog):
    def __init__(self, person_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Emails for Person ID: {person_id}")
        self.setFont(QFont('Arial', 10))
        self.resize(600, 400)

        layout = QVBoxLayout()

        self.emails_list = QListWidget(self)
        self.emails_list.itemClicked.connect(self.on_email_selected)
        layout.addWidget(self.emails_list)

        self.email_content = QTextEdit(self)
        self.email_content.setReadOnly(True)
        layout.addWidget(self.email_content)

        self.load_emails(person_id)

        self.setLayout(layout)

    def load_emails(self, person_id):
        self.emails_list.clear()
        emails = get_emails_by_person_id(person_id)
        for email in emails:
            self.emails_list.addItem(f"ID: {email.Id}, Subject: {email.MetadataSubject}")

    def on_email_selected(self, item):
        email_id = int(item.text().split(",")[0].split(":")[1].strip())
        emails = get_emails_by_person_id(email_id)
        if emails:
            email = emails[0]  # Assuming unique ID
            self.email_content.setText(f"Subject: {email.MetadataSubject}\nBody: {email.ExtractedBodyText}")

class EmailManagerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Email Manager")
        self.setFont(QFont('Arial', 10))

        main_layout = QVBoxLayout()
        grid_layout = QGridLayout()

        # Добавление персоны
        self.person_name_input = QLineEdit(self)
        self.person_name_input.setPlaceholderText("Enter Person Name")
        grid_layout.addWidget(QLabel("Add Person:"), 0, 0)
        grid_layout.addWidget(self.person_name_input, 0, 1)

        add_person_btn = QPushButton("Add Person", self)
        add_person_btn.clicked.connect(self.add_person)
        grid_layout.addWidget(add_person_btn, 0, 2)

        # Обновление имени персоны
        self.update_id_input = QLineEdit(self)
        self.update_id_input.setPlaceholderText("Enter Person ID to Update")
        grid_layout.addWidget(QLabel("Update Person:"), 1, 0)
        grid_layout.addWidget(self.update_id_input, 1, 1)

        self.new_name_input = QLineEdit(self)
        self.new_name_input.setPlaceholderText("Enter New Name")
        grid_layout.addWidget(self.new_name_input, 1, 2)

        update_person_btn = QPushButton("Update Person", self)
        update_person_btn.clicked.connect(self.update_person)
        grid_layout.addWidget(update_person_btn, 1, 3)

        # Удаление персоны
        self.delete_person_id_input = QLineEdit(self)
        self.delete_person_id_input.setPlaceholderText("Enter Person ID to Delete")
        grid_layout.addWidget(QLabel("Delete Person:"), 2, 0)
        grid_layout.addWidget(self.delete_person_id_input, 2, 1)

        delete_person_btn = QPushButton("Delete Person", self)
        delete_person_btn.clicked.connect(self.delete_person)
        grid_layout.addWidget(delete_person_btn, 2, 2)

        # Поиск персоны по имени
        self.search_name_input = QLineEdit(self)
        self.search_name_input.setPlaceholderText("Search Person by Name")
        grid_layout.addWidget(QLabel("Search Person:"), 3, 0)
        grid_layout.addWidget(self.search_name_input, 3, 1)

        search_person_btn = QPushButton("Search Person by Name", self)
        search_person_btn.clicked.connect(self.search_person)
        grid_layout.addWidget(search_person_btn, 3, 2)

        # Добавление емейла
        self.sender_id_input = QLineEdit(self)
        self.sender_id_input.setPlaceholderText("Enter Sender Person ID")
        grid_layout.addWidget(QLabel("Add Email:"), 4, 0)
        grid_layout.addWidget(self.sender_id_input, 4, 1)

        self.email_subject_input = QLineEdit(self)
        self.email_subject_input.setPlaceholderText("Enter Email Subject")
        grid_layout.addWidget(self.email_subject_input, 4, 2)

        self.email_body_input = QTextEdit(self)
        self.email_body_input.setPlaceholderText("Enter Email Body")
        grid_layout.addWidget(self.email_body_input, 4, 3)

        add_email_btn = QPushButton("Add Email", self)
        add_email_btn.clicked.connect(self.add_email)
        grid_layout.addWidget(add_email_btn, 4, 4)

        # Удаление письма
        self.delete_email_id_input = QLineEdit(self)
        self.delete_email_id_input.setPlaceholderText("Enter Email ID to Delete")
        grid_layout.addWidget(QLabel("Delete Email:"), 5, 0)
        grid_layout.addWidget(self.delete_email_id_input, 5, 1)

        delete_email_btn = QPushButton("Delete Email", self)
        delete_email_btn.clicked.connect(self.delete_email)
        grid_layout.addWidget(delete_email_btn, 5, 2)

        # Поиск письма по id персоны
        self.view_emails_id_input = QLineEdit(self)
        self.view_emails_id_input.setPlaceholderText("Enter Person ID to View Emails")
        grid_layout.addWidget(QLabel("View Emails:"), 6, 0)
        grid_layout.addWidget(self.view_emails_id_input, 6, 1)

        view_emails_btn = QPushButton("View Emails by Person ID", self)
        view_emails_btn.clicked.connect(self.view_emails_by_person_id)
        grid_layout.addWidget(view_emails_btn, 6, 2)

        # Частый получатель писем
        most_frequent_btn = QPushButton("Most Frequent Email Recipient", self)
        most_frequent_btn.clicked.connect(self.show_most_frequent_email_recipient)
        grid_layout.addWidget(most_frequent_btn, 7, 0, 1, 3)

        # Вывод всех персон
        view_all_persons_btn = QPushButton("View All Persons", self)
        view_all_persons_btn.clicked.connect(self.view_all_persons)
        grid_layout.addWidget(view_all_persons_btn, 8, 0, 1, 3)

        main_layout.addLayout(grid_layout)
        self.setLayout(main_layout)

    def add_person(self):
        name = self.person_name_input.text()
        if name:
            person_id = add_person(name)
            QMessageBox.information(self, "Success", f"Person added with ID: {person_id}")
            self.person_name_input.clear()
        else:
            QMessageBox.warning(self, "Input Error", "Please enter a name.")

    def update_person(self):
        person_id_text = self.update_id_input.text()
        new_name = self.new_name_input.text()

        if person_id_text.isdigit() and new_name:
            updated_person = update_person_name(int(person_id_text), new_name)
            if updated_person:
                QMessageBox.information(self, "Success", f"Person ID {person_id_text} updated.")
            else:
                QMessageBox.warning(self, "Error", f"Person ID {person_id_text} not found.")
            self.update_id_input.clear()
            self.new_name_input.clear()
        else:
            QMessageBox.warning(self, "Input Error", "Please enter valid ID and new name.")

    def delete_person(self):
        person_id_text = self.delete_person_id_input.text()
        if person_id_text.isdigit():
            success = delete_person(int(person_id_text))
            if success:
                QMessageBox.information(self, "Success", f"Person ID {person_id_text} deleted.")
            else:
                QMessageBox.warning(self, "Error", f"Person ID {person_id_text} not found.")
            self.delete_person_id_input.clear()
        else:
            QMessageBox.warning(self, "Input Error", "Please enter a valid Person ID.")

    def search_person(self):
        name = self.search_name_input.text()
        if name:
            persons = search_person_by_name(name)
            if persons:
                result_text = "\n".join([f"ID: {person.Id}, Name: {person.Name}" for person in persons])
                QMessageBox.information(self, "Search Result", result_text)
            else:
                QMessageBox.information(self, "Search Result", "No persons found.")
            self.search_name_input.clear()

    def add_email(self):
        sender_id_text = self.sender_id_input.text()
        subject = self.email_subject_input.text()
        body = self.email_body_input.toPlainText()
        if sender_id_text.isdigit() and subject and body:
            email_id = add_email(int(sender_id_text), subject, body)
            QMessageBox.information(self, "Success", f"Email added with ID: {email_id}")
            self.sender_id_input.clear()
            self.email_subject_input.clear()
            self.email_body_input.clear()
        else:
            QMessageBox.warning(self, "Input Error", "Please enter valid Sender ID, Subject, and Body.")

    def delete_email(self):
        email_id_text = self.delete_email_id_input.text()
        if email_id_text.isdigit():
            success = delete_email(int(email_id_text))
            if success:
                QMessageBox.information(self, "Success", f"Email ID {email_id_text} deleted.")
            else:
                QMessageBox.warning(self, "Error", f"Email ID {email_id_text} not found.")
            self.delete_email_id_input.clear()
        else:
            QMessageBox.warning(self, "Input Error", "Please enter a valid Email ID.")

    def view_emails_by_person_id(self):
        person_id_text = self.view_emails_id_input.text()
        if person_id_text.isdigit():
            dialog = ViewEmailsByPersonDialog(int(person_id_text), self)
            dialog.exec_()
            self.view_emails_id_input.clear()
        else:
            QMessageBox.warning(self, "Input Error", "Please enter a valid Person ID.")

    def show_most_frequent_email_recipient(self):
        result = most_frequent_email_recipient()
        if result:
            person, email_count = result
            QMessageBox.information(self,"Result",f"Most frequent email recipient: {person.Name} (ID: {person.Id}) with {email_count} emails sent")
        else:
            QMessageBox.information(self, "Result", "No emails found")

    def view_all_persons(self):
        dialog = ViewAllPersonsDialog(self)
        dialog.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = EmailManagerApp()
    ex.resize(800, 600)
    ex.show()
    sys.exit(app.exec_())