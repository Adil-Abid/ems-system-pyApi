# Generated by Django 5.1.4 on 2025-06-18 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emsmodel', '0046_attroster'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttEntryRosterMonth',
            fields=[
                ('VID', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('EmpID', models.DecimalField(decimal_places=0, max_digits=18)),
                ('EmpCode', models.TextField()),
                ('EName', models.TextField(max_length=200)),
                ('Department', models.TextField(max_length=200)),
                ('Designation', models.TextField(max_length=200)),
                ('D01', models.CharField(blank=True, max_length=10, null=True)),
                ('D02', models.CharField(blank=True, max_length=10, null=True)),
                ('D03', models.CharField(blank=True, max_length=10, null=True)),
                ('D04', models.CharField(blank=True, max_length=10, null=True)),
                ('D05', models.CharField(blank=True, max_length=10, null=True)),
                ('D06', models.CharField(blank=True, max_length=10, null=True)),
                ('D07', models.CharField(blank=True, max_length=10, null=True)),
                ('D08', models.CharField(blank=True, max_length=10, null=True)),
                ('D09', models.CharField(blank=True, max_length=10, null=True)),
                ('D10', models.CharField(blank=True, max_length=10, null=True)),
                ('D11', models.CharField(blank=True, max_length=10, null=True)),
                ('D12', models.CharField(blank=True, max_length=10, null=True)),
                ('D13', models.CharField(blank=True, max_length=10, null=True)),
                ('D14', models.CharField(blank=True, max_length=10, null=True)),
                ('D15', models.CharField(blank=True, max_length=10, null=True)),
                ('D16', models.CharField(blank=True, max_length=10, null=True)),
                ('D17', models.CharField(blank=True, max_length=10, null=True)),
                ('D18', models.CharField(blank=True, max_length=10, null=True)),
                ('D19', models.CharField(blank=True, max_length=10, null=True)),
                ('D20', models.CharField(blank=True, max_length=10, null=True)),
                ('D21', models.CharField(blank=True, max_length=10, null=True)),
                ('D22', models.CharField(blank=True, max_length=10, null=True)),
                ('D23', models.CharField(blank=True, max_length=10, null=True)),
                ('D24', models.CharField(blank=True, max_length=10, null=True)),
                ('D25', models.CharField(blank=True, max_length=10, null=True)),
                ('D26', models.CharField(blank=True, max_length=10, null=True)),
                ('D27', models.CharField(blank=True, max_length=10, null=True)),
                ('D28', models.CharField(blank=True, max_length=10, null=True)),
                ('D29', models.CharField(blank=True, max_length=10, null=True)),
                ('D30', models.CharField(blank=True, max_length=10, null=True)),
                ('D31', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
    ]
