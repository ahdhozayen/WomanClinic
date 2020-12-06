# Generated by Django 3.0.1 on 2020-11-06 15:02

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import patient.models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0001_initial'),
        ('patient', '0052_auto_20200319_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient_exit',
            name='date_end',
            field=models.DateField(blank=True, null=True, verbose_name='Days-off End Date'),
        ),
        migrations.AddField(
            model_name='patient_exit',
            name='date_start',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Days-off Start Date'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient_exit',
            name='exit_diagnosis',
            field=models.CharField(blank=True, max_length=70, null=True, verbose_name='Exit Diagnosis'),
        ),
        migrations.AddField(
            model_name='patient_exit',
            name='exit_nature',
            field=models.CharField(blank=True, choices=[('better', 'Better'), ('responsibility', 'Responsibility'), ('scape', 'Scape')], max_length=50, null=True, verbose_name='Exit Nature'),
        ),
        migrations.AddField(
            model_name='patient_exit',
            name='physician',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Physician'),
        ),
        migrations.AddField(
            model_name='patient_exit',
            name='resident_doctor',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Resident Doctor'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='abo_rh',
            field=models.CharField(blank=True, choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')], max_length=50, null=True, verbose_name='Blood Type'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='anesthesia_doc',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Anesthesia Doctor'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='anesthesia_type',
            field=models.CharField(blank=True, choices=[('S', 'Spinal anesthesia'), ('G', 'General anesthesia')], max_length=50, null=True, verbose_name='Anesthesia Type'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='date',
            field=models.DateField(blank=True, default=datetime.date.today, null=True, verbose_name='Delivery Date'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='description',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Delivery Notes'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='fetal_sex',
            field=models.CharField(blank=True, choices=[('m', 'ذكر'), ('f', 'انثي'), ('t', 'توأم')], max_length=50, null=True, verbose_name='Fetal Sex'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='lnmp',
            field=models.DateField(blank=True, null=True, verbose_name='Last Period Date'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='patient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='patient.Patient', verbose_name='Patient'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='place',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Delivery Hospital'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='type',
            field=models.CharField(blank=True, choices=[('n', 'طبيعي'), ('c', 'قيصري')], max_length=30, null=True, verbose_name='Delivery Types'),
        ),
        migrations.AlterField(
            model_name='diabetes',
            name='bp_down',
            field=models.PositiveIntegerField(default=80, verbose_name='BP Down'),
        ),
        migrations.AlterField(
            model_name='diabetes',
            name='bp_up',
            field=models.PositiveIntegerField(default=120, verbose_name='BP Up'),
        ),
        migrations.AlterField(
            model_name='diabetes',
            name='reading_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 6, 17, 2, 26, 739163), verbose_name='تاريخ القراءة'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='clexane_order_number',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Clexane Order Number'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True, verbose_name='Date Of Birth'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='entrance_date',
            field=models.DateField(blank=True, null=True, verbose_name='Enterance Date'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='entrance_number',
            field=models.PositiveIntegerField(verbose_name='Enterance Number'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='exit_date',
            field=models.DateField(blank=True, null=True, verbose_name='Exit Date'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='hospital',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic.Clinic', verbose_name='Hospital'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='hospital_number',
            field=models.PositiveIntegerField(verbose_name='Hospital Number'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='hospital_section',
            field=models.CharField(blank=True, max_length=70, null=True, verbose_name='Section'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='husband_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Husband Name'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='husband_phone',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Husband Phone'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='insurance_number',
            field=models.PositiveIntegerField(verbose_name='Insurance Number'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='job',
            field=models.CharField(max_length=30, verbose_name='Job'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='mobile',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Mobile'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='name',
            field=models.CharField(max_length=70, verbose_name='Patient Name'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='patient_number',
            field=models.PositiveIntegerField(verbose_name='Patient Number'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='patient_type',
            field=models.CharField(blank=True, choices=[('CHECK_UP', 'متابعة'), ('CONSULTANT', 'استشاري'), ('OPERATION', 'عمليات نسا'), ('DELIVER', 'ولادة')], max_length=50, null=True, verbose_name='Patient Type'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='phone',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Phone'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='pre',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='PRE'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='room',
            field=models.CharField(max_length=70, verbose_name='Room'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='transferred_from',
            field=models.CharField(blank=True, choices=[('insurance', 'عيادة تأمين'), ('consultant', 'عيادة استشاري'), ('outpatient', 'طبيب خارجي'), ('patient', 'المريض نفسه')], max_length=70, null=True, verbose_name='Patient Transferred From'),
        ),
        migrations.AlterField(
            model_name='patient_days_off',
            name='notes',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Notes'),
        ),
        migrations.AlterField(
            model_name='patient_days_off',
            name='num_of_days',
            field=models.PositiveIntegerField(verbose_name='Number of days'),
        ),
        migrations.AlterField(
            model_name='patient_exit',
            name='exit_date',
            field=models.DateField(blank=True, null=True, verbose_name='Exit Date'),
        ),
        migrations.AlterField(
            model_name='patient_exit',
            name='exit_note',
            field=models.TextField(blank=True, max_length=250, null=True, verbose_name='Exit Note'),
        ),
        migrations.AlterField(
            model_name='patient_files',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to=patient.models.path_and_rename, verbose_name='Attachment'),
        ),
        migrations.AlterField(
            model_name='patient_files',
            name='attachment_name',
            field=models.CharField(max_length=150, verbose_name='File Name'),
        ),
    ]
