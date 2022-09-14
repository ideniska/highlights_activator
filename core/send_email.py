from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site

# from django.utils.encoding import force_bytes, force_text


def send_activation_email(user_email):
    send_mail(
        "Confirm your email address",
        "Thank you for registering. Please confirm your email below.",
        "ha@example.com",
        [user_email],
        fail_silently=False,
    )
    print("email_sent")


def send_html_activation_email(user, current_site):
    mail_subject = "Confirm your email address"
    message = render_to_string(
        "email_confirmation.html",
        {
            "user": user,
            "domain": current_site.domain,
            "uid": user.pk,
            "token": default_token_generator.make_token(user),
        },
    )
    to_email = user.email
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()