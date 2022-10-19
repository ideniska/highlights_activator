from telegram.ext import Updater
import logging
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from api.views import pick_random_object
from core.models import Quote

TOKEN = "5143838024:AAFxjxkBrsF27UQm3UY2ekQyCG63r7-sX3w"
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a HA bot, please talk to me!"
    )


random_quote_text = Quote.objects.filter(owner=1).filter(id=pick_random_object(1))


def random_quote(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=random_quote_text)


start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)

random_handler = CommandHandler("random", random_quote)
dispatcher.add_handler(random_handler)

updater.start_polling()
