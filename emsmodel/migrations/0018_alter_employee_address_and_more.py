# Generated by Django 5.1.4 on 2025-05-22 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emsmodel', '0017_alter_employee_actualsalary_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='Address',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='AddressPermanent',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='AddressUrdu',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='Bloodgroup',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='CellPhone',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='DesignationTitle',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='ENameUrdu',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='EOBINo',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='EOBINoAct',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='Education',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='FNameUrdu',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='HODID',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=18),
        ),
        migrations.AlterField(
            model_name='employee',
            name='IcePhone',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='LeftRemarks',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='LifeInsuranceNo',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='MotherName',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='NextToKin',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='PFAmount',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=18),
        ),
        migrations.AlterField(
            model_name='employee',
            name='SSNo',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='TransportLocation',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='TransportRoute',
            field=models.TextField(blank=True),
        ),
    ]
