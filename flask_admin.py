from flask import Flask
from flask_admin import Admin
from database import engine
from models import Base

# --- Настройки ---
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# --- Инициализация базы данных ---
Base.metadata.create_all(bind=engine)

# --- Админ-зона ---
admin = Admin(app, name='Admin Zone', template_mode='bootstrap3')

# Запуск Flask-приложения
if __name__ == '__main__':
    app.run(debug=True)
