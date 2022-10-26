from xml.dom import NotFoundErr
from django.core.management.base import BaseCommand
from telegram.ext import Updater
import logging
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler, MessageHandler, Filters
from api.services import pick_random_quote_id
from core.models import Quote
from users.models import CustomUser
from django.conf import settings

TOKEN = settings.TELEGRAM_TOKEN
# user = CustomUser.objects.get(id=1)


class Command(BaseCommand):
    help = "TG BOT"

    def handle(self, *args, **options):

        updater = Updater(token=TOKEN, use_context=True)
        dispatcher = updater.dispatcher

        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            level=logging.INFO,
        )

        def start(update: Update, context: CallbackContext):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Hello! Type your email to connect to your HA app or type random to get ",
            )

        def random_quote(update: Update, context: CallbackContext):
            random_quote_text = Quote.objects.get(id=pick_random_quote_id(user))
            bot_message_text = f"Random quote: {random_quote_text.text}\nYour id: {update.effective_chat.id}"
            context.bot.send_message(
                chat_id=update.effective_chat.id, text=bot_message_text
            )

        def handle_response(text) -> str:
            if "random" in text:
                # random_quote_text = Quote.objects.get(id=pick_random_quote_id(1))
                random_quote_text = Quote.objects.get(id=2)
                bot_message_text = f"Random quote: {random_quote_text.text}"
                return bot_message_text

            if "@" in text:
                try:
                    user = CustomUser.objects.get(email=text)
                except:
                    return "Account not found"
                user.telegram_id = update.effective_chat.id
                return "Account connected"

            return "I don't understand. Please type random to get a random quote"

        def handle_message(update, context):
            # Get basic info of the incoming message
            text = str(update.message.text).lower()
            # Print a log for debugging
            print(f'User ({update.message.chat.id}) says: "{text}"')

            response = handle_response(text)
            update.message.reply_text(response)

        start_handler = CommandHandler("start", start)
        dispatcher.add_handler(start_handler)

        random_handler = CommandHandler("random", random_quote)
        dispatcher.add_handler(random_handler)
        dispatcher.add_handler(MessageHandler(Filters.text, handle_message))

        updater.start_polling()
        updater.idle()
