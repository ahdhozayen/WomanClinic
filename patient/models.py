import os
from django.conf import settings
from django.db import models
from datetime import datetime, date
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from clinic.models import Clinic
from pharmacy.models import Medicine
from django.utils.translation import ugettext_lazy as _

import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File


class Patient(models.Model):
    transferred_list = [('insurance',_("Medical Insurance")),('consultant',_('Consultant Doctor')),
                        ('outpatient',_('Outside Doctor')),('patient',_('Patient himself'))]
    barcode_image = models.ImageField(upload_to='barcode/', blank=True, null=True)
    barcode = models.CharField(max_length=70, blank=True, null=True, verbose_name=_('barcode Number'))
    hospital = models.ForeignKey(Clinic, on_delete=models.CASCADE, verbose_name=_('Hospital'))
    name = models.CharField(max_length=70, verbose_name=_('Patient Name'))
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Address'))
    phone = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Phone'))
    mobile = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Mobile'))
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('Date Of Birth'))
    job = models.CharField(max_length=30, verbose_name=_('Job'))
    husband_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Husband Name'))
    husband_phone = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Husband Phone'))
    # *******************************************************
    g = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('G'))
    p = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('P'))
    pre = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('PRE'))
    insurance_number = models.CharField(max_length=70, verbose_name=_('Insurance Number'))
    entrance_number = models.PositiveIntegerField(verbose_name=_('Enterance Number'))
    hospital_number = models.PositiveIntegerField(verbose_name=_('Hospital Number'))
    patient_number = models.PositiveIntegerField(verbose_name=_('Patient Number'))
    room = models.CharField(max_length=70, verbose_name=_('Room'))
    hospital_section = models.CharField(max_length=70,blank=True, null=True, verbose_name=_('Section'))
    transferred_from = models.CharField(max_length=70, blank=True, null=True,choices=transferred_list ,verbose_name=_('Patient Transferred From'))
    clexane_order_number = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Clexane Order Number'))
    entrance_date = models.DateField(auto_now=False, blank=True, null=True, verbose_name=_('Enterance Date'))
    patient_type_list = [('CHECK_UP',_('Check up')), ('CONSULTANT',_('Consultant')), ('OPERATION',_("GYN operations")), ('DELIVER',_('Delivery'))]
    patient_type = models.CharField(max_length=50, choices=patient_type_list, blank=True, null=True, verbose_name=_('Patient Type'))
    exit_date = models.DateField(auto_now=False, blank=True, null=True, verbose_name=_('Exit Date'))
    # ****************************************************************************
    start_date  = models.DateField(auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date    = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="patient_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="patient_last_updated_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name



@receiver(pre_save, sender='patient.Patient')
def save_barcode_image(sender, instance, **kwargs):
    barcode_dir       = os.path.join(settings.MEDIA_DIR, 'barcode')
    bar_code_name = instance.barcode
    EAN = barcode.get_barcode_class('code39')
    ean = EAN(bar_code_name, writer=ImageWriter())
    fullname = ean.save(os.path.join(barcode_dir,bar_code_name))
    file = open(f'{os.path.join(barcode_dir,bar_code_name)}.png', 'rb')
    instance.barcode_image = 'barcode/'+f'{bar_code_name}.png'
    # instance.barcode.save(f'{bar_code_name}.png', File(buffer), save=False)



class Patient_Exit(models.Model):
    exit_nature_list = [('better',_('Better')),
                        ('responsibility',_('Responsibility')),
                        ('scape',_('Scape'))]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, blank=True, null=True)
    exit_date = models.DateField(auto_now=False, blank=True, null=True, verbose_name=_('Exit Date'))
    exit_diagnosis = models.CharField(max_length=70,blank=True, null=True, verbose_name=_('Exit Diagnosis'))
    exit_nature = models.CharField(max_length=50,  choices=exit_nature_list, blank=True, null=True, verbose_name=_('Exit Nature'))
    physician = models.CharField(max_length=150, blank=True, null=True, verbose_name=_('Physician'))
    resident_doctor = models.CharField(max_length=150, blank=True, null=True, verbose_name=_('Resident Doctor'))
    exit_note = models.TextField(max_length=250, blank=True, null=True, verbose_name=_('Exit Note'))
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="exit_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="exit_last_updated_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)

    def save(self):
        patient_obj = Patient.objects.get(pk=self.patient.id)
        patient_obj.exit_date = self.exit_date
        patient_obj.save()
        super().save()

class Past_Medical_History(models.Model):
    anesthetic_list = [('GA',_('GA')),('SA',_('SA'))]
    thyroid_dysfunction_list = [('hypo',_('HYPO')),('hyper',_('HYPER'))]
    allergies_list_choices = [('food',_('طعام')),('med',_('ادوية')),('chemical',_('مواد كيميائية')),('chest',_('حساسية صدر')),('nose',_('جيوب أنفية')),]
    # ########################################################################################
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, blank=True, null=True)
    diabetes= models.BooleanField(default=False,blank=True, null=True, verbose_name=_('Diabetes'))
    pulmonar= models.BooleanField(default=False,blank=True, null=True, verbose_name=_('Pulmonary'))
    hypertension= models.BooleanField(default=False,blank=True, null=True, verbose_name=_('Hypertension'))
    allergies= models.BooleanField(default=False,blank=True, null=True, verbose_name=_('Allergies'))
    allergies_list= models.CharField(max_length=50, choices=allergies_list_choices, blank=True, null=True,)
    allergies_value= models.CharField(max_length=200, blank=True, null=True, verbose_name=_('Allergies Name'))
    heart_disease= models.BooleanField(default=False,blank=True, null=True, verbose_name=_('Heart Disease'))
    breast= models.BooleanField(default=False,blank=True, null=True, verbose_name=_('Breast'))
    autoimmun_disorder= models.BooleanField(default=False,blank=True, null=True, verbose_name=_('Autoimmun Disorder'))
    autoimmun_disorder_value = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('Autoimmun Disorder Type'))
    abnormal_pap= models.CharField(max_length=50, blank=True, null=True, verbose_name=_('Abnormal PAP'))
    kidney_disease= models.BooleanField(default=False,blank=True, null=True, verbose_name=_('Kidney Disease'))
    kidney_disease_value= models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Kidney Disease Type'))
    uterine= models.CharField(max_length=50, blank=True, null=True, verbose_name=_('Uterine'))
    psychiatric=models.BooleanField(default=False,blank=True, null=True, verbose_name=_('PSYCHIATRIC'))
    infertility= models.CharField(max_length=255, blank=True, null=True, verbose_name=_('INFERTILITY'))
    neurologic= models.BooleanField(default=False,blank=True, null=True, verbose_name=_('NEUROLOGIC'))
    rfh= models.CharField(max_length=50, blank=True, null=True, verbose_name=_('RFH'))
    hld= models.BooleanField(default=False,blank=True, null=True, verbose_name=_('HLD'))
    hld_value= models.CharField(max_length=20, blank=True, null=True, verbose_name=_('HLD Type'))
    gyns= models.CharField(max_length=255, blank=True, null=True, verbose_name=_('GYNS'))
    varicosities= models.BooleanField(default=False,blank=True, null=True, verbose_name=_('VARICOSITIES'))
    operation= models.CharField(max_length=255, blank=True, null=True, verbose_name=_('OPERATION'))
    thyroid_dysfunction = models.BooleanField(default=False,blank=True, null=True, verbose_name=_('THYROID DYSFUNCTION'))
    thyroid_dysfunction_value = models.CharField(max_length=20, choices=thyroid_dysfunction_list, blank=True, null=True, verbose_name=_('THYROID DYSFUNCTION Type'))
    anesthetic= models.CharField(max_length=20, choices=anesthetic_list, blank=True, null=True, verbose_name=_('ANESTHETIC'))
    trauma= models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Trauma'))
    history_of_blood_transfusion =  models.BooleanField(default=False,blank=True, null=True, verbose_name=_('History Of Blood Transfusion'))
    history_of_blood_transfusion_value = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('History Of Blood Transfusion Type'))
    othr= models.CharField(max_length=255, blank=True, null=True, verbose_name=_('other'))
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="medical_history_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="medical_history_last_updated_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.patient.name

def path_and_rename(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'patient_{0}/{1}'.format(instance.patient.id, filename)

class Patient_Files(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, blank=True, null=True)
    attachment_name = models.CharField(max_length=150, verbose_name=_('File Name'))
    attachment = models.FileField(upload_to=path_and_rename, null=True, blank=True, verbose_name=_('Attachment'))
    start_date  = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, default=date.today, verbose_name=_('Start Date'))
    end_date    = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="patient_attach_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="patient_attach_last_updated_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.patient.name

class Delivery(models.Model):
    delivery_type_list = [('n', 'NVD'), ('c', 'LSCS')]      # طبيعي او قيصري
    blood_type_list = [('A+', 'A+'), ('A-', 'A-'),('B+', 'B+'), ('B-', 'B-'),
                       ('O+', 'O+'), ('O-', 'O-'),('AB+', 'AB+'), ('AB-', 'AB-'),]
    fetal_sex_list = [('m',_('Male')),('f',_('Female')),('t',_('Twins'))]
    anesthesia_type_list = [('S','Spinal anesthesia'),('G','General anesthesia')]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('Patient'))
    description = models.CharField(max_length=250,blank=True, null=True, verbose_name=_('Delivery Notes'))
    type = models.CharField(max_length=30, blank=True, null=True,choices=delivery_type_list, verbose_name=_('Delivery Types'))
    place = models.CharField(max_length=100,blank=True, null=True, verbose_name=_('Delivery Hospital'))
    date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, default=date.today, verbose_name=_('Delivery Date'))
    anesthesia_type = models.CharField(max_length=50, choices=anesthesia_type_list, blank=True, null=True, verbose_name=_('Anesthesia Type'))
    anesthesia_doc = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('Anesthesia Doctor'))
    abo_rh  = models.CharField(max_length=50, choices=blood_type_list, blank=True, null=True, verbose_name=_('Blood Type'))
    fetal_sex  = models.CharField(max_length=50, choices=fetal_sex_list, blank=True, null=True, verbose_name=_('Fetal Sex'))
    lnmp    = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('Last Period Date'))
    end_date    = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="delivery_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="delivery_last_updated_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.patient.name +' ' + str(self.date)

class Check_Up(models.Model):
    exit_nature_list = [('better',_('Better')),
                        ('responsibility',_('Responsibility')),
                        ('scape',_('Scape'))]
    surgery_list = [('curettage_cleaning',_('Dilatation & Curettage')),
                        ('cervical_stitch',_('Cervical Cerclage')),
                        ('ectopic_pregnancy',_('Ectopic Pregnancy')),
                        ('CS',_('Cesarean Delivery')),]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('Patient'))
    week_number = models.CharField(max_length=3, blank=True, null=True,verbose_name=_('Week Number'))
    complain = models.CharField(max_length=200, blank=True, null=True,verbose_name=_('Complain'))
    visit_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('Visit date'))
    next_visit = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('Next visit date'))
    blood_presure = models.CharField(max_length=6, default='120/80', verbose_name=_('Blood presure'))
    protine = models.CharField(max_length=3, blank=True, null=True, verbose_name=_('Protine'))
    rbs = models.CharField(max_length=6, blank=True, null=True, verbose_name=_('RBS'))
    hemoglobin = models.CharField(max_length=10, blank=True, null=True, verbose_name=_('HB%'))
    placenta = models.CharField(max_length=10, blank=True, null=True, verbose_name=_('Placenta'))
    water = models.CharField(max_length=6, blank=True, null=True, verbose_name=_('Water'))
    fetal_position = models.CharField(max_length=10, blank=True, null=True, verbose_name=_('Fetal position'))
    fetal_movement = models.CharField(max_length=10, blank=True, null=True, verbose_name=_('Fetal movement'))
    fetal_heart_rate = models.CharField(max_length=10, blank=True, null=True, verbose_name=_('Fetal heart rate'))
    weight = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('Weight'))
    exit_nature = models.CharField(max_length=50,  choices=exit_nature_list, blank=True, null=True, verbose_name=_('Exit Nature'))
    exit_desc = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('Responsibility'))
    surgery = models.CharField(max_length=50,  choices=surgery_list, blank=True, null=True, verbose_name=_('Surgery'))
    surgery_desc = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('Surgery desc'))
    clexane_sarf_date  = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False, verbose_name=_('Clexane issue date'))
    mhx = models.TextField(max_length=255,blank=True, null=True, verbose_name=_('MHx'))
    shx = models.TextField(max_length=255,blank=True, null=True, verbose_name=_('SHx'))
    allergy_hx = models.TextField(max_length=255,blank=True, null=True, verbose_name=_('Allergy Hx'))
    ################################################################################################################
    start_date  = models.DateField(auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date    = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="check_up_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="check_up_last_updated_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.patient.name+' '+self.week_number

class Patient_Medicine(models.Model):
    check_up = models.ForeignKey(Check_Up, on_delete=models.CASCADE, verbose_name=_('Follow up'))
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, verbose_name=_('Medicine'))
    issue_date = models.DateField(auto_now=False, auto_now_add=False, default=date.today ,verbose_name=_('Issue date'))
    dose = models.PositiveIntegerField(verbose_name=_('Dose'))
    notes = models.CharField(max_length=250, blank=True, null=True,verbose_name=_('Notes'))
    # ###############################################################################################################
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="patient_med_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="patient_med_last_updated_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.medicine.trade_name

class Gynecology(models.Model):
    diagnosis_en = models.CharField(max_length=200, verbose_name=_('Diagnosis EN'))
    diagnosis_ar = models.CharField(max_length=200, verbose_name=_('Diagnosis AR'))
    start_date  = models.DateField(auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date    = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="gyno_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="gyno_last_updated_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.delivery.description

class Patient_Days_Off(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_day_off', verbose_name=_('Patient'))
    date_start  = models.DateField(auto_now=False, auto_now_add=False, verbose_name=_('Days-off Start Date'))
    date_end    = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('Days-off End Date'))
    num_of_days = models.PositiveIntegerField(verbose_name=_('Number of days'))
    notes = models.CharField(max_length=250, blank=True, null=True,verbose_name=_('Notes'))
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="patient_day_off_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="patient_day_off_last_updated_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)

    def save(self):
        self.num_of_days = (self.date_end-self.date_start).days+1
        super().save()

    def __str__(self):
        return self.patient.name+' '+self.num_of_days

class Ultrasound(models.Model):
    check_up = models.ForeignKey(Check_Up,blank=True, null=True, on_delete=models.CASCADE, verbose_name=_('Follow up'))
    prognosis = models.TextField(max_length=250, verbose_name=_('Prognosis'))
    visit_date = models.DateField(auto_now=False, auto_now_add=False, default=date.today ,verbose_name=_('Visit date'))
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="ultrasound_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="ultrasound_last_updated_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.prognosis

class Diabetes(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_diabetes', verbose_name=_('Patient'))
    bs = models.PositiveIntegerField(verbose_name=_('Blood sugar'))
    bp_up = models.PositiveIntegerField(default=120, verbose_name=_('BP Up'))
    bp_down = models.PositiveIntegerField(default=80, verbose_name=_('BP Down'))
    temp = models.PositiveIntegerField(default=37, verbose_name=_('Temprature'))
    reading_date = models.DateTimeField(auto_now=False, auto_now_add=False, default=datetime.now ,verbose_name=_('reading date'))
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="diabetes_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="diabetes_last_updated_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)
