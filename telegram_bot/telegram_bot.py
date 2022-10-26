from telegram.ext import Updater
import logging
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler, MessageHandler, Filters
import requests

# from api.services import pick_random_quote_id
# from core.models import Quote
# from users.models import CustomUser
# from django.conf import settings

TOKEN = "5446374976:AAHwD0UZQKJRLdBRxUE3rRGkdIYGthGToLc"
# user = CustomUser.objects.get(id=1)

random_quote_url = "http://127.0.0.1:8000/api/telegram/random-quote/"
connect_user_url = "http://127.0.0.1:8000/api/telegram/connect/"
# random_quote_url = "http://host.docker.internal:8000/api/telegram-random/"


def main():
    response = requests.get(random_quote_url)
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    # def start(update: Update, context: CallbackContext):
    #     context.bot.send_message(
    #         chat_id=update.effective_chat.id,
    #         text="Hello! Type your email to connect to your HA app or type random to get ",
    #     )

    def start_callback(update, context):
        django_telegram_key = context.args
        update.message.reply_text(
            "Hello! "
            + str(django_telegram_key[0])
            + "id:"
            + str(update.effective_chat.id)
        )
        if django_telegram_key:
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

    # def random_quote(update: Update, context: CallbackContext):
    #             random_quote_text = Quote.objects.get(id=pick_random_quote_id(user))
    #             bot_message_text = f"Random quote: {random_quote_text.text}\nYour id: {update.effective_chat.id}"
    #             context.bot.send_message(
    #                 chat_id=update.effective_chat.id, text=bot_message_text
    #             )

    def random_quote(update: Update, context: CallbackContext):
        random_quote_text = response.json()
        bot_message_text = f"Random quote: {random_quote_text[0]['text']}"
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=bot_message_text
        )

    # def handle_response(text) -> str:
    #             if "random" in text:
    #                 # random_quote_text = Quote.objects.get(id=pick_random_quote_id(1))
    #                 random_quote_text = Quote.objects.get(id=2)
    #                 bot_message_text = f"Random quote: {random_quote_text.text}"
    #                 return bot_message_text

    #             if "@" in text:
    #                 try:
    #                     user = CustomUser.objects.get(email=text)
    #                 except:
    #                     return "Account not found"
    #                 user.telegram_id = update.effective_chat.id
    #                 return "Account connected"

    #             return "I don't understand. Please type random to get a random quote"

    # def handle_message(update, context):
    #             # Get basic info of the incoming message
    #             text = str(update.message.text).lower()
    #             # Print a log for debugging
    #             print(f'User ({update.message.chat.id}) says: "{text}"')

    #             response = handle_response(text)
    #             update.message.reply_text(response)

    # start_handler = CommandHandler("start", start)
    # dispatcher.add_handler(start_handler)

    dispatcher.add_handler(CommandHandler("start", start_callback))

    random_handler = CommandHandler("random", random_quote)
    dispatcher.add_handler(random_handler)
    # dispatcher.add_handler(MessageHandler(Filters.text, handle_message))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
