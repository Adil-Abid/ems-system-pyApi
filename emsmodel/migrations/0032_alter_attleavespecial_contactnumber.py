# Generated by Django 5.1.4 on 2025-06-02 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emsmodel', '0031_attleavespecial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attleavespecial',
            name='ContactNumber',
            field=models.TextField(default='-'),
        ),
    ]
