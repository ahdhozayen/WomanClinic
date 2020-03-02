# Generated by Django 3.0.1 on 2020-02-26 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0026_auto_20200221_1108'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='entrance_date',
            field=models.DateField(blank=True, null=True, verbose_name='تاريخ دخول المستشفي'),
        ),
        migrations.AddField(
            model_name='patient',
            name='exit_date',
            field=models.DateField(blank=True, null=True, verbose_name='تارخ الخروج'),
        ),
        migrations.AddField(
            model_name='patient',
            name='patient_type',
            field=models.CharField(blank=True, choices=[('CHECK_UP', 'متابعة'), ('CONSULTANT', 'استشاري'), ('OPERATION', 'عمليات'), ('DELIVERY_CHECK', 'متابعة ولادة'), ('DAYS_OFF', 'اجازات')], max_length=50, null=True, verbose_name='طبيعة المريضة'),
        ),
    ]
