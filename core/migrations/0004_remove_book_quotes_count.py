# Generated by Django 4.1 on 2022-08-17 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_book_quotes_count"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="book",
            name="quotes_count",
        ),
    ]