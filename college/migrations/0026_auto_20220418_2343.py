# Generated by Django 3.2.9 on 2022-04-18 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0025_auto_20220405_1315'),
    ]

    operations = [
        migrations.AddField(
            model_name='faculty',
            name='fcm_token',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='student',
            name='fcm_token',
            field=models.TextField(default=''),
        ),
    ]