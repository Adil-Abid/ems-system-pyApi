# Generated by Django 5.1.4 on 2025-01-22 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emsmodel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('VID', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('VCode', models.TextField()),
                ('VName', models.TextField()),
                ('VNameUrdu', models.TextField()),
                ('SortOrder', models.IntegerField()),
                ('GroupID', models.IntegerField()),
                ('Strength', models.IntegerField()),
                ('LocationID', models.IntegerField()),
                ('IsActive', models.IntegerField()),
                ('UID', models.IntegerField()),
                ('CompanyID', models.IntegerField()),
                ('Tranzdatetime', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='DepartmentGroup',
            fields=[
                ('VID', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('VCode', models.TextField()),
                ('VName', models.TextField()),
                ('VNameUrdu', models.TextField()),
                ('SortOrder', models.IntegerField()),
                ('IsActive', models.IntegerField()),
                ('UID', models.IntegerField()),
                ('CompanyID', models.IntegerField()),
                ('Tranzdatetime', models.DateTimeField()),
            ],
        ),
    ]
