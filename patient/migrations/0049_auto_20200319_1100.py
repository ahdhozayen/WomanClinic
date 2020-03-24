# Generated by Django 3.0.1 on 2020-03-19 09:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0048_auto_20200319_1002'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='exit_note',
        ),
        migrations.AlterField(
            model_name='diabetes',
            name='reading_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 19, 11, 0, 7, 103601), verbose_name='تاريخ القراءة'),
        ),
    ]
