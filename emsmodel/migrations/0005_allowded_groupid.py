# Generated by Django 5.1.4 on 2025-01-29 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emsmodel', '0004_allowdedgroup_vname'),
    ]

    operations = [
        migrations.AddField(
            model_name='allowded',
            name='GroupID',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
