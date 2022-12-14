# Generated by Django 4.1 on 2022-10-10 16:01

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=350)),
                ('author', models.CharField(default='', max_length=350)),
                ('visibility', models.BooleanField(default=True)),
                ('cover', models.CharField(default='', max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_type', models.CharField(max_length=15)),
                ('stripe_order_id', models.CharField(max_length=35)),
                ('subscription_period', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=3, max_digits=10)),
                ('payment_date', models.DateTimeField()),
                ('payment_status', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.CharField(max_length=250)),
                ('text', models.CharField(max_length=1500)),
                ('like', models.BooleanField(default=False)),
                ('comment', models.CharField(default='', max_length=1500)),
            ],
        ),
        migrations.CreateModel(
            name='UserFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=core.models.upload_file_path, verbose_name='')),
                ('type', models.CharField(choices=[('kindle', 'Kindle'), ('other', 'Other')], max_length=30)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
