# Generated by Django 3.1.6 on 2021-03-21 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_meet_dt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meet',
            name='dt',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
