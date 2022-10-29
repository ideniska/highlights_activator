from unicodedata import name
from telegram.ext import Updater
import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler, MessageHandler, Filters
import requests
from db import init_db
from db import add_user_email
from db import get_user_email
import datetime, pytz


TOKEN = "5446374976:AAHwD0UZQKJRLdBRxUE3rRGkdIYGthGToLc"
# user = CustomUser.objects.get(id=1)

random_quote_url = "http://127.0.0.1:8000/api/telegram/random-quote/"
connect_user_url = "http://127.0.0.1:8000/api/telegram/connect/"
# random_quote_url = "http://host.docker.internal:8000/api/telegram-random/"


def main():

    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    init_db()

    # random_button = "Random"
    # send_daily_button = "Send daily quote"
    reply_keyboard = [["/get_random", "/get_daily"], ["/get_weekly", "/stop"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    def start_callback(update, context):
        # buttons = [[KeyboardButton(random_button)], [KeyboardButton(send_daily_button)]]
        django_telegram_key = context.args
        update.message.reply_text("Hello! ", reply_markup=markup)
        if django_telegram_key:
            add_user_email(
                user_id=update.effective_chat.id, email=str(django_telegram_key[0])
            )
            payload = {
                "telegram_key": django_telegram_key,
                "telegram_id": update.effective_chat.id,
            }
            request_connect_tg_bot = requests.post(connect_user_url, data=payload)
            if request_connect_tg_bot:
                update.message.reply_text("Account connected!")
            else:
                update.message.reply_text(
                    "Something went wrong, account is not connected :("
                )

    def random_quote(update: Update, context):
        payload = {
            "email": get_user_email(user_id=update.effective_chat.id, limit=1)[0][1],
            "telegram_id": update.effective_chat.id,
        }
        random_quote_response = requests.post(random_quote_url, data=payload)
        random_quote_text = random_quote_response.json()
        bot_message_text = f"Random quote: {random_quote_text['text']}"
        update.message.reply_text(bot_message_text)

    def callback_random_quote(context: CallbackContext):
        payload = {
            "email": get_user_email(
                user_id=context.job.context.effective_chat.id, limit=1
            )[0][1],
            "telegram_id": context.job.context.effective_chat.id,
        }
        random_quote_response = requests.post(random_quote_url, data=payload)
        random_quote_text = random_quote_response.json()
        bot_message_text = f"Random quote: {random_quote_text['text']}"
        context.bot.send_message(
            chat_id=context.job.context.effective_chat.id, text=bot_message_text
        )

    def random_daily_quote(update: Update, context: CallbackContext):
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Activated! I will send you a new random quote at 8:55 AM every day. Send /stop to deactivate.",
        )

        context.job_queue.run_daily(
            callback_random_quote,
            time=datetime.time(hour=8, minute=55, tzinfo=pytz.timezone("US/Eastern")),
            days=(0, 1, 2, 3, 4, 5, 6),
            context=update,
        )

    def random_weekly_quote(update: Update, context: CallbackContext):
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Activated! I will send you a new random quote at 8:55 AM every Monday. Send /stop to deactivate.",
        )

        context.job_queue.run_daily(
            callback_random_quote,
            when=datetime.time(hour=8, minute=55, tzinfo=pytz.timezone("US/Eastern")),
            days=(0),
            context=update,
        )

    # def messageHandler(update: Update, context: CallbackContext):
    #     if random_button in update.message.text:
    #         CommandHandler("random", random_quote)
    #     if send_daily_button in update.message.text:
    #         CommandHandler("daily", random_daily_quote)

    dispatcher.add_handler(
        CommandHandler("get_daily", random_daily_quote)
    )  # Get a random quote every day at 8:55
    dispatcher.add_handler(
        CommandHandler("get_weekly", random_weekly_quote)
    )  # Get a random quote every monday
    dispatcher.add_handler(CommandHandler("start", start_callback))
    dispatcher.add_handler(
        CommandHandler("get_random", random_quote)
    )  # Get instant random quote
    # dispatcher.add_handler(MessageHandler(Filters.text, messageHandler))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
