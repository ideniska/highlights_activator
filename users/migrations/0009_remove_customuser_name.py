# Generated by Django 4.1 on 2022-12-28 23:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0008_customuser_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="name",
        ),
    ]
