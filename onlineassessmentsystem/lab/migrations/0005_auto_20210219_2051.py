# Generated by Django 3.1.5 on 2021-02-19 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0004_labgrade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='labgrade',
            name='grade',
            field=models.CharField(default='F', max_length=2),
        ),
    ]
