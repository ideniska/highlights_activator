# Generated by Django 4.1 on 2022-10-24 21:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_remove_orders_stripe_order_id_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="orders",
            name="stripe_user_email",
        ),
    ]
