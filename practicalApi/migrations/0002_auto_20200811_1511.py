# Generated by Django 3.1 on 2020-08-11 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practicalApi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsersData',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.CharField(max_length=100)),
                ('number', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name='Users',
        ),
    ]