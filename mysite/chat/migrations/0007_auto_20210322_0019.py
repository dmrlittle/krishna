# Generated by Django 3.1.6 on 2021-03-21 18:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_auto_20210322_0012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meet',
            name='dt',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
