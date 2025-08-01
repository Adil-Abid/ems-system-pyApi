# Generated by Django 5.1.4 on 2025-06-04 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emsmodel', '0036_salarygratuity_basicsalary_salarygratuity_paidon'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeLeaveBalance',
            fields=[
                ('VID', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('VName', models.TextField()),
                ('AttGroupID', models.IntegerField()),
                ('DateFrom', models.DateTimeField()),
                ('DateTo', models.DateTimeField()),
                ('LeaveLimit', models.IntegerField()),
                ('LocationID', models.IntegerField()),
                ('IsActive', models.BooleanField(default=True)),
                ('UID', models.IntegerField()),
                ('CompanyID', models.IntegerField()),
                ('Tranzdatetime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
