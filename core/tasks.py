from project.celery import app
from os import path
from smtplib import SMTPRecipientsRefused
from typing import Any, Optional

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.translation import activate

from core.send_email import send_html_activation_email
from core.get_book_covers import get_book_covers
from core.kindle_parser import start_kindle_parser
from core.models import UserFile, CustomUser, Orders


# @app.task
# def celery_send_activation_email(user_email):
#     send_activation_email(user_email)


@app.task
def celery_stop_membership(user_id):
    user = CustomUser.objects.get(id=user_id)
    user.active_subscription = False
    user.trial_used = True
    user.save()
    order = Orders.objects.filter(user_id=user_id).last()
    order.payment_status = "Canceled"
    order.save()


@app.task
def celery_send_html_activation_email(user_id):
    send_html_activation_email(user_id)


@app.task
def celery_get_book_covers(user_id):
    get_book_covers(user_id)


@app.task
def celery_start_kindle_parser(userfile_id: int):
    userfile = UserFile.objects.get(id=userfile_id)
    start_kindle_parser(userfile)


class SendingEmailTaskArgs(app.Task):
    autoretry_for = (SMTPRecipientsRefused, ConnectionRefusedError)
    retry_kwargs = {"max_retries": 5}
    retry_backoff = 5
    retry_jitter = True


@app.task(name="email.send_information_email", base=SendingEmailTaskArgs)
def send_information_email(
    *,
    subject: str,
    template_name: str,
    context: dict,
    to_email: list[str] | str,
    letter_language: str = "en",
    **kwargs: Optional[Any],
) -> bool:
    """
    :param subject: email subject
    :param template_name: template path to email template
    :param context: data what will be passed into email
    :param to_email: receiver email(s)
    :param letter_language: translate letter to selected lang
    :param kwargs: from_email, bcc, cc, reply_to and file_path params
    """
    activate(letter_language)
    _to_email: list[str] = [to_email] if isinstance(to_email, str) else to_email
    email_message = EmailMultiAlternatives(
        subject=subject,
        to=_to_email,
        from_email=kwargs.get("from_email"),
        bcc=kwargs.get("bcc"),
        cc=kwargs.get("cc"),
        reply_to=kwargs.get("reply_to"),
    )
    html_email: str = loader.render_to_string(template_name, context)
    email_message.attach_alternative(html_email, "text/html")
    if file_path := kwargs.get("file_path"):
        file_path = path.join(settings.BASE_DIR, file_path)
        email_message.attach_file(file_path, kwargs.get("mimetype"))
    email_message.send()
    return True
