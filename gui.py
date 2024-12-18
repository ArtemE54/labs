import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from sqlalchemy import create_engine, func, desc
from sqlalchemy.orm import sessionmaker
from CRUD import setup_database, create_session, Persons, Aliases, Emails  # Подключаем модели из ORM

# Инициализация базы данных
engine = setup_database("sqlite:///database.sqlite")
session = create_session(engine)


# CRUD функции
def add_person(name):
    new_person = Persons(Name=name)
    session.add(new_person)
    session.commit()
    return new_person.Id


def add_email(sender_person_id, subject, body):
    new_email = Emails(
        SenderPersonId=sender_person_id,
        MetadataSubject=subject,
        ExtractedBodyText=body
    )
    session.add(new_email)
    session.commit()
    return new_email.Id


def update_person_name(person_id, new_name):
    person = session.query(Persons).filter_by(Id=person_id).first()
    if person:
        person.Name = new_name
        session.commit()
        return person
    return None


def search_person_by_name(name):
    persons = session.query(Persons).filter(Persons.Name.ilike(f"%{name}%")).all()
    return persons


def search_person_by_id(person_id):
    person = session.query(Persons).filter_by(Id=person_id).first()
    return person


def most_frequent_email_recipient():
    result = session.query(
        Emails.SenderPersonId,
        func.count(Emails.Id).label('email_count')
    ).group_by(Emails.SenderPersonId).order_by(desc('email_count')).first()

    if result:
        person_id, email_count = result
        person = session.query(Persons).filter_by(Id=person_id).first()
        return person, email_count
    return None