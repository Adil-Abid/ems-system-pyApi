# Generated by Django 5.1.4 on 2025-01-29 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emsmodel', '0003_allowded_allowdedcat_allowdedgroup_attcode_attgroup_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='allowdedgroup',
            name='VName',
            field=models.TextField(default='2025-01-29'),
            preserve_default=False,
        ),
    ]
