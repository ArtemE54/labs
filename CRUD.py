from sqlalchemy import create_engine, func, desc
from sqlalchemy.orm import sessionmaker
from alch import setup_database, create_session, Persons, Aliases, Emails  # Подключаем модели из ORM

# Инициализация базы данных
engine = setup_database("sqlite:///database.sqlite")
session = create_session(engine)

# CREATE (Создание)
def add_person(name):
    new_person = Persons(Name=name)
    session.add(new_person)
    session.commit()
    print(f"Person '{name}' added with ID: {new_person.Id}")
    return new_person.Id

def add_alias(alias, person_id):
    new_alias = Aliases(Alias=alias, PersonId=person_id)  # Убираем явное указание Id
    session.add(new_alias)
    session.commit()
    print(f"Alias '{alias}' added for Person ID: {person_id}")
    return new_alias.Id

def add_email(sender_person_id, subject, body):
    new_email = Emails(
        SenderPersonId=sender_person_id,
        MetadataSubject=subject,
        ExtractedBodyText=body
    )
    session.add(new_email)
    session.commit()
    print(f"Email added for Person ID: {sender_person_id}")
    return new_email.Id

# READ (Чтение)
def get_person_by_id(person_id):
    person = session.query(Persons).filter_by(Id=person_id).first()
    if person:
        print(f"Person: {person.Name}")
        return person
    else:
        print(f"Person with ID {person_id} not found.")
        return None

def get_all_persons():
    persons = session.query(Persons).limit(50).all()
    for person in persons:
        print(f"Person ID: {person.Id}, Name: {person.Name}")
    return persons

def aliases_by_person(person_id):
    aliases = session.query(Aliases).filter_by(PersonId=person_id).all()
    print(f"Aliases for Person ID {person_id}:")
    for alias in aliases:
        print(f"- {alias.Alias}")
    return aliases

def emails_by_person(person_id):
    emails = session.query(Emails).filter_by(SenderPersonId=person_id).all()
    print(f"Emails for Person ID {person_id}:")
    for email in emails:
        print(f"- Subject: {email.MetadataSubject}, Body: {email.ExtractedBodyText}")
    return emails

def most_frequent_email_recipient():
    result = session.query(
        Emails.SenderPersonId,
        func.count(Emails.Id).label('email_count')
    ).group_by(Emails.SenderPersonId).order_by(desc('email_count')).first()

    if result:
        person_id, email_count = result
        person = session.query(Persons).filter_by(Id=person_id).first()
        if person:
            print(f"Most frequent email recipient: {person.Name} (ID: {person.Id}) with {email_count} emails sent.")
            return person, email_count
    else:
        print("No emails found.")
        return None


# UPDATE (Обновление)
def update_person_name(person_id, new_name):
    person = session.query(Persons).filter_by(Id=person_id).first()
    if person:
        person.Name = new_name
        session.commit()
        print(f"Person ID {person_id} updated to '{new_name}'")
        return person
    else:
        print(f"Person with ID {person_id} not found.")
        return None

def update_alias(alias_id, new_alias):
    alias = session.query(Aliases).filter_by(Id=alias_id).first()
    if alias:
        alias.Alias = new_alias
        session.commit()
        print(f"Alias ID {alias_id} updated to '{new_alias}'")
        return alias
    else:
        print(f"Alias with ID {alias_id} not found.")
        return None

def update_email(email_id, new_subject, new_body):
    email = session.query(Emails).filter_by(Id=email_id).first()
    if email:
        email.MetadataSubject = new_subject
        email.ExtractedBodyText = new_body
        session.commit()
        print(f"Email ID {email_id} updated.")
        return email
    else:
        print(f"Email with ID {email_id} not found.")
        return None

# SEARCH (Поиск)
def search_person_by_name(name):
    persons = session.query(Persons).filter(Persons.Name.ilike(f"%{name}%")).all()
    if persons:
        print(f"Found persons with name '{name}':")
        for person in persons:
            print(f"Person ID: {person.Id}, Name: {person.Name}")
        return persons
    else:
        print(f"No persons found with name '{name}'.")
        return None

def search_alias_by_alias(alias):
    aliases = session.query(Aliases).filter(Aliases.Alias.ilike(f"%{alias}%")).all()
    if aliases:
        print(f"Found aliases with alias '{alias}':")
        for alias in aliases:
            print(f"Alias ID: {alias.Id}, Alias: {alias.Alias}, Person ID: {alias.PersonId}")
        return aliases
    else:
        print(f"No aliases found with alias '{alias}'.")
        return None

def search_email_by_subject(subject):
    emails = session.query(Emails).filter(Emails.MetadataSubject.ilike(f"%{subject}%")).all()
    if emails:
        print(f"Found emails with subject '{subject}':")
        for email in emails:
            print(f"Email ID: {email.Id}, Subject: {email.MetadataSubject}, Body: {email.ExtractedBodyText}")
        return emails
    else:
        print(f"No emails found with subject '{subject}'.")
        return None

# DELETE (Удаление)
def delete_person(person_id):
    person = session.query(Persons).filter_by(Id=person_id).first()
    if person:
        session.delete(person)
        session.commit()
        print(f"Person ID {person_id} deleted.")
    else:
        print(f"Person with ID {person_id} not found.")

def delete_alias(alias_id):
    alias = session.query(Aliases).filter_by(Id=alias_id).first()
    if alias:
        session.delete(alias)
        session.commit()
        print(f"Alias ID {alias_id} deleted.")
    else:
        print(f"Alias with ID {alias_id} not found.")

def delete_email(email_id):
    email = session.query(Emails).filter_by(Id=email_id).first()
    if email:
        session.delete(email)
        session.commit()
        print(f"Email ID {email_id} deleted.")
    else:
        print(f"Email with ID {email_id} not found.")

# Примеры использования
if __name__ == "__main__":
    # Создание
    person_id = add_person("Jackie Chan")
    alias_id = add_alias("Jackie", person_id)
    email_id = add_email(person_id, "Hello", "My names is a")

    # Чтение
    get_person_by_id(person_id)
    get_all_persons()
    aliases_by_person(person_id)
    emails_by_person(person_id)
    most_frequent_email_recipient()

    # Обновление
    update_person_name(person_id, "Jackie Sui")
    update_alias(alias_id, "JackieS")
    update_email(email_id, "aBOBA", "Aboba")

    # Поиск
    search_person_by_name("Jackie")
    search_alias_by_alias("Jackie")
    search_email_by_subject("Hello")

    # Удаление
    delete_email(email_id)
    delete_alias(alias_id)
    delete_person(person_id)





