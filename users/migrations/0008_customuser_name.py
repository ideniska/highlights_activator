# Generated by Django 4.1 on 2022-12-28 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0007_customuser_is_demo_demouserdata"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="name",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
