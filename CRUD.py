from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alch import setup_database, create_session, Persons, Aliases  # Подключаем модели из ORM

# Инициализация базы данных
engine = setup_database("sqlite:///C:\\Users\\Eroha\\PycharmProjects\\pythonProject\\pipon\\database.sqlite")
session = create_session(engine)

# CREATE (Создание)
def add_person(name):
    new_person = Persons(Name=name)
    session.add(new_person)
    session.commit()
    print(f"Person '{name}' added with ID: {new_person.Id}")
    return new_person.Id

def add_alias_id(id, person_id):
    new_alias_id = Aliases(Id=id, PersonId=person_id)
    session.add(new_alias_id)
    session.commit()
    print(f"Alias '{id}' added with ID: {new_alias_id.Id}")
    return new_alias_id.Id

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
    persons = session.query(Persons).all()
    for person in persons:
        print(f"Person ID: {person.Id}, Name: {person.Name}")
    return persons

def aliases_by_person(person_id):
    aliases = session.query(Aliases).filter_by(PersonId=person_id).all()
    print(f"Aliases for Person ID {person_id}:")
    for alias in aliases:
        print(f"- {alias.Alias}")
    return aliases

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

# Примеры использования
if __name__ == "__main__":
    # Создание
    person_id = add_person("John Doe")
    alias_id = add_alias_id("JD", person_id)

    # Чтение
    get_person_by_id(person_id)
    get_all_persons()
    aliases_by_person(person_id)

    # Обновление
    update_person_name(person_id, "John Doe")
    update_alias(alias_id, "JohnD")

    # Находим запись по Id
    alias = session.query(Aliases).filter_by(Id=alias_id).first()
    if alias:
     # Удаляем запись
        session.delete(alias)
        session.commit()
        print(f"Alias with ID {alias_id} deleted.")