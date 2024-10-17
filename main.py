import asyncio
from telethon import TelegramClient, events, Button
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

# --- Настройки ---
API_ID = 'YOUR_API_ID'          # Замените на ваш API_ID
API_HASH = 'YOUR_API_HASH'      # Замените на ваш API_HASH
BOT_TOKEN = 'YOUR_BOT_TOKEN'    # Замените на ваш BOT_TOKEN

# --- Настройка базы данных ---
engine = create_engine('sqlite:///users.db', echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True)  # Telegram ID пользователя тип str
    name = Column(String)
    phone = Column(String)
    email = Column(String)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# --- Инициализация клиента ---
client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# --- Хранилище данных пользователей во время ввода ---
user_data = {}

# --- Обработчик команды /start ---
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    buttons = [
        [Button.inline("FAQ", b'faq')],
        [Button.inline("Сохранить данные", b'save_data')]
    ]
    await event.respond('Добро пожаловать! Выберите опцию:', buttons=buttons)

# --- Обработчик нажатий кнопок ---
@client.on(events.CallbackQuery)
async def callback_handler(event):
    data = event.data.decode('utf-8')
    if data == 'faq':
        faq_buttons = [
            [Button.inline("Контактная информация", b'contact_info')],
            [Button.inline("Адрес", b'address')],
            [Button.inline("Назад", b'start')]
        ]
        await event.edit('FAQ:', buttons=faq_buttons)
    elif data == 'contact_info':
        await event.edit('Наша контактная информация:\nТелефон: +123456789')
    elif data == 'address':
        await event.edit('Наш адрес:\nул. Примерная, дом 1.')
    elif data == 'start':
        buttons = [
            [Button.inline("FAQ", b'faq')],
            [Button.inline("Сохранить данные", b'save_data')]
        ]
        await event.edit('Добро пожаловать! Выберите опцию:', buttons=buttons)
    elif data == 'save_data':
        user_data[event.sender_id] = {}
        await event.respond('Введите ваше имя:')

# --- Обработчик сообщений для ввода данных ---
@client.on(events.NewMessage)
async def handle_user_input(event):
    sender_id = event.sender_id
    if sender_id in user_data:
        current_data = user_data[sender_id]
        if 'name' not in current_data:
            current_data['name'] = event.text
            await event.respond('Введите ваш номер телефона:')
        elif 'phone' not in current_data:
            current_data['phone'] = event.text
            await event.respond('Введите ваш email:')
        elif 'email' not in current_data:
            current_data['email'] = event.text
            # Сохранение данных в базу
            new_user = User(
                id=sender_id,
                name=current_data['name'],
                phone=current_data['phone'],
                email=current_data['email']
            )
            try:
                session.add(new_user)
                session.commit()
                await event.respond('Ваши данные успешно сохранены!')
            except IntegrityError:
                session.rollback()
                await event.respond('Произошла ошибка при сохранении данных. Возможно, вы уже зарегистрированы.')
            finally:
                del user_data[sender_id]

# --- Запуск бота ---
def main():
    print("Бот запущен...")
    client.run_until_disconnected()

if __name__ == '__main__':
    main()
