# Generated by Django 2.2 on 2021-03-08 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0003_auto_20210308_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='insurance_number',
            field=models.CharField(max_length=70, verbose_name='Insurance Number'),
        ),
    ]
