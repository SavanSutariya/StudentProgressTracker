# Generated by Django 3.2.9 on 2022-03-19 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0018_alter_customuser_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_pic',
            field=models.ImageField(upload_to='media/profile_pic'),
        ),
    ]
