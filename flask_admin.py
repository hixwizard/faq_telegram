import os
from flask import Flask
from flask_admin import Admin
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# --- Настройки ---
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# --- Подключение к PostgreSQL ---
DB_URL = os.getenv(
    'DATABASE_URL', 'postgresql://user:password@localhost:5432/mydatabase'
)
engine = create_engine(DB_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# --- Админ-зона ---
admin = Admin(app, name='Admin Zone', template_mode='bootstrap3')

# Запуск Flask-приложения
if __name__ == '__main__':
    app.run(debug=True)
