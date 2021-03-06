# Generated by Django 2.2 on 2019-06-01 19:43

import Account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExtendedUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userID', models.IntegerField()),
                ('ava', models.ImageField(upload_to=Account.models.getAvaName)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(default=0)),
                ('title', models.CharField(max_length=32)),
                ('text', models.CharField(max_length=1024)),
                ('time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('surname', models.CharField(max_length=32)),
                ('login', models.CharField(max_length=32)),
                ('mail', models.EmailField(max_length=64)),
                ('passwd', models.CharField(max_length=256)),
            ],
        ),
    ]
