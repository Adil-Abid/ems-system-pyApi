# Generated by Django 5.1.4 on 2025-06-11 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emsmodel', '0043_alter_attexemptlate_iscancel_alter_attot_vno_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shift',
            name='IsActive',
            field=models.IntegerField(default=True),
        ),
    ]
