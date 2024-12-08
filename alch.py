from flask_sqlalchemy.session import Session
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Базовый класс для всех моделей
Base = declarative_base()

class Persons(Base):
    __tablename__ = 'Persons'
    Id = Column(Integer, primary_key=True)
    Name = Column(String)

    # Связь один ко многим с таблицей Aliases
    aliases = relationship('Aliases', back_populates='person')

class Aliases(Base):
    __tablename__ = 'Aliases'
    Id = Column(Integer, primary_key=True)
    Alias = Column(String)
    PersonId = Column(Integer, ForeignKey('Persons.Id'), primary_key=True)

    # Связь с таблицей Persons
    person = relationship('Persons', back_populates='aliases')

def setup_database(database_path="sqlite:///database.sqlite"):
    engine = create_engine(database_path)
    Base.metadata.create_all(engine)
    return engine

# Создание сессии
def create_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()

engine = setup_database("sqlite:///database.sqlite")
session = create_session(engine)

# Добавление новой персоны
new_person = Persons(Name="Josh Sque")
session.add(new_person)
session.commit()
print(f"Added person with ID: {new_person.Id}")

# Добавление нового алиаса
new_alias = Aliases(Alias="Banan", PersonId=new_person.Id, Id = 1000000000018)
session.add(new_alias)
session.commit()
print(f"Added alias with ID: {new_alias.Id}")

# Получение алиасов персоны
person_id = new_person.Id
person = session.query(Persons).filter_by(Id=person_id).first()

if person:
    print(f"Aliases for {person.Name}: {[alias.Alias for alias in person.aliases]}")

# Удаление персоны & алиаса
person_id = new_person.Id
person = session.query(Persons).filter_by(Id=person_id).first()

if person:
    session.query(Persons).delete()
    session.commit()
    print(f"Deleted person with ID {new_person.Id}")

new_alias = new_alias.Id
alias = session.query(Aliases).filter_by(Id=new_alias).first()

if alias:
    session.query(Aliases).delete()
    session.commit()
    print(f"Deleted alias with ID {alias.Id}")
