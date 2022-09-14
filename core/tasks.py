from project.celery import app
from core.send_email import send_activation_email, send_html_activation_email


@app.task
def celery_send_activation_email(user_email):
    send_auth_email(user_email)


@app.task
def celery_send_html_activation_email(user, current_site):
    send_html_activation_email(user, current_site)
