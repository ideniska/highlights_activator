from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from core.tasks import send_information_email
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

User = get_user_model()


class EmailService:
    def send_password_reset(self, user, current_site):
        send_information_email.delay(
            subject="Password recovery",
            template_name="emails/set_new_password.html",
            context={
                "user": user.email,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.id)),
                "token": default_token_generator.make_token(user),
            },
            to_email=user.email,
            letter_language="en",
        )

    def send_activation_link(self, user, current_site):
        send_information_email.delay(
            subject="Confirm registration",
            template_name="emails/email_confirmation.html",
            context={
                "user": user.email,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.id)),
                "token": default_token_generator.make_token(user),
            },
            to_email=user.email,
            letter_language="en",
        )

    def send_payment_confirmation(self, user, current_site):
        send_information_email.delay(
            subject="Thank you for subscribing!",
            template_name="emails/payment_confirmation.html",
            context={
                "user": user.email,
            },
            to_email=user.email,
            letter_language="en",
        )
