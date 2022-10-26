from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag()
def telegram_deep_link(user):
    url = settings.TELEGRAM_BOT_NAME.format(user.telegram_key)
    return url
