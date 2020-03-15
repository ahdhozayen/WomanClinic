from django.conf import settings
from django.db import models
from datetime import datetime, date
from clinic.models import Clinic
from pharmacy.models import Medicine
from django.utils.translation import ugettext_lazy as _

class Patient(models.Model):
    transferred_list = [('insurance','عيادة تأمين'),('consultant','عيادة استشاري'),
                        ('outpatient','طبيب خارجي'),('patient','المريض نفسه')]
    hospital = models.ForeignKey(Clinic, on_delete=models.CASCADE, verbose_name='المستشفي')
    name = models.CharField(max_length=70, verbose_name='الأسم')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='العنوان')
    phone = models.CharField(max_length=255, blank=True, null=True, verbose_name='الهاتف')
    mobile = models.CharField(max_length=255, blank=True, null=True, verbose_name='المحمول')
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name='تاريخ الميلاد')
    job = models.CharField(max_length=30, verbose_name='الوظيفة')
    insurance_number = models.PositiveIntegerField(verbose_name='الرقم التأميني')
    entrance_number = models.PositiveIntegerField(verbose_name='رقم الدخول')
    hospital_number = models.PositiveIntegerField(verbose_name='رقم المستشفي الموحد')
    patient_number = models.PositiveIntegerField(verbose_name='رقم المريضة')
    room = models.CharField(max_length=70, verbose_name='الغرفة')
    hospital_section = models.CharField(max_length=70,blank=True, null=True, verbose_name='القسم')
    transferred_from = models.CharField(max_length=70, blank=True, null=True,choices=transferred_list ,verbose_name='المريضة محولة من')
    # ****************************************************************************
    clexane_order_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='رقم قرار صرف الكلكسان')
    entrance_date = models.DateField(auto_now=False, blank=True, null=True, verbose_name='تاريخ دخول المستشفي')
    patient_type_list = [('CHECK_UP','متابعة'), ('CONSULTANT','استشاري'), ('OPERATION','عمليات نسا'), ('DELIVER','ولادة')]
    patient_type = models.CharField(max_length=50, choices=patient_type_list, blank=True, null=True, verbose_name='طبيعة المريضة')
    exit_date = models.DateField(auto_now=False, blank=True, null=True, verbose_name='تاريخ الخروج')
    exit_note = models.TextField(max_length=250, blank=True, null=True,verbose_name=_('ملاحظات الخروج'))
    # ****************************************************************************
    start_date  = models.DateField(auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date    = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="patient_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="patient_last_updated_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name

class Patient_Exit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, blank=True, null=True)
    exit_date = models.DateField(auto_now=False, blank=True, null=True, verbose_name='تاريخ الخروج')
    exit_note = models.TextField(max_length=250, blank=True, null=True, verbose_name=_('ملاحظات الخروج'))
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="exit_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="exit_last_updated_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)

    def save(self):
        patient_obj = Patient.objects.get(pk=self.patient.id)
        patient_obj.exit_date = self.exit_date
        patient_obj.save()
        super().save()

def path_and_rename(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'patient_{0}/{1}'.format(instance.patient.id, filename)

class Patient_Files(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, blank=True, null=True)
    attachment_name = models.CharField(max_length=150, verbose_name=_('اسم المرفق'))
    attachment = models.FileField(upload_to=path_and_rename, null=True, blank=True, verbose_name=_('المرفقات'))
    start_date  = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, default=date.today, verbose_name=_('Start Date'))
    end_date    = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="patient_attach_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="patient_attach_last_updated_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.patient.name

class Delivery(models.Model):
    delivery_type_list = [('n', 'طبيعي'), ('c', 'قيصري')]
    blood_type_list = [('A+', 'A+'), ('A-', 'A-'),('B+', 'B+'), ('B-', 'B-'),
                       ('O+', 'O+'), ('O-', 'O-'),('AB+', 'AB+'), ('AB-', 'AB-'),]
    fetal_sex_list = [('m','ذكر'),('f','انثي'),('t','توأم')]
    anesthesia_type_list = [('S','Spinal anesthesia'),('G','General anesthesia')]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, blank=True, null=True, verbose_name='المريضة')
    description = models.CharField(max_length=250,blank=True, null=True, verbose_name='ملاحظات الولادة')
    type = models.CharField(max_length=30, blank=True, null=True,choices=delivery_type_list, verbose_name='نوع الولادة')
    place = models.CharField(max_length=100,blank=True, null=True, verbose_name='مكان الولادة')
    date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, default=date.today, verbose_name='تاريخ الولادة')
    anesthesia_type = models.CharField(max_length=50, choices=anesthesia_type_list, blank=True, null=True, verbose_name='نوع التخدير')
    anesthesia_doc = models.CharField(max_length=200, blank=True, null=True, verbose_name='دكتور التخدير')
    abo_rh  = models.CharField(max_length=50, choices=blood_type_list, blank=True, null=True, verbose_name='فصيلة الدم')
    fetal_sex  = models.CharField(max_length=50, choices=fetal_sex_list, blank=True, null=True, verbose_name='نوع المولود')
    lnmp    = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name='اخر تاريخ للدورة الشهرية')
    end_date    = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="delivery_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="delivery_last_updated_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.patient.name +' ' + str(self.date)

class Check_Up(models.Model):
    exit_nature_list = [('better','تحسن'),
                        ('responsibility','علي مسئولية'),
                        ('scape','هروب')]
    surgery_list = [('curettage_cleaning','كحت و تنظيف'),
                        ('cervical_stitch','غرزة بعنق الرحم'),
                        ('ectopic_pregnancy','حمل خارج الرحم'),
                        ('CS','ولادة قيصري'),]
    # delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, blank=True, null=True, verbose_name='الولادة')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, blank=True, null=True, verbose_name='المريضة')
    week_number = models.CharField(max_length=3, verbose_name='اسبوع الحمل')
    complain = models.CharField(max_length=200, verbose_name='شكوي المريضة')
    visit_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name='تاريخ الزيارة')
    next_visit = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name='تاريخ الزيارة القادم')
    blood_presure = models.CharField(max_length=6, default='120/80', verbose_name='ضغط الدم')
    protine = models.CharField(max_length=3, blank=True, null=True, verbose_name='البروتين')
    rbs = models.CharField(max_length=6, blank=True, null=True, verbose_name='rbs')
    hemoglobin = models.CharField(max_length=6, blank=True, null=True, verbose_name='Hb%')
    placenta = models.CharField(max_length=6, blank=True, null=True, verbose_name='المشيمة')
    water = models.CharField(max_length=6, blank=True, null=True, verbose_name='نسبة المياة')
    fetal_position = models.CharField(max_length=10, blank=True, null=True, verbose_name='وضعية الجنين')
    fetal_movement = models.CharField(max_length=10, blank=True, null=True, verbose_name='حركة الجنين')
    fetal_heart_rate = models.CharField(max_length=10, blank=True, null=True, verbose_name='ضربات قلب الجنين')
    weight = models.PositiveIntegerField(blank=True, null=True, verbose_name='وزن الجنين')
    exit_nature = models.CharField(max_length=50,  choices=exit_nature_list, blank=True, null=True, verbose_name='نوعية الخروج')
    exit_desc = models.CharField(max_length=200, blank=True, null=True, verbose_name='علي مسئولية من')
    surgery = models.CharField(max_length=50,  choices=surgery_list, blank=True, null=True, verbose_name='عمليات')
    surgery_desc = models.CharField(max_length=200, blank=True, null=True, verbose_name='شرح عمليات')
    clexane_sarf_date  = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False, verbose_name=_('تاريخ صرف الكلكسان'))
    mhx = models.TextField(max_length=255,blank=True, null=True, verbose_name='MHx')
    shx = models.TextField(max_length=255,blank=True, null=True, verbose_name='SHx')
    allergy_hx = models.TextField(max_length=255,blank=True, null=True, verbose_name='Allergy Hx')
    g = models.PositiveIntegerField(blank=True, null=True, verbose_name='G')
    p = models.PositiveIntegerField(blank=True, null=True, verbose_name='P')
    pre = models.PositiveIntegerField(blank=True, null=True, verbose_name='Pre')
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
    check_up = models.ForeignKey(Check_Up, on_delete=models.CASCADE, verbose_name='المتابعة')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, verbose_name='الدواء')
    issue_date = models.DateField(auto_now=False, auto_now_add=False, default=date.today ,verbose_name=_('تاريخ الصرف'))
    dose = models.PositiveIntegerField(verbose_name='الجرعة')
    notes = models.CharField(max_length=250, blank=True, null=True,verbose_name='ملاحظات')
    # ###############################################################################################################
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="patient_med_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="patient_med_last_updated_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.medicine.trade_name

class Gynecology(models.Model):
    diagnosis_en = models.CharField(max_length=200, verbose_name='التشخيص بالعربي')
    diagnosis_ar = models.CharField(max_length=200, verbose_name='التشخيص بالانجليزي')
    start_date  = models.DateField(auto_now=False, auto_now_add=False, default=date.today, verbose_name=_('Start Date'))
    end_date    = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('End Date'))
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="gyno_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="gyno_last_updated_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.delivery.description

class Patient_Days_Off(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_day_off', verbose_name=_('المريضة'))
    date_start  = models.DateField(auto_now=False, auto_now_add=False, verbose_name=_('تاريخ بداية الاجازة'))
    date_end    = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name=_('تاريخ نهاية الاجازة'))
    num_of_days = models.PositiveIntegerField()
    notes = models.CharField(max_length=250, blank=True, null=True,verbose_name='ملاحظات')
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
    check_up = models.ForeignKey(Check_Up,blank=True, null=True, on_delete=models.CASCADE, verbose_name='المتابعة')
    prognosis = models.TextField(max_length=250, verbose_name=_('التشخيص'))
    visit_date = models.DateField(auto_now=False, auto_now_add=False, default=date.today ,verbose_name=_('تاريخ الزيارة'))
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="ultrasound_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="ultrasound_last_updated_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.prognosis

class Diabetes(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_diabetes', verbose_name=_('المريضة'))
    bs = models.PositiveIntegerField(verbose_name=_('قياس السكر'))
    bp = models.CharField(max_length=10, verbose_name=_('قياس الضغط'))
    temp = models.PositiveIntegerField(default=37, verbose_name=_('درجة الحرارة'))
    reading_date = models.DateTimeField(auto_now=False, auto_now_add=False, default=datetime.now() ,verbose_name=_('تاريخ القراءة'))
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="diabetes_created_by")
    creation_date = models.DateField(auto_now=True, auto_now_add=False)
    last_update_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name="diabetes_last_updated_by")
    last_update_date = models.DateField(auto_now=False, auto_now_add=True)
