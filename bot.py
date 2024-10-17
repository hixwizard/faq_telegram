from telegram import Update
from telegram.ext import CallbackContext


async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        ('Добро пожаловать в финансовый консалтинг!',
         'Как долго вы занимаетесь бизнесом?'))


async def process_application(update: Update, context: CallbackContext):
    # Процесс обработки заявки
    user = update.message.from_user
    await update.message.reply_text(
        f'Спасибо за ваш ответ, {user.first_name}.'
        'Мы начали формировать вашу заявку.')
    # Логика сохранения заявки в базу данных и отправки уведомления админу.
