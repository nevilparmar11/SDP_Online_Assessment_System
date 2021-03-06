# Generated by Django 3.1.5 on 2021-01-09 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('classroom', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('labId', models.AutoField(primary_key=True, serialize=False)),
                ('subject', models.CharField(default='DEFAULT-SUBJECT', max_length=50)),
                ('description', models.CharField(default='Default Lab description', max_length=1000)),
                ('deadline', models.DateField()),
                ('classId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classroom.classroom')),
            ],
        ),
    ]
