# Generated by Django 4.1 on 2022-08-30 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_quote_like"),
    ]

    operations = [
        migrations.AddField(
            model_name="quote",
            name="comment",
            field=models.CharField(default="", max_length=1500),
        ),
    ]
