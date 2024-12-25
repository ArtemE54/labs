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

        # Обновление имени персоны
        self.update_id_input = QLineEdit(self)
        self.update_id_input.setPlaceholderText("Enter Person ID to Update")
        layout.addWidget(self.update_id_input)

        self.new_name_input = QLineEdit(self)
        self.new_name_input.setPlaceholderText("Enter New Name")
        layout.addWidget(self.new_name_input)

        update_person_btn = QPushButton("Update Person", self)
        update_person_btn.clicked.connect(self.update_person)
        layout.addWidget(update_person_btn)

        # Удаление персоны
        self.delete_person_id_input = QLineEdit(self)
        self.delete_person_id_input.setPlaceholderText("Enter Person ID to Delete")
        layout.addWidget(self.delete_person_id_input)

        delete_person_btn = QPushButton("Delete Person", self)
        delete_person_btn.clicked.connect(self.delete_person)
        layout.addWidget(delete_person_btn)

        # Поиск персоны по имени
        self.search_name_input = QLineEdit(self)
        self.search_name_input.setPlaceholderText("Search Person by Name")
        layout.addWidget(self.search_name_input)

        search_person_btn = QPushButton("Search Person by Name", self)
        search_person_btn.clicked.connect(self.search_person)
        layout.addWidget(search_person_btn)

        # Добавление емейла
        self.sender_id_input = QLineEdit(self)
        self.sender_id_input.setPlaceholderText("Enter Sender Person ID")
        layout.addWidget(self.sender_id_input)

        self.email_subject_input = QLineEdit(self)
        self.email_subject_input.setPlaceholderText("Enter Email Subject")
        layout.addWidget(self.email_subject_input)

        self.email_body_input = QTextEdit(self)
        self.email_body_input.setPlaceholderText("Enter Email Body")
        layout.addWidget(self.email_body_input)

        add_email_btn = QPushButton("Add Email", self)
        add_email_btn.clicked.connect(self.add_email)
        layout.addWidget(add_email_btn)

        # Удаление письма
        self.delete_email_id_input = QLineEdit(self)
        self.delete_email_id_input.setPlaceholderText("Enter Email ID to Delete")
        layout.addWidget(self.delete_email_id_input)

        delete_email_btn = QPushButton("Delete Email", self)
        delete_email_btn.clicked.connect(self.delete_email)
        layout.addWidget(delete_email_btn)

        # Поиск письма по id персоны
        self.view_emails_id_input = QLineEdit(self)
        self.view_emails_id_input.setPlaceholderText("Enter Person ID to View Emails")
        layout.addWidget(self.view_emails_id_input)

        view_emails_btn = QPushButton("View Emails by Person ID", self)
        view_emails_btn.clicked.connect(self.view_emails_by_person_id)
        layout.addWidget(view_emails_btn)

        # Частый получатель писем
        most_frequent_btn = QPushButton("Most Frequent Email Recipient", self)
        most_frequent_btn.clicked.connect(self.show_most_frequent_email_recipient)
        layout.addWidget(most_frequent_btn)

        self.setLayout(layout)

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
            emails = get_emails_by_person_id(int(person_id_text))
            if emails:
                result_text = "\n".join([f"Subject: {email.MetadataSubject}\nBody: {email.ExtractedBodyText}\n" for email in emails])
                QMessageBox.information(self, "Emails", result_text)
            else:
                QMessageBox.information(self, "Emails", "No emails found for this person.")
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = EmailManagerApp()
    ex.resize(800, 600)
    ex.show()
    sys.exit(app.exec_())
