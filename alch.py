from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, Text
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Base class for all models
Base = declarative_base()

class Persons(Base):
    __tablename__ = 'Persons'
    Id = Column(Integer, primary_key=True)
    Name = Column(String)

    # One-to-many relationship with Aliases and Emails tables
    aliases = relationship('Aliases', back_populates='person', cascade="all, delete-orphan")
    emails = relationship('Emails', back_populates='sender', cascade="all, delete-orphan")

class Aliases(Base):
    __tablename__ = 'Aliases'
    Id = Column(Integer, primary_key=True, autoincrement=True)  # Ensure this is the only primary key
    Alias = Column(String)
    PersonId = Column(Integer, ForeignKey('Persons.Id'))

    # Relationship with Persons table
    person = relationship('Persons', back_populates='aliases')

class Emails(Base):
    __tablename__ = 'Emails'
    Id = Column(Integer, primary_key=True)
    DocNumber = Column(String)
    MetadataSubject = Column(String)
    MetadataTo = Column(String)
    MetadataFrom = Column(String)
    SenderPersonId = Column(Integer, ForeignKey('Persons.Id'))
    MetadataDateSent = Column(String)
    MetadataDateReleased = Column(String)
    MetadataPdfLink = Column(String)
    MetadataCaseNumber = Column(String)
    MetadataDocumentClass = Column(String)
    ExtractedSubject = Column(String)
    ExtractedTo = Column(String)
    ExtractedFrom = Column(String)
    ExtractedCc = Column(String)
    ExtractedDateSent = Column(String)
    ExtractedCaseNumber = Column(String)
    ExtractedDocNumber = Column(String)
    ExtractedDateReleased = Column(String)
    ExtractedReleaseInPartOrFull = Column(String)
    ExtractedBodyText = Column(Text)

    # Relationship with Persons table
    sender = relationship('Persons', back_populates='emails')

def setup_database(database_path="sqlite:///database.sqlite"):
    engine = create_engine(database_path)
    Base.metadata.create_all(engine)  # Create tables in the database
    return engine

# Create a session
def create_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()

engine = setup_database("sqlite:///database.sqlite")
session = create_session(engine)

# Adding a new person
new_person = Persons(Name="Josh Sque")
session.add(new_person)
session.commit()
print(f"Added person with ID: {new_person.Id}")

# Adding a new email
new_email = Emails(
    DocNumber="12345",
    MetadataSubject="Test Subject",
    MetadataTo="test@example.com",
    MetadataFrom="sender@example.com",
    SenderPersonId=new_person.Id,
    MetadataDateSent="2023-10-01",
    MetadataDateReleased="2023-10-02",
    MetadataPdfLink="http://example.com/pdf",
    MetadataCaseNumber="CASE123",
    MetadataDocumentClass="ClassA",
    ExtractedSubject="Extracted Subject",
    ExtractedTo="extracted@example.com",
    ExtractedFrom="extracted_sender@example.com",
    ExtractedCc="cc@example.com",
    ExtractedDateSent="2023-10-01",
    ExtractedCaseNumber="CASE123",
    ExtractedDocNumber="12345",
    ExtractedDateReleased="2023-10-02",
    ExtractedReleaseInPartOrFull="Full",
    ExtractedBodyText="This is the body of the email."
)

session.add(new_email)
session.commit()
print(f"Added email with ID: {new_email.Id}")

# Retrieving aliases and emails for the person
person_id = new_person.Id
person = session.query(Persons).filter_by(Id=person_id).first()

if person:
    print(f"Aliases for {person.Name}: {[alias.Alias for alias in person.aliases]}")
    print(f"Emails sent by {person.Name}: {[email.MetadataSubject for email in person.emails]}")

# Deleting the person
if person:
    session.delete(person)  # This will also delete related aliases and emails due to cascade option
    session.commit()
    print(f"Deleted person with ID {new_person.Id}")
