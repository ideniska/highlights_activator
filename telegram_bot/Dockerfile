FROM python:3.10

RUN pip install python-telegram-bot requests

COPY telegram_bot.py .

EXPOSE 8000

CMD ["python", "./telegram_bot.py"]