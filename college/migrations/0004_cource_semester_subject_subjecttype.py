# Generated by Django 3.2.9 on 2022-01-06 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0003_customuser_college'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='college.college')),
            ],
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('cource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='college.cource')),
            ],
        ),
        migrations.CreateModel(
            name='SubjectType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=100)),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='college.semester')),
                ('sub_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='college.subjecttype')),
            ],
        ),
    ]
