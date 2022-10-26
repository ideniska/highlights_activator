# Generated by Django 4.1 on 2022-10-18 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_customuser_stripe_session_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="send_emails",
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name="customuser",
            name="send_telegrams",
            field=models.IntegerField(default=1),
        ),
    ]