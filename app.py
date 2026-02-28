from flask import Flask, render_template, url_for, request, jsonify, Response
from  flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, constr, validator, ValidationError
import json


app = Flask('app')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_db.db'
db = SQLAlchemy(app)


class Users(db.Model):
    """" Создание модели"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f'<User>, {self.id!r}'


class Validator(BaseModel):
    """"Класс-валидатор на основе BaseModel, pydantic"""
    name: constr(min_length=1)
    email: constr(min_length=1)

    @validator('email')
    def validate_email(cls, value):
        """Простейшая проверка email"""
        if '@' not in value:
            raise HttpError(400,'Field expect email')
        return value

def validate(input_data, Class_validator):
    """Валидация данных"""
    try:
        item = Class_validator(**input_data)
        return  item.dict()
    except ValidationError as er:
        messages = set()
        for err in er.errors():
            messages.add(err["msg"])
        error = [{"message": msg} for msg in messages]
        raise HttpError(400, error)

class HttpError(Exception):
    """"Кастомный класс обработки ошибок"""
    def __init__(self, status_code, description):
        self.status_code = status_code
        self.description = description


@app.errorhandler(404)
def handle_404(e):
    raise HttpError(404, "User not found")


@app.errorhandler(HttpError) #На базе нашего класса HttpError
def error_handler(error):
    response = jsonify({'status': 'error', 'description':error.description})
    response.status_code = error.status_code
    return  response


@app.route('/')
def index():
    """"Главная"""
    return render_template('index.html')


@app.route('/users')
def users():
    """"Все юхеры"""
    users = Users.query.order_by(Users.id.desc()).all()
    return  jsonify([{'id':user.id, 'name':user.name, 'email': user.email} for user in users]) # выводит json всех


@app.route('/users/<id>')
def user_detail(id):
    """"Получение юзера по id"""
    try:
        id = int(id)
    except:
        raise HttpError(400, "User's Id not found")
    user = Users.query.get(id)
    if not user:
        raise HttpError(404, 'User not found')
    return jsonify([{'id': user.id, 'name': user.name, 'email': user.email}])  # выводит json юзера по id


@app.route('/users/<int:id>/delete')
def user_delete(id):
    """"Удаление юзура"""
    user = Users.query.get_or_404(id)
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'status':'ok'})
    except:
        raise HttpError(400,'Deleting error')


@app.route('/create-user', methods=['POST'])
def create_user():
    """"Создание юзера"""
    if request.method == 'POST':
        data = {**request.form}
        data = validate(data, Validator)
        user=Users(**data)
        try:
            db.session.add(user)
            db.session.commit()
            return jsonify({'status':'ok'})
        except IntegrityError as er:
            raise HttpError(409, 'User already exist')


@app.route('/about')
def about():
    data = {
        "app": "Тестовое задание Победа",
        "version": "1.0",
        "author": "Гугузин Роман"
    }
    return Response(
        json.dumps(data, ensure_ascii=False),
        content_type='application/json; charset=utf-8'
    )

if __name__ == '__main__':
    app.run(debug=True)