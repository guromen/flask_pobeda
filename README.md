Простое веб-приложение на **Flask + SQLite + Bootstrap**, которое позволяет:
- Просматривать список пользователей
- Добавлять нового пользователя через форму
- По клику выводит информацию о пользователе

В проекте используются:

Flask — веб-фреймворк

Flask-SQLAlchemy — ORM для работы с базой данных

SQLAlchemy — ORM

Pydantic — валидация входящих данных

SQLite — встроенная база данных

Bootstrap — стилизация интерфейса

**Установка**
1. Клонировать проект

2. Создать виртуальное окружение

`python -m venv venv`

`source venv/bin/activate`
3. Установить зависимости

`pip install flask flask_sqlalchemy pydantic`

`pip install -r requirements.txt`
4. Создание базы данных
Открыть Python shell:

`from app import db`

`db.create_all()`

`exit()`
5. Запуск приложения
`python app.py`
Приложение будет доступно по адресу:
`http://127.0.0.1:5000`

Автор
Роман Гугузин