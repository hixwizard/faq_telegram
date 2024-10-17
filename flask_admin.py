from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from telegram_bot_code import Base, User, Application  # импортируйте ваши модели

# --- Настройки ---
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Установите секретный ключ

# --- Подключение к PostgreSQL ---
DB_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/mydatabase')
engine = create_engine(DB_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# --- Админ-зона ---
admin = Admin(app, name='Admin Zone', template_mode='bootstrap3')

# Добавляем модели в админ-панель
admin.add_view(ModelView(User, session))
admin.add_view(ModelView(Application, session))

# Запуск Flask-приложения
if __name__ == '__main__':
    app.run(debug=True)
