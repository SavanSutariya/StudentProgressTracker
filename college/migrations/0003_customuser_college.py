# Generated by Django 3.2.9 on 2022-01-06 09:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0002_auto_20220106_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='college',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='college.college'),
            preserve_default=False,
        ),
    ]