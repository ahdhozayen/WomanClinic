import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.contrib.auth.decorators import login_required
from datetime import date
from django.contrib import messages
from patient.models import (Patient, Patient_Files, Delivery, Check_Up,
                            Gynecology, Patient_Medicine, Patient_Days_Off, Ultrasound)
from patient.forms import (PatientForm, Patient_Files_formset,
                           DeliveryForm, Delivery_Check_Up_formset,
                           Gynecology_formset, GynecologyForm,
                           Check_Up_Form, Patient_Medicine_formset,
                           Patient_Days_Off_formset, Ultrasound_Form)


@login_required(login_url='/login')
def list_patients_view(request):
    all_patients = Patient.objects.all()
    return render(request, 'list-patients.html', context={'page_title':'عرض المريضات','all_patients':all_patients})

@login_required(login_url='/login')
def create_patient_view(request):
    patient_form = PatientForm(form_type='create',)
    patient_attachments = Patient_Files_formset()
    if request.method == 'POST':
        patient_form = PatientForm(request.POST, form_type='create')
        patient_attachments = Patient_Files_formset(request.POST, request.FILES)
        if patient_form.is_valid() and patient_attachments.is_valid():
            master_obj = patient_form.save(commit=False)
            master_obj.hospital_id = request.user.clinic_id
            master_obj.created_by = request.user
            master_obj.last_update_by = request.user
            master_obj.save()
            patient_attachments = Patient_Files_formset(request.POST, request.FILES, instance=master_obj)
            detail_obj = patient_attachments.save(commit=False)
            for x in detail_obj:
                x.created_by = request.user
                x.last_update_by = request.user
                x.save()
            return redirect('patient:all-checkup', patient_id=master_obj.id)
        else:
            if patient_form.errors:
                messages.error(request, patient_form.errors)
            elif patient_attachments.errors:
                for error in patient_attachments.errors:
                    messages.error(request, error)
    createContext = {
                     'page_title':'تسجيل مريضة جديدة',
                     'patient_form':patient_form,
                     'patient_attachments':patient_attachments,
    }
    return render(request, 'create-patient.html', createContext)

@login_required(login_url='/login')
def view_patient_view(request, pk):
    required_patient = Patient.objects.get(pk=pk)
    patient_form = PatientForm(form_type='view', instance=required_patient)
    patient_attachments = Patient_Files.objects.filter(patient = pk)
    # patient_attachments = Patient_Files_formset(instance=required_patient)
    createContext = {
                     'page_title':'شاشة المتابعة الرئيسية',
                     'patient_id':pk,
                     'patient_form':patient_form,
                     'patient_attachments':patient_attachments,
                     'media_url':settings.MEDIA_URL,
    }
    return render(request, 'view-patient.html', createContext)

@login_required(login_url='/login')
def update_patient_view(request, pk):
    required_patient = Patient.objects.get(pk=pk)
    patient_form = PatientForm(form_type='update', instance=required_patient)
    patient_attachments = Patient_Files_formset(instance=required_patient)
    if request.method == 'POST':
        patient_form = PatientForm(request.POST, form_type='update', instance=required_patient)
        patient_attachments = Patient_Files_formset(request.POST, request.FILES, instance=required_patient)
        if patient_form.is_valid() and patient_attachments.is_valid():
            master_obj = patient_form.save(commit=False)
            # master_obj.created_by = request.user
            master_obj.last_update_by = request.user
            master_obj.save()
            patient_attachments = Patient_Files_formset(request.POST, request.FILES, instance=master_obj)
            detail_obj = patient_attachments.save(commit=False)
            for x in detail_obj:
                # initial_name = x.attachment.name
                # new_name = str(x.patient.id)+'-'+str(x.patient.insurance_number)+'-'+x.attachment.name
                x.created_by = request.user
                x.last_update_by = request.user
                x.save()
        else:
            if patient_form.errors:
                messages.error(request, patient_form.errors)
            elif patient_attachments.errors:
                for error in patient_attachments.errors:
                    messages.error(request, error)
    createContext = {
                     'page_title':'تعديل المريضة {}'.format(required_patient),
                     'patient_form':patient_form,
                     'patient_id':pk,
                     'patient_attachments':patient_attachments,
    }
    return render(request, 'create-patient.html', createContext)

@login_required(login_url='/login')
def list_gyno_view(request):
    all_gyno = Gynecology.objects.all()
    return render(request, 'gyno/list-gyno.html',  context={'page_title':'أمراض النسا','all_gyno':all_gyno})

@login_required(login_url='/login')
def create_gyno_view(request):
    gyno_formset = GynecologyForm()
    # gyno_formset = Gynecology_formset(queryset = Gynecology.objects.none())
    if request.method == 'POST':
        gyno_formset = GynecologyForm(request.POST)
        if gyno_formset.is_valid():
            gyno_obj = gyno_formset.save(commit=False)
            # for x in gyno_obj:
            gyno_obj.created_by = request.user
            gyno_obj.last_update_by = request.user
            gyno_obj.save()
            return redirect("patient:create-gyno")
    gynoContext = {
                     'page_title':'تشخيص امراض النسا',
                     'gyno_form':gyno_formset,
    }
    return render(request, 'gyno/create-gyno.html', gynoContext)

@login_required(login_url='/login')
def update_gyno_view(request, pk):
    required_gyno = get_object_or_404(Gynecology, pk=pk)
    gyno_form = GynecologyForm(instance=required_gyno)
    if request.method == 'POST':
        gyno_form = GynecologyForm(request.POST)
        if gyno_form.is_valid():
            gyno_obj = gyno_formset.save(commit=False)
            # for x in gyno_obj:
            gyno_obj.created_by = request.user
            gyno_obj.last_update_by = request.user
            gyno_obj.save()
    gynoContext = {
                     'page_title':'تعديل {}'.format(required_gyno.diagnosis_en),
                     'gyno_form':gyno_form,
    }
    return render(request, 'gyno/create-gyno.html', gynoContext)

@login_required(login_url='/login')
def list_delivery_view(request, pk):
    patient_delivery = Delivery.objects.filter(patient=pk)
    return render(request, 'delivery/list-delivery.html', context={'page_title':'بيانات الولادة','patient_delivery':patient_delivery})

@login_required(login_url='/login')
def create_delivery_view(request, pk):
    delivery_form = DeliveryForm()
    patient_delivery = Delivery.objects.filter(patient=pk)
    if request.method == 'POST':
        delivery_form = DeliveryForm(request.POST)
        if delivery_form.is_valid():
            delivery_obj = delivery_form.save(commit=False)
            delivery_obj.patient_id = pk
            delivery_obj.created_by = request.user
            delivery_obj.last_update_by = request.user
            delivery_obj.save()
            delivery_form = DeliveryForm()
            return redirect('patient:view-patient', pk=pk)
        else:
            if delivery_form.errors:
                messages.error(request, patient_form.errors)
    delivery_context = {
                         'page_title':'شاشة الولادة الرئيسية',
                         'patient_id':pk,
                         'delivery_form':delivery_form,
                         'patient_delivery':patient_delivery,
    }
    return render(request, 'delivery/create-delivery.html', delivery_context)

@login_required(login_url='/login')
def update_delivery_view(request, pk, patient_id):
    required_delivery = Delivery.objects.get(pk=pk)
    delivery_form = DeliveryForm(instance=required_delivery)
    required_patient = Patient.objects.get(pk=patient_id)
    patient_delivery = Delivery.objects.filter(patient=patient_id)
    if request.method == 'POST':
        delivery_form = DeliveryForm(request.POST, instance=required_delivery)
        if delivery_form.is_valid():
            delivery_obj = delivery_form.save(commit=False)
            delivery_obj.patient_id = patient_id
            delivery_obj.created_by = required_delivery.created_by
            delivery_obj.last_update_date = date.today()
            delivery_obj.last_update_by = request.user
            delivery_obj.save()
        delivery_form = DeliveryForm()
    delivery_context = {
                        'page_title':'تعديل بيانات الولادة للمريضة {}'.format(required_patient),
                        'patient_id':patient_id,
                         'delivery_form':delivery_form,
                         'patient_delivery':patient_delivery,
    }
    return render(request, 'delivery/create-delivery.html', delivery_context)

@login_required(login_url='/login')
def create_list_check_up_view(request, patient_id):
    list_checkups = Check_Up.objects.filter(patient=patient_id)
    # latest_delivery = Delivery.objects.filter(patient=patient_id).latest('date')
    check_up_form = Check_Up_Form(form_type='create')
    if request.method == 'POST':
        check_up_form = Check_Up_Form(request.POST,form_type='create')
        if check_up_form.is_valid():
            master_obj = check_up_form.save(commit=False)
            # master_obj.delivery.id = 0
            master_obj.patient_id = patient_id
            master_obj.created_by = request.user
            master_obj.last_update_by = request.user
            master_obj.save()
    checkContext = {
                    'page_title':'شاشة المتابعة',
                    'patient_id':patient_id,
                    'list_checkups':list_checkups,
                    'check_up_form':check_up_form,
    }
    return render(request, 'check-up/create-check-up.html', checkContext)


def ultrasound_create_view(request, check_id, patient_id):
    us_form = Ultrasound_Form()
    required_check = Check_Up.objects.get(id =check_id)
    list_us = Ultrasound.objects.filter(check_up=check_id)
    if request.method == 'POST':
        us_form = Ultrasound_Form(request.POST)
        if us_form.is_valid():
            us_object = us_form.save(commit=False)
            us_object.check_up = required_check
            us_object.created_by = request.user
            us_object.last_update_by = request.user
            us_object.save()
            messages.success(request, 'تـــم التسجيل بنجــاح')
            return redirect('patient:all-checkup', patient_id=patient_id)
        else:
            messages.error(request, us_form.errors)
    ultraSoundContext = {
                         'page_title':'تسجيل قراءة السونار للمتابعة {}'.format(required_check),
                         'patient_id':patient_id,
                         'us_form':us_form,
                         'list_us':list_us,
    }
    return render(request, 'check-up/create-ultrasound.html', ultraSoundContext)

@login_required(login_url='/login')
def view_list_check_up_view(request, chk_id, patient_id):
    list_checkups = Check_Up.objects.filter(patient=patient_id)
    list_patient_med = Patient_Medicine.objects.filter(check_up=chk_id)
    required_checkup = get_object_or_404(Check_Up,patient=patient_id, id=chk_id)
    check_up_form = Check_Up_Form(form_type='view', instance=required_checkup)
    checkContext = {
                    'page_title':'بيانات متابعة الاسبوع {}'.format(chk_id),
                    'patient_id':patient_id,
                    'list_patient_med':list_patient_med,
                    'check_up_form':check_up_form,
    }
    return render(request, 'check-up/view-check-up.html', checkContext)

@login_required(login_url='/login')
def update_list_check_up_view(request, chk_id, pk):
    list_checkups = Check_Up.objects.filter(patient=pk)
    required_patient = get_object_or_404(Patient, pk=pk)
    required_checkup = get_object_or_404(Check_Up,patient=pk, week_number=chk_id)
    check_up_form = Check_Up_Form(form_type='update', instance=required_checkup)
    if request.method == 'POST':
        check_up_form = Check_Up_Form(request.POST,form_type='update', instance=required_checkup)
        if check_up_form.is_valid():
            master_obj = check_up_form.save(commit=False)
            master_obj.patient_id = pk
            # master_obj.created_by = request.user
            master_obj.last_update_by = request.user
            master_obj.save()
            check_up_form = Check_Up_Form(form_type='update',)
    checkContext = {
                    'page_title':'تعديل بيانات متابعة المريضة {}'.format(required_patient),
                    'patient_id':pk,
                    'list_checkups':list_checkups,
                    'check_up_form':check_up_form,
    }
    return render(request, 'check-up/create-check-up.html', checkContext)

@login_required(login_url='/login')
def create_patient_medicine_view(request, patient_id, chk_id):
    required_patient = Patient.objects.get(id = patient_id)
    patient_med = Patient_Medicine_formset(queryset= Patient_Medicine.objects.none())
    if request.method=='POST':
        patient_med = Patient_Medicine_formset(request.POST)
        if patient_med.is_valid():
            med_obj = patient_med.save(commit=False)
            for x in med_obj:
                x.check_up_id = chk_id
                x.created_by = request.user
                x.last_update_by = request.user
                x.save()
    medContext = {
                    'page_title':'صرف ادوية ',
                    'patient_id':required_patient,
                    'patient_med':patient_med,
    }
    return render(request, 'check-up/create-med.html', medContext)

@login_required(login_url='/login')
def update_patient_medicine_view(request, patient_id, chk_id):
    required_checkup = get_object_or_404(Check_Up, id=chk_id)
    check_up_form = Check_Up_Form(form_type='update', instance=required_checkup)
    patient_med = Patient_Medicine_formset(queryset=Patient_Medicine.objects.filter(check_up=chk_id))
    required_patient = Patient.objects.get(id = patient_id)
    medContext = {
                    'page_title':'تعديل بيانات المتابعة {}'.format(required_checkup),
                    'patient_id':required_patient,
                    'patient_med':patient_med,
                    'check_up_form': check_up_form,
                    'required_patient': required_patient,
    }
    return render(request, 'check-up/update-check-up.html', medContext)

@login_required(login_url='/login')
def list_patient_consultant_view(request):
    all_patients = Patient.objects.filter(transferred_from ='consultant')
    consultantContext={
                       'page_title':'متابعة الاستشاري',
                       'all_patients':all_patients,
    }
    return render(request, 'consultant/list-patient.html', consultantContext)

@login_required(login_url='/login')
def create_patient_days_off_view(request, patient_id):
    required_patient = Patient.objects.get(id = patient_id)
    days_formset = Patient_Days_Off_formset(queryset= Patient_Days_Off.objects.none())
    if request.method == 'POST':
        days_formset = Patient_Days_Off_formset(request.POST)
        if days_formset.is_valid():
            days_obj = days_formset.save(commit=False)
            for x in days_obj:
                x.patient = required_patient
                x.created_by = request.user
                x.last_update_by = request.user
                x.save()
    offContext = {
                  'page_title':' تسجيل اجازات لـ {}'.format(required_patient),
                  'days_formset':days_formset,
                  'patient_id':patient_id,
    }
    return render(request, 'create-days-off.html', offContext)
