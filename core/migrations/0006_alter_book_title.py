# Generated by Django 4.1 on 2022-12-15 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_remove_orders_stripe_user_email"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="title",
            field=models.CharField(max_length=350, unique=True),
        ),
    ]
