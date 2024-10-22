from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from databaseSingleton import DatabaseSingleton
from enum import Enum
from dotenv import load_dotenv
import os
from models import Ticket
#вынести тикеты в модель джанго!!!

load_dotenv()

db=DatabaseSingleton()           

#надеюсь что коммит про emum правильно поняла
class ButtonText(Enum):
    write_complain = "Написать жалобу"

# обр нач кнопки стр
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    keyboard = [[ButtonText.write_complain.value]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(f'Hello {update.effective_user.first_name},', reply_markup=reply_markup)


# обр кнопки "напис жалоб"
async def request_complain(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # флаг юзера что он захотел пожаловаться (жалуются тока гады!!!)
    context.user_data['complain_mode'] = True
    await update.message.reply_text("Напишите нам, что вас не устроило или что хотели бы изменить. Нам важно ваше мнение!!ю ноу")



# ответы на смс пользователя!!
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.text == ButtonText.write_complain.value:
        await request_complain(update, context)
    elif context.user_data.get('complain_mode', False):
        if 'complain_text' not in context.user_data:
            # жалоба
            context.user_data['complain_text'] = update.message.text
            await update.message.reply_text("Подскажите ваши контактные данные")

        else:
            contact_information = update.message.text
            # вырезать жабу
            complain_text = context.user_data.pop('complain_text')
            # await update.message.reply_text(f"ваш контакт: {contact_information}\nваша жалоба: {complain_text}")
            await update.message.reply_text("Спасибо за ваш отзыв! Жалобу рассмотрим в ближайшее время")
            context.user_data['complain_mode'] = False
            Ticket.insert(contact_information,complain_text)
            # db.insert_ticket(contact_information,complain_text)


if __name__ == '__main__':
    
    token=os.getenv("TOKEN")
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()



