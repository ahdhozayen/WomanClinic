# Generated by Django 3.0.1 on 2020-11-15 08:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0054_auto_20201106_1712'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='past_medical_history',
            name='hobt',
        ),
        migrations.AddField(
            model_name='past_medical_history',
            name='autoimmun_disorder_value',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Autoimmun Disorder Value'),
        ),
        migrations.AddField(
            model_name='past_medical_history',
            name='history_of_blood_transfusion',
            field=models.BooleanField(blank=True, null=True, verbose_name='History Of Blood Transfusion'),
        ),
        migrations.AddField(
            model_name='past_medical_history',
            name='history_of_blood_transfusion_value',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='History Of Blood Transfusion Value'),
        ),
        migrations.AddField(
            model_name='past_medical_history',
            name='hld_value',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='HLD Value'),
        ),
        migrations.AddField(
            model_name='past_medical_history',
            name='kidney_disease_value',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Kidney Disease Value'),
        ),
        migrations.AddField(
            model_name='past_medical_history',
            name='thyroid_dysfunction_value',
            field=models.CharField(blank=True, choices=[('hypo', 'HYPO'), ('hyper', 'HYPER')], max_length=20, null=True, verbose_name='THYROID DYSFUNCTION Value'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='type',
            field=models.CharField(blank=True, choices=[('n', 'NVD'), ('c', 'LSCS')], max_length=30, null=True, verbose_name='Delivery Types'),
        ),
        migrations.AlterField(
            model_name='diabetes',
            name='reading_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 15, 10, 48, 10, 637833), verbose_name='reading date'),
        ),
        migrations.AlterField(
            model_name='past_medical_history',
            name='abnormal_pap',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Abnormal PAP'),
        ),
        migrations.AlterField(
            model_name='past_medical_history',
            name='allergies',
            field=models.BooleanField(blank=True, null=True, verbose_name='Allergies'),
        ),
        migrations.AlterField(
            model_name='past_medical_history',
            name='anesthetic',
            field=models.CharField(blank=True, choices=[('GA', 'GA'), ('SA', 'SA')], max_length=20, null=True, verbose_name='ANESTHETIC'),
        ),
        migrations.AlterField(
            model_name='past_medical_history',
            name='autoimmun_disorder',
            field=models.BooleanField(blank=True, null=True, verbose_name='Autoimmun Disorder'),
        ),
        migrations.AlterField(
            model_name='past_medical_history',
            name='breast',
            field=models.BooleanField(blank=True, null=True, verbose_name='Breast'),
        ),
        migrations.AlterField(
            model_name='past_medical_history',
            name='diabetes',
            field=models.BooleanField(blank=True, null=True, verbose_name='Diabetes'),
        ),
        migrations.AlterField(
            model_name='past_medical_history',
            name='gyns',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='GYNS'),
        ),
        migrations.AlterField(
            model_name='past_medical_history',
            name='heart_disease',
            field=models.BooleanField(blank=True, null=True, verbose_name='Heart Disease'),
        ),
        migrations.AlterField(
            model_name='past_medical_history',
            name='hld',
            field=models.BooleanField(blank=True, null=True, verbose_name='HLD'),
        ),
        migrations.AlterField(
            model_name='past_medical_history',
            name='hypertension',
            field=models.BooleanField(blank=True, null=True, verbose_name='Hypertension'),
        ),
        migrations.AlterField(
            model_name='past_medical_history',
            name='infertility',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='INFERTILITY'),
        ),
        migrations.AlterField(
            model_name='past_medical_history',
            name='kidney_disease',
            field=models.BooleanField(blank=True, null=True, verbose_name='Kidney Disease'),
        ),
        migrations.AlterField(
            model_name='past_medical_history',
            name='neurologic',
            field=models.BooleanField(blank=True, null=True, verbose_name='NEUROLOGIC'),
        ),
        migrations.AlterField(
            model_name='past_medical_history',
            name='operation',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='OPERATION'),
        ),
        migrations.AlterField(
            model_name='past_medical_history',
            name='psychiatric',
            field=models.BooleanField(blank=True, null=True, verbose_name='PSYCHIATRIC'),
        ),
        migrations.AlterField(
            model_name='past_medical_history',
            name='pulmonar',
            field=models.BooleanField(blank=True, null=True, verbose_name='Pulmonar'),
        ),
        migrations.AlterField(
            model_name='past_medical_history',
            name='rfh',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='RFH'),
        ),
        migrations.AlterField(
            model_name='past_medical_history',
            name='thyroid_dysfunction',
            field=models.BooleanField(blank=True, null=True, verbose_name='THYROID DYSFUNCTION'),
        ),
        migrations.AlterField(
            model_name='past_medical_history',
            name='uterine',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='uterine'),
        ),
        migrations.AlterField(
            model_name='past_medical_history',
            name='varicosities',
            field=models.BooleanField(blank=True, null=True, verbose_name='VARICOSITIES'),
        ),
    ]
