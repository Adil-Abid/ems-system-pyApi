# Generated by Django 5.1.4 on 2025-05-28 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emsmodel', '0025_alter_salaryallowded_approvedby_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salaryloan',
            name='ApprovedBy',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='salaryloan',
            name='ApprovedDate',
            field=models.DateTimeField(default='1900-01-01'),
        ),
        migrations.AlterField(
            model_name='salaryloan',
            name='IsApproved',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='salaryloan',
            name='IsPosted',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='salaryloan',
            name='PostedBy',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='salaryloan',
            name='PostedDate',
            field=models.DateTimeField(default='1900-01-01'),
        ),
        migrations.AlterField(
            model_name='salaryloan',
            name='RefNo',
            field=models.TextField(default='-'),
        ),
        migrations.AlterField(
            model_name='salaryloan',
            name='UsedAmount',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=18),
        ),
        migrations.AlterField(
            model_name='salaryloan',
            name='VName',
            field=models.TextField(blank=True),
        ),
    ]
