from flask import Flask, request, render_template, redirect, url_for
from alch import session, Aliases, Emails
import os
from flask import Flask, render_template
from CRUD import (
    add_person, add_alias, add_email,
    get_person_by_id, get_all_persons, aliases_by_person, emails_by_person,
    update_person_name, update_alias, update_email,
    delete_person, delete_alias, delete_email,
    search_person_by_name, search_email_by_subject,
)


# Инициализация Flask-приложения
app = Flask(__name__, template_folder=os.path.abspath("templates"))

# Главная страница
@app.route('/')
def main():
    # Отображение главной страницы
    return render_template('main.html', page='home')

# CREATE operations (Операции создания)

# Добавление новой персоны
@app.route('/add_person', methods=['GET', 'POST'])
def create_person():
    if request.method == 'POST':
        name = request.form.get('name')  # Получаем имя из формы
        if name:
            person_id = add_person(name)  # Добавляем персону в базу данных
            return redirect(url_for('view_person', person_id=person_id))  # Перенаправляем на страницу персоны
    return render_template('main.html', page='add_person')  # Отображение формы добавления персоны

# Добавление нового алиаса
@app.route('/add_alias', methods=['GET', 'POST'])
def create_alias():
    if request.method == 'POST':
        alias = request.form.get('alias')
        person_id = request.form.get('person_id')  # Получаем ID персоны из формы
        if alias and person_id:
            add_alias(alias, int(person_id))  # Добавляем алиас в базу данных
            return redirect(url_for('view_person', person_id=person_id))  # Перенаправляем на страницу персоны
    return render_template('main.html', page='add_alias')  # Отображение формы добавления алиаса

# Добавление нового письма
@app.route('/add_email', methods=['GET', 'POST'])
def create_email():
    if request.method == 'POST':
        sender_person_id = request.form.get('sender_person_id')  # Получаем ID отправителя из формы
        subject = request.form.get('subject')  # Получаем тему письма из формы
        body = request.form.get('body')  # Получаем тело письма из формы
        if sender_person_id and subject and body:
            add_email(int(sender_person_id), subject, body)  # Добавляем письмо в базу данных
            return redirect(url_for('view_person', person_id=sender_person_id))  # Перенаправляем на страницу персоны
    return render_template('main.html', page='add_email')  # Отображение формы добавления письма

# READ operations (Операции чтения)

# Просмотр информации о персоне
@app.route('/person/<int:person_id>')
def view_person(person_id):
    person = get_person_by_id(person_id)  # Получаем персону по ID
    aliases = aliases_by_person(person_id)  # Получаем алиасы персоны
    emails = emails_by_person(person_id)  # Получаем письма персоны
    return render_template('main.html', page='view_person', person=person, aliases=aliases, emails=emails)

# Просмотр всех персон
@app.route('/persons')
def view_all_persons():
    persons = get_all_persons()  # Получаем всех персон из базы данных
    return render_template('main.html', page='view_all_persons', persons=persons)

# UPDATE operations (Операции обновления)

# Обновление имени персоны
@app.route('/update_person/<int:person_id>', methods=['GET', 'POST'])
def update_person(person_id):
    if request.method == 'POST':
        new_name = request.form.get('name')  # Получаем новое имя из формы
        if new_name:
            update_person_name(person_id, new_name)  # Обновляем имя персоны
            return redirect(url_for('view_person', person_id=person_id))  # Перенаправляем на страницу персоны
    person = get_person_by_id(person_id)  # Получаем персону по ID
    return render_template('main.html', page='update_person', person=person)  # Отображение формы обновления персоны

# Обновление алиаса
@app.route('/update_alias/<int:alias_id>', methods=['GET', 'POST'])
def update_alias_route(alias_id):
    if request.method == 'POST':
        new_alias = request.form.get('alias')  # Получаем новый алиас из формы
        if new_alias:
            update_alias(alias_id, new_alias)  # Обновляем алиас
            alias = session.query(Aliases).filter_by(Id=alias_id).first()  # Получаем алиас по ID
            return redirect(url_for('view_person', person_id=alias.PersonId))  # Перенаправляем на страницу персоны
    alias = session.query(Aliases).filter_by(Id=alias_id).first()  # Получаем алиас по ID
    return render_template('main.html', page='update_alias', alias=alias)  # Отображение формы обновления алиаса

# Обновление письма
@app.route('/update_email/<int:email_id>', methods=['GET', 'POST'])
def update_email_route(email_id):
    if request.method == 'POST':
        new_subject = request.form.get('subject')  # Получаем новую тему из формы
        new_body = request.form.get('body')  # Получаем новое тело письма из формы
        if new_subject and new_body:
            update_email(email_id, new_subject, new_body)  # Обновляем письмо
            email = session.query(Emails).filter_by(Id=email_id).first()  # Получаем письмо по ID
            return redirect(url_for('view_person', person_id=email.SenderPersonId))  # Перенаправляем на страницу персоны
    email = session.query(Emails).filter_by(Id=email_id).first()  # Получаем письмо по ID
    return render_template('main.html', page='update_email', email=email)  # Отображение формы обновления письма

# DELETE operations (Операции удаления)

# Удаление персоны
@app.route('/delete_person/<int:person_id>')
def delete_person_route(person_id):
    delete_person(person_id)  # Удаляем персону по ID
    return redirect(url_for('view_all_persons'))  # Перенаправляем на страницу всех персон

# Удаление алиаса
@app.route('/delete_alias/<int:alias_id>')
def delete_alias_route(alias_id):
    alias = session.query(Aliases).filter_by(Id=alias_id).first()  # Получаем алиас по ID
    person_id = alias.PersonId  # Получаем ID персоны, связанной с алиасом
    delete_alias(alias_id)  # Удаляем алиас
    return redirect(url_for('view_person', person_id=person_id))  # Перенаправляем на страницу персоны

# Удаление письма
@app.route('/delete_email/<int:email_id>')
def delete_email_route(email_id):
    email = session.query(Emails).filter_by(Id=email_id).first()  # Получаем письмо по ID
    person_id = email.SenderPersonId  # Получаем ID персоны, связанной с письмом
    delete_email(email_id)  # Удаляем письмо
    return redirect(url_for('view_person', person_id=person_id))  # Перенаправляем на страницу персоны

# SEARCH operations (Операции поиска)

# Поиск персоны по имени
@app.route('/search_person', methods=['GET', 'POST'])
def search_person_route():
    if request.method == 'POST':
        name = request.form.get('name')  # Получаем имя из формы
        if not name:
            return render_template('main.html', page='search_person', error="Please enter a name to search.")  # Ошибка, если имя не введено

        persons = search_person_by_name(name)  # Ищем персону по имени
        return render_template('main.html', page='search_person', persons=persons, search_query=name)  # Отображение результатов поиска

    return render_template('main.html', page='search_person')  # Отображение формы поиска

# Поиск письма по теме
@app.route('/search_email', methods=['GET', 'POST'])
def search_email_route():
    if request.method == 'POST':
        subject = request.form.get('subject')  # Получаем тему из формы
        emails = search_email_by_subject(subject)  # Ищем письмо по теме
        return render_template('main.html', page='search_email', emails=emails, search_query=subject)  # Отображение результатов поиска
    return render_template('main.html', page='search_email')  # Отображение формы поиска

# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True)  # Запуск Flask-приложения в режиме отладки