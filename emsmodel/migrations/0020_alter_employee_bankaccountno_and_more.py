# Generated by Django 5.1.4 on 2025-05-22 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emsmodel', '0019_alter_employee_probitionstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='BankAccountNo',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='CompanyBankID',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='DOJAct',
            field=models.DateTimeField(default='1900-01-01'),
        ),
    ]
