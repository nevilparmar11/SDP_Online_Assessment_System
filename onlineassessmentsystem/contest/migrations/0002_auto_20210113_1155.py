# Generated by Django 3.1.5 on 2021-01-13 06:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contest',
            old_name='classId',
            new_name='classroom',
        ),
    ]
