# Generated by Django 5.1.4 on 2025-07-30 09:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emsmodel', '0048_attclosingmonth'),
    ]

    operations = [
        migrations.CreateModel(
            name='dummy',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('age', models.PositiveIntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='department',
            name='GroupID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='emsmodel.departmentgroup'),
        ),
        migrations.AlterField(
            model_name='department',
            name='LocationID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='emsmodel.location'),
        ),
    ]
