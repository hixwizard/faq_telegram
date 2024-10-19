from telegram import Update
from telegram.ext import CallbackContext


async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        'Добро пожаловать в финансовый консалтинг!'
        ' Как долго вы занимаетесь бизнесом?'
    )


async def process_application(update: Update, context: CallbackContext):
    user = update.message.from_user
    # Можно использовать context для записи данных о пользователе
    # или для выполнения логики бота
    await update.message.reply_text(
        f'Спасибо за ваш ответ, {user.name}.'
        ' Мы начали формировать вашу заявку.'
    )
    # Логика сохранения заявки в базу данных и отправки уведомления админу.
    # context может использоваться для отправки уведомлений
    # можно использовать чат-id
    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID, text="Новая заявка получена"
    )
