# Generated by Django 5.1.4 on 2025-02-03 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emsmodel', '0011_attclosingday_attleave_attmain_attot_salaryloan_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ramazan',
            name='Tranzdatetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
