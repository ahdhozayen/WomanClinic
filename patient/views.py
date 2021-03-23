import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.contrib.auth.decorators import login_required
from datetime import date
from django.http import JsonResponse, HttpResponse, Http404
from django.contrib import messages
from patient.models import (Patient, Patient_Files, Delivery, Check_Up,
                            Gynecology, Patient_Medicine, Patient_Days_Off,
                            Ultrasound, Diabetes, Patient_Exit, Past_Medical_History)
from patient.forms import (PatientForm, Patient_Files_formset,
                           DeliveryForm, Delivery_Check_Up_formset,
                           Gynecology_formset, GynecologyForm,
                           Check_Up_Form, Patient_Medicine_formset,
                           Patient_Days_Off_formset, Ultrasound_Form,
                           Diabetes_Form, Patient_Exit_Form, Past_Medical_History_Form)
from django.utils.translation import ugettext_lazy as _


@login_required(login_url='/login')
def list_patients_view(request):
    all_patients = Patient.objects.all()
    return render(request, 'list-patients.html', context={'page_title':_('All Patients'),'all_patients':all_patients})

@login_required(login_url='/login')
def create_patient_view(request):
    patient_form = PatientForm(form_type='create',)
    patient_attachments = Patient_Files_formset()
    patient_past_med = Past_Medical_History_Form(form_type='create',)
    if request.method == 'POST':
        patient_form = PatientForm(request.POST, form_type='create')
        patient_attachments = Patient_Files_formset(request.POST, request.FILES)
        patient_past_med = Past_Medical_History_Form(request.POST, form_type='create')
        if patient_form.is_valid() and patient_attachments.is_valid() and patient_past_med.is_valid():
            master_obj = patient_form.save(commit=False)
            master_obj.hospital_id = request.user.clinic_id
            master_obj.barcode = master_obj.insurance_number
            master_obj.created_by = request.user
            master_obj.last_update_by = request.user
            master_obj.save()
            patient_attachments = Patient_Files_formset(request.POST, request.FILES, instance=master_obj)
            detail_obj = patient_attachments.save(commit=False)
            for x in detail_obj:
                x.created_by = request.user
                x.last_update_by = request.user
                x.save()
            past_med_obj = patient_past_med.save(commit=False)
            past_med_obj.patient = master_obj
            past_med_obj.created_by = request.user
            past_med_obj.last_update_by = request.user
            past_med_obj.save()
            if master_obj.patient_type == 'DELIVER' :
                messages.success(request, 'تم الحفظ بنجاح')
                return redirect('patient:all-delivery', pk=master_obj.id)
            elif master_obj.patient_type == 'OPERATION'  :
                messages.success(request, 'تم الحفظ بنجاح')
                return redirect('surgery:create-patient-surgery', patient_id=master_obj.id)
            else :
                messages.success(request, 'تم الحفظ بنجاح')
                return redirect('patient:all-checkup', patient_id=master_obj.id)
        else:
            if patient_form.errors:
                messages.error(request, patient_form.errors)
            elif patient_attachments.errors:
                for error in patient_attachments.errors:
                    messages.error(request, error)
            elif patient_past_med.errors:
                messages.error(request, patient_past_med.errors)
    createContext = {
                     'page_title':_('ADD NEW PATIENT'),
                     'patient_form':patient_form,
                     'patient_attachments':patient_attachments,
                     'patient_past_med':patient_past_med,
    }
    return render(request, 'create-patient.html', createContext)

@login_required(login_url='/login')
def view_patient_view(request, pk):
    required_patient = get_object_or_404(Patient, pk=pk)
    patient_form = PatientForm(form_type='view', instance=required_patient)
    patient_attachments = Patient_Files.objects.filter(patient = pk)
    required_patient_past_med = Past_Medical_History.objects.filter(patient = pk).first()
    patient_past_med = Past_Medical_History_Form(form_type='view', instance=required_patient_past_med)
    # patient_attachments = Patient_Files_formset(instance=required_patient)
    exit_form = Patient_Exit_Form()
    if request.method == 'POST':
        exit_form = Patient_Exit_Form(request.POST)
        if exit_form.is_valid():
            exit_obj = exit_form.save(commit=False)
            exit_obj.patient = required_patient
            exit_obj.created_by = request.user
            exit_obj.last_update_by = request.user
            exit_obj.save()
            return redirect('patient:view-patient', pk=pk)
    createContext = {
                     'page_title':_('FOLLOW UP MAIN PAGE'),
                     'patient_id':pk,
                     'patient_form':patient_form,
                     'patient_attachments':patient_attachments,
                     'patient_past_med':patient_past_med,
                     'media_url':settings.MEDIA_URL,
                     'exit_form':exit_form,
                     'required_patient':required_patient
    }
    return render(request, 'view-patient.html', createContext)


@login_required(login_url='/login')
def view_patient_barcode(request):
    if request.method == "POST":
        url_code = request.POST.get('barcode')
        truncated_barcode = url_code[:-1]
        try:
            required_patient = get_object_or_404(Patient, barcode=truncated_barcode)
            return redirect('patient:view-patient', pk= required_patient.pk)
        except Http404:
            raise


@login_required(login_url='/login')
def update_patient_view(request, pk):
    required_patient = Patient.objects.get(pk=pk)
    patient_form = PatientForm(form_type='update', instance=required_patient)
    required_patient_past_med = Past_Medical_History.objects.filter(patient = pk).first()
    patient_past_med = Past_Medical_History_Form(form_type='update', instance=required_patient_past_med)
    patient_attachments = Patient_Files_formset(instance=required_patient)
    if request.method == 'POST':
        patient_form = PatientForm(request.POST, form_type='update', instance=required_patient)
        patient_past_med = Past_Medical_History_Form(request.POST, form_type='update', instance=required_patient)
        patient_attachments = Patient_Files_formset(request.POST, request.FILES, instance=required_patient)
        if patient_form.is_valid() and patient_attachments.is_valid() and patient_past_med.is_valid():
            master_obj = patient_form.save(commit=False)
            master_obj.created_by = request.user
            master_obj.barcode = master_obj.insurance_number
            master_obj.last_update_by = request.user
            master_obj.save()
            patient_attachments = Patient_Files_formset(request.POST, request.FILES, instance=master_obj)
            detail_obj = patient_attachments.save(commit=False)
            for x in detail_obj:
                x.created_by = request.user
                x.last_update_by = request.user
                x.save()
            past_med_obj = patient_past_med.save(commit=False)
            past_med_obj.patient = master_obj
            past_med_obj.created_by = request.user
            past_med_obj.last_update_by = request.user
            past_med_obj.save()
            messages.success(request, 'تم الحفظ بنجاح')
            return redirect('patient:view-patient', pk=master_obj.id)
        else:
            print(patient_form.errors)
            messages.error(request, patient_form.errors)
            messages.error(request, patient_past_med.errors)
            for error in patient_attachments.errors:
                messages.error(request, error)
    createContext = {
                     'page_title':_('EDIT PATIENT {}').format(required_patient),
                     'patient_form':patient_form,
                     'patient_past_med':patient_past_med,
                     'patient_id':pk,
                     'patient_attachments':patient_attachments,
    }
    return render(request, 'create-patient.html', createContext)

@login_required(login_url='/login')
def delete_patient(request, pk):
    required_patient = get_object_or_404(Patient, pk=pk)
    required_patient.delete()
    return redirect('patient:all-patients')


@login_required(login_url='/login')
def list_gyno_view(request):
    all_gyno = Gynecology.objects.all()
    gyno_formset = GynecologyForm()
    if request.method == 'POST':
        gyno_formset = GynecologyForm(request.POST)
        if gyno_formset.is_valid():
            gyno_obj = gyno_formset.save(commit=False)
            # for x in gyno_obj:
            gyno_obj.created_by = request.user
            gyno_obj.last_update_by = request.user
            gyno_obj.save()
            return redirect("patient:all-gynos")
        else:
            print(gyno_formset.errors)
    gyno_context={
             'page_title':_('GYN LIST'),
             'page_title_gyno':_('GYN DIAGNOSIS'),
             'all_gyno':all_gyno,
             'gyno_form':gyno_formset,
             }
    return render(request, 'gyno/list-gyno.html', gyno_context)

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
        else:
            print(gyno_formset.errors)
    gynoContext = {
                     'page_title_gyno':_('تشخيص امراض النسا'),
                     'gyno_form':gyno_formset,
    }
    return render(request, 'gyno/create-gyno.html', gynoContext)

@login_required(login_url='/login')
def update_gyno_view(request, pk):
    required_gyno = get_object_or_404(Gynecology, pk=pk)
    gyno_form = GynecologyForm(instance=required_gyno)
    if request.method == 'POST':
        gyno_form = GynecologyForm(request.POST,instance=required_gyno)
        if gyno_form.is_valid():
            gyno_obj = gyno_form.save(commit=False)
            gyno_obj.created_by = request.user
            gyno_obj.last_update_by = request.user
            gyno_obj.save()
    gynoContext = {
                     'page_title':_('EDIT {}').format(required_gyno.diagnosis_en),
                     'gyno_form':gyno_form,
    }
    return render(request, 'gyno/update-gyno.html', gynoContext)


@login_required(login_url='/login')
def delete_gyno_view(request, pk):
    required_gyno = get_object_or_404(Gynecology, pk=pk)
    required_gyno.delete()
    return redirect('patient:all-gynos')

@login_required(login_url='/login')
def list_delivery_view(request, pk):
    patient_delivery = Delivery.objects.filter(patient=pk)
    return render(request, 'delivery/list-delivery.html', context={'page_title':_('DELIVERY INFORMATIONS'),'patient_delivery':patient_delivery})

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
                         'page_title':_('DELIVERY MAIN PAGE'),
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
                        'page_title':_('EDIT DELIVERY INFORMATIONS FOR  {}').format(required_patient),
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
                    'page_title':_('FOLLOW UP PAGE'),
                    'patient_id':patient_id,
                    'list_checkups':list_checkups,
                    'check_up_form':check_up_form,
    }
    return render(request, 'check-up/create-check-up.html', checkContext)

@login_required(login_url='/login')
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
            messages.success(request, _('SAVED SUCCESSFULLY'))
            return redirect('patient:all-checkup', patient_id=patient_id)
        else:
            messages.error(request, us_form.errors)
    ultraSoundContext = {
                         'page_title':_('ULTRASOUND READINGS FOR {}').format(required_check),
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
                    'page_title':_('FOLLOW UP WEEK {}').format(chk_id),
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
            messages.success(request, _('SAVED SUCCESSFULLY'))
            check_up_form = Check_Up_Form(form_type='update',)
    checkContext = {
                    'page_title':_('EDIT FOLLOW UP FOR {}').format(required_patient),
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
                messages.success(request, _('SAVED SUCCESSFULLY'))

    medContext = {
                    'page_title':_('DISPENSING MEDICINES'),
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
                    'page_title':_('EDIT MEDICINES FOR {}').format(required_checkup),
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
                       'page_title':_('CONSULTANT PATIENTS LIST'),
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
                messages.success(request, _('SAVED SUCCESSFULLY'))

    offContext = {
                  'page_title':_('DAYS OFF FOR PATIENT {}').format(required_patient),
                  'days_formset':days_formset,
                  'patient_id':patient_id,
    }
    return render(request, 'create-days-off.html', offContext)

@login_required(login_url='/login')
def create_diabetes_view(request, patient_id):
    required_patient = Patient.objects.get(id = patient_id)
    list_diabetes = Diabetes.objects.filter(patient=patient_id)
    diabete_form = Diabetes_Form()
    if request.method == 'POST':
        diabete_form = Diabetes_Form(request.POST)
        if diabete_form.is_valid():
            diabete_obj = diabete_form.save(commit=False)
            diabete_obj.patient = required_patient
            diabete_obj.created_by = request.user
            diabete_obj.last_update_by = request.user
            diabete_obj.save()
            messages.success(request, _('SAVED SUCCESSFULLY'))
            return redirect('patient:create-diabetes', patient_id=patient_id)
    diabeteContext = {
                  'page_title':_('BLOOD SUGAR & PRESSURE READINGS FOR PATIENT {}').format(required_patient),
                 'required_patient':required_patient,
                 'list_diabetes':list_diabetes,
                 'diabete_form':diabete_form
    }
    return render(request, 'diabetes.html', diabeteContext)

@login_required(login_url='/login')
def patient_diabete_chart(request, patient_id):
    labels = []
    bs = []
    bp_up = []
    bp_down = []
    chart_diabetes = Diabetes.objects.filter(patient=patient_id)
    for x in chart_diabetes:
        labels.append(x.reading_date.month)
        bs.append(x.bs)
        bp_up.append(x.bp_up)
        bp_down.append(x.bp_down)
    data = {
        'labels': labels,
        'bs': bs,
        'bp_up': bp_up,
        'bp_down' : bp_down
    }
    return JsonResponse(data)
