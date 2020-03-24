# Generated by Django 3.0.1 on 2020-03-19 12:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0051_auto_20200319_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diabetes',
            name='bp_down',
            field=models.PositiveIntegerField(default=80, max_length=3, verbose_name='BP Down'),
        ),
        migrations.AlterField(
            model_name='diabetes',
            name='bp_up',
            field=models.PositiveIntegerField(default=120, max_length=3, verbose_name='BP Up'),
        ),
        migrations.AlterField(
            model_name='diabetes',
            name='reading_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 19, 14, 34, 12, 480282), verbose_name='تاريخ القراءة'),
        ),
    ]
