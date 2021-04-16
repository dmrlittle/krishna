# Generated by Django 3.0 on 2021-04-16 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='meet',
            name='admin',
            field=models.ManyToManyField(to='accounts.UserProfile'),
        ),
        migrations.AddField(
            model_name='meet',
            name='members',
            field=models.ManyToManyField(related_name='groups', to='accounts.UserProfile'),
        ),
    ]