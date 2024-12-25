from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy.orm import sessionmaker
from alch import setup_database, Persons, Aliases, Emails

app = Flask(__name__)

engine = setup_database("sqlite:///database.sqlite")
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/')
def main():
    persons = session.query(Persons).all()
    return render_template('main.html', persons=persons)

@app.route('/add_person', methods=['GET', 'POST'])
def add_person():
    if request.method == 'POST':
        name = request.form['name']
        new_person = Persons(Name=name)
        session.add(new_person)
        session.commit()
        return redirect(url_for('main'))
    return render_template('add_person.html')

@app.route('/add_alias/<int:person_id>', methods=['GET', 'POST'])
def add_alias(person_id):
    if request.method == 'POST':
        alias = request.form['alias']
        new_alias = Aliases(Alias=alias, PersonId=person_id)
        session.add(new_alias)
        session.commit()
        return redirect(url_for('main'))
    return render_template('add_alias.html', person_id=person_id)

@app.route('/add_email/<int:person_id>', methods=['GET', 'POST'])
def add_email(person_id):
    if request.method == 'POST':
        subject = request.form['subject']
        body = request.form['body']
        new_email = Emails(SenderPersonId=person_id, MetadataSubject=subject, ExtractedBodyText=body)
        session.add(new_email)
        session.commit()
        return redirect(url_for('main'))
    return render_template('add_email.html', person_id=person_id)

@app.route('/edit_person/<int:person_id>', methods=['GET', 'POST'])
def edit_person(person_id):
    person = session.query(Persons).filter_by(Id=person_id).first()
    if request.method == 'POST':
        person.Name = request.form['name']
        session.commit()
        return redirect(url_for('main'))
    return render_template('edit_person.html', person=person)

@app.route('/edit_alias/<int:alias_id>', methods=['GET', 'POST'])
def edit_alias(alias_id):
    alias = session.query(Aliases).filter_by(Id=alias_id).first()
    if request.method == 'POST':
        alias.Alias = request.form['alias']
        session.commit()
        return redirect(url_for('main'))
    return render_template('edit_alias.html', alias=alias)

@app.route('/edit_email/<int:email_id>', methods=['GET', 'POST'])
def edit_email(email_id):
    email = session.query(Emails).filter_by(Id=email_id).first()
    if request.method == 'POST':
        email.MetadataSubject = request.form['subject']
        email.ExtractedBodyText = request.form['body']
        session.commit()
        return redirect(url_for('main'))
    return render_template('edit_email.html', email=email)

@app.route('/delete_person/<int:person_id>')
def delete_person(person_id):
    person = session.query(Persons).filter_by(Id=person_id).first()
    if person:
        session.delete(person)
        session.commit()
    return redirect(url_for('main'))

@app.route('/delete_alias/<int:alias_id>')
def delete_alias(alias_id):
    alias = session.query(Aliases).filter_by(Id=alias_id).first()
    if alias:
        session.delete(alias)
        session.commit()
    return redirect(url_for('main'))

@app.route('/delete_email/<int:email_id>')
def delete_email(email_id):
    email = session.query(Emails).filter_by(Id=email_id).first()
    if email:
        session.delete(email)
        session.commit()
    return redirect(url_for('main'))

if __name__ == '__main__':
    app.run(debug=True)