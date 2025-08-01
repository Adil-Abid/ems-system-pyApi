# Generated by Django 5.1.4 on 2025-02-10 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emsmodel', '0013_designation_locationid_alter_holiday_tranzdatetime_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttOTMonth',
            fields=[
                ('VID', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('VName', models.TextField()),
                ('VNo', models.TextField()),
                ('VDate', models.DateTimeField()),
                ('EmpID', models.DecimalField(decimal_places=0, max_digits=18)),
                ('OverTime', models.DecimalField(decimal_places=2, max_digits=4)),
                ('LeaveTypeID', models.IntegerField()),
                ('UID', models.IntegerField()),
                ('CompanyID', models.IntegerField()),
                ('Tranzdatetime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmpLocationTransfer',
            fields=[
                ('VID', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('VName', models.TextField()),
                ('VNo', models.TextField()),
                ('VDate', models.DateTimeField()),
                ('EmpID', models.DecimalField(decimal_places=0, max_digits=18)),
                ('CurrentLocationID', models.IntegerField()),
                ('LocationID', models.IntegerField()),
                ('IsPosted', models.IntegerField()),
                ('PostedBy', models.IntegerField()),
                ('PostedDate', models.DateTimeField()),
                ('IsActive', models.BooleanField(default=True)),
                ('UID', models.IntegerField()),
                ('CompanyID', models.IntegerField()),
                ('Tranzdatetime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('EmpID', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('ETypeID', models.IntegerField()),
                ('LocationID', models.IntegerField()),
                ('EmpCode', models.TextField()),
                ('AccCode', models.TextField()),
                ('MachineCode', models.TextField()),
                ('EName', models.TextField()),
                ('FName', models.TextField()),
                ('DeptID', models.IntegerField()),
                ('DesgID', models.IntegerField()),
                ('HODID', models.DecimalField(decimal_places=0, max_digits=18)),
                ('DOB', models.DateTimeField()),
                ('DOJ', models.DateTimeField()),
                ('DOJAct', models.DateTimeField()),
                ('HireType', models.TextField(null=True)),
                ('JobType', models.TextField(null=True)),
                ('OffDay1', models.IntegerField()),
                ('OffDay2', models.IntegerField()),
                ('ShiftID', models.IntegerField()),
                ('NIC', models.TextField()),
                ('BasicSalary', models.DecimalField(decimal_places=0, max_digits=10)),
                ('ActualSalary', models.DecimalField(decimal_places=0, max_digits=10)),
                ('ManagerSalary', models.DecimalField(decimal_places=0, max_digits=18)),
                ('IncomeTax', models.DecimalField(decimal_places=0, max_digits=18)),
                ('HaveOT', models.BooleanField(default=True)),
                ('HaveOTAct', models.BooleanField(default=True)),
                ('HaveOTOFF', models.BooleanField(default=True)),
                ('ReplacementOf', models.DecimalField(decimal_places=0, max_digits=18)),
                ('IsBank', models.BooleanField(default=True)),
                ('BankAccountNo', models.TextField()),
                ('CompanyBankID', models.IntegerField()),
                ('Isactive', models.IntegerField()),
                ('IsactiveAct', models.IntegerField()),
                ('DOL', models.DateTimeField()),
                ('DOLAct', models.DateTimeField()),
                ('LeftRemarks', models.TextField()),
                ('GradeID', models.IntegerField()),
                ('ProbitionStatus', models.TextField()),
                ('ProbitionDate', models.DateTimeField()),
                ('CellPhone', models.TextField()),
                ('IcePhone', models.TextField()),
                ('Address', models.TextField()),
                ('AddressPermanent', models.TextField()),
                ('Bloodgroup', models.TextField()),
                ('EOBINo', models.TextField()),
                ('EOBINoAct', models.TextField()),
                ('SSNo', models.TextField()),
                ('LifeInsuranceNo', models.TextField()),
                ('IsGroupInsurance', models.BooleanField(default=True)),
                ('MartialStatus', models.TextField()),
                ('IsPFundEntitled', models.BooleanField(default=True)),
                ('PFundEntitledDate', models.DateTimeField()),
                ('IsPFund', models.BooleanField(default=True)),
                ('PFAmount', models.DecimalField(decimal_places=0, max_digits=18)),
                ('IsPessi', models.BooleanField(default=True)),
                ('PessiDate', models.DateTimeField()),
                ('Gender', models.TextField()),
                ('ReligionID', models.IntegerField()),
                ('IsExempt', models.BooleanField(default=True)),
                ('IsShiftEmployee', models.BooleanField(default=True)),
                ('IsShiftEmployeeAct', models.BooleanField(default=True)),
                ('ExemptLate', models.BooleanField(default=True)),
                ('ExemptMinuts', models.IntegerField()),
                ('Education', models.TextField(null=True)),
                ('ENameUrdu', models.TextField()),
                ('FNameUrdu', models.TextField()),
                ('AddressUrdu', models.TextField()),
                ('DesignationTitle', models.TextField()),
                ('OldCode', models.TextField()),
                ('MotherName', models.TextField()),
                ('NextToKin', models.TextField()),
                ('IsTransport', models.BooleanField(default=True)),
                ('TransportDate', models.DateTimeField()),
                ('TransportRoute', models.TextField()),
                ('TransportLocation', models.TextField()),
                ('IsManager', models.BooleanField(default=True)),
                ('IsShowForAudit', models.BooleanField(default=True)),
                ('IsStopSalary', models.BooleanField(default=True)),
                ('OTRate', models.DecimalField(decimal_places=0, max_digits=4)),
                ('OTRateOFF', models.DecimalField(decimal_places=0, max_digits=4)),
                ('NICExpairy', models.DateTimeField()),
                ('BusDeduction', models.BooleanField(default=True)),
                ('BlackList', models.BooleanField(default=True)),
                ('UID', models.IntegerField()),
                ('Tranzdatetime', models.DateTimeField(auto_now_add=True)),
                ('CompanyID', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeType',
            fields=[
                ('VID', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('VCode', models.TextField()),
                ('VName', models.TextField()),
                ('SortOrder', models.IntegerField()),
                ('SalaryTypeID', models.IntegerField()),
                ('IsActive', models.BooleanField(default=True)),
                ('UID', models.IntegerField()),
                ('CompanyID', models.IntegerField()),
                ('Tranzdatetime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('VID', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('VCode', models.TextField()),
                ('VName', models.TextField()),
                ('SortOrder', models.IntegerField()),
                ('SalaryTypeID', models.IntegerField()),
                ('IsActive', models.BooleanField(default=True)),
                ('UID', models.IntegerField()),
                ('CompanyID', models.IntegerField()),
                ('Tranzdatetime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Religion',
            fields=[
                ('VID', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('VCode', models.TextField()),
                ('VName', models.TextField()),
                ('SortOrder', models.IntegerField()),
                ('SalaryTypeID', models.IntegerField()),
                ('IsActive', models.BooleanField(default=True)),
                ('UID', models.IntegerField()),
                ('CompanyID', models.IntegerField()),
                ('Tranzdatetime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SalaryType',
            fields=[
                ('VID', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('VCode', models.TextField()),
                ('VName', models.TextField()),
                ('IsActive', models.BooleanField(default=True)),
                ('UID', models.IntegerField()),
                ('CompanyID', models.IntegerField()),
                ('Tranzdatetime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('VID', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('VCode', models.TextField()),
                ('VName', models.TextField()),
                ('SortOrder', models.IntegerField()),
                ('SalaryTypeID', models.IntegerField()),
                ('IsActive', models.BooleanField(default=True)),
                ('UID', models.IntegerField()),
                ('CompanyID', models.IntegerField()),
                ('Tranzdatetime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='allowded',
            name='Tranzdatetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='allowdedcat',
            name='Tranzdatetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='allowdedgroup',
            name='Tranzdatetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='attclosingday',
            name='Tranzdatetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='attcode',
            name='Tranzdatetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='attgroup',
            name='Tranzdatetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='attleave',
            name='Tranzdatetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='attmain',
            name='Tranzdatetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='attot',
            name='Tranzdatetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='bank',
            name='Tranzdatetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='Tranzdatetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='department',
            name='Tranzdatetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='departmentgroup',
            name='Tranzdatetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='designation',
            name='Tranzdatetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='grade',
            name='Tranzdatetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='Tranzdatetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='salaryallowded',
            name='Tranzdatetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='salaryincrement',
            name='Tranzdatetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='salaryloan',
            name='Tranzdatetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='salaryloandeduction',
            name='Tranzdatetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
