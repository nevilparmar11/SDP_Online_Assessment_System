# Generated by Django 3.1.5 on 2021-01-24 13:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0003_auto_20210124_1842'),
    ]

    operations = [
        migrations.RenameField(
            model_name='problem',
            old_name='durationTime',
            new_name='timeLimit',
        ),
    ]
