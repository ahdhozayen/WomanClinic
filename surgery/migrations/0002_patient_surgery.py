# Generated by Django 3.0.1 on 2020-02-03 20:56

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0011_auto_20200203_2256'),
        ('surgery', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient_Surgery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surgery_doctor', models.CharField(max_length=80, verbose_name='اسم الجراح')),
                ('surgery_date', models.DateField(default=datetime.date.today, verbose_name='تاريخ اجراء العملية')),
                ('exit_date', models.DateField(default=datetime.date.today, verbose_name='تاريخ الخروج')),
                ('case_progress', models.CharField(max_length=250, verbose_name='تطور الحالة')),
                ('final_diagnosis', models.CharField(max_length=250, verbose_name='التشخيص النهائي')),
                ('recomendations', models.TextField(verbose_name='توصيات اخري')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient.Patient', verbose_name='اسم المريضة')),
                ('surgery_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surgery.Surgery_Master', verbose_name='نوع العملية')),
            ],
        ),
    ]
