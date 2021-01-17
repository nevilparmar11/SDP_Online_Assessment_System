# Generated by Django 3.1.5 on 2021-01-13 06:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='problem',
            old_name='contestId',
            new_name='contest',
        ),
        migrations.RenameField(
            model_name='problem',
            old_name='labId',
            new_name='lab',
        ),
        migrations.RenameField(
            model_name='problemcomment',
            old_name='problemId',
            new_name='problem',
        ),
        migrations.RenameField(
            model_name='problemcomment',
            old_name='userId',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='testcase',
            old_name='problemId',
            new_name='problem',
        ),
    ]