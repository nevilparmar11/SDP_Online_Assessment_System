# Generated by Django 3.1.5 on 2021-01-21 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0002_auto_20210113_1155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='endTime',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='contest',
            name='startTime',
            field=models.DateTimeField(),
        ),
    ]