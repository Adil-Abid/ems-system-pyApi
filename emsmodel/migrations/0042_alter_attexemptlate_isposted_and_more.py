# Generated by Django 5.1.4 on 2025-06-10 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emsmodel', '0041_attexemptlate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attexemptlate',
            name='IsPosted',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='attexemptlate',
            name='LocationID',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='attexemptlate',
            name='PostedBy',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='attexemptlate',
            name='PostedDate',
            field=models.DateField(default='1900-01-01'),
        ),
        migrations.AlterField(
            model_name='attleavedepartment',
            name='LocationID',
            field=models.IntegerField(default=0),
        ),
    ]
