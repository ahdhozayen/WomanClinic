# Generated by Django 3.0.1 on 2020-02-01 13:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0007_auto_20200201_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='date',
            field=models.DateField(blank=True, default=datetime.date(2020, 2, 1), null=True, verbose_name='تاريخ الولادة'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='lnmp',
            field=models.DateField(blank=True, null=True, verbose_name='اخر تاريخ للدورة الشهرية'),
        ),
    ]
