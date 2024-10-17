import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from sqlalchemy import create_engine, Column, String, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import IntegrityError
import enum
import os

# --- Настройки ---
BOT_TOKEN = 'YOUR_BOT_TOKEN'  # Замените на ваш BOT_TOKEN

# --- Подключение к PostgreSQL ---
DB_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/mydatabase')  # Укажите корректный URL для PostgreSQL
engine = create_engine(DB_URL, echo=True)
Base = declarative_base()

# --- Модель пользователя ---
class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True)  # Telegram ID пользователя тип str
    name = Column(String, unique=True)
    phone = Column(String)
    email = Column(String)

# --- Enum для статуса заявки ---
class ApplicationStatus(enum.Enum):
    open = 'Открыта'
    in_progress = 'В работе'
    closed = 'Закрыта'

# --- Модель заявки ---
class Application(Base):
    __tablename__ = 'applications'

    id = Column(String, primary_key=True)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.open)
    closed_by = Column(String, ForeignKey('users.name'))  # Внешний ключ на поле name из таблицы users
    closed_by_user = relationship('User', backref='closed_applications')

# --- Создание таблиц ---
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# --- Хранилище данных пользователей во время ввода ---
user_data = {}

# --- Логирование ---
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Обработчик команды /start ---
async def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("FAQ", callback_data='faq')],
        [InlineKeyboardButton("Сохранить данные", callback_data='save_data')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Добро пожаловать! Выберите опцию:', reply_markup=reply_markup)

# --- Обработчик нажатий кнопок ---
async def button(update: Update, context):
    query = update.callback_query
    await query.answer()

    if query.data == 'faq':
        faq_buttons = [
            [InlineKeyboardButton("Контактная информация", callback_data='contact_info')],
            [InlineKeyboardButton("Адрес", callback_data='address')],
            [InlineKeyboardButton("Назад", callback_data='start')]
        ]
        await query.edit_message_text(text='FAQ:', reply_markup=InlineKeyboardMarkup(faq_buttons))
    elif query.data == 'contact_info':
        await query.edit_message_text(text='Наша контактная информация:\nТелефон: +123456789')
    elif query.data == 'address':
        await query.edit_message_text(text='Наш адрес:\nул. Примерная, дом 1.')
    elif query.data == 'start':
        start_buttons = [
            [InlineKeyboardButton("FAQ", callback_data='faq')],
            [InlineKeyboardButton("Сохранить данные", callback_data='save_data')]
        ]
        await query.edit_message_text(text='Добро пожаловать! Выберите опцию:', reply_markup=InlineKeyboardMarkup(start_buttons))
    elif query.data == 'save_data':
        user_data[query.from_user.id] = {}
        await query.message.reply_text('Введите ваше имя:')

# --- Обработчик сообщений для ввода данных ---
async def handle_user_input(update: Update, context):
    sender_id = update.message.from_user.id
    if sender_id in user_data:
        current_data = user_data[sender_id]
        if 'name' not in current_data:
            current_data['name'] = update.message.text
            await update.message.reply_text('Введите ваш номер телефона:')
        elif 'phone' not in current_data:
            current_data['phone'] = update.message.text
            await update.message.reply_text('Введите ваш email:')
        elif 'email' not in current_data:
            current_data['email'] = update.message.text
            # Сохранение данных в базу
            new_user = User(
                id=str(sender_id),
                name=current_data['name'],
                phone=current_data['phone'],
                email=current_data['email']
            )
            try:
                session.add(new_user)
                session.commit()
                await update.message.reply_text('Ваши данные успешно сохранены!')
            except IntegrityError:
                session.rollback()
                await update.message.reply_text('Произошла ошибка при сохранении данных. Возможно, вы уже зарегистрированы.')
            finally:
                del user_data[sender_id]

# --- Запуск бота ---
def main():
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()

    # Регистрация обработчиков команд
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_input))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
