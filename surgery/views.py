from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date
from patient.models import Patient
from surgery.forms import (Surgery_Inline, Surgery_Master_Form, Patient_Surgery_Form,
                           Surgery_Doctor_Form, doctor_Inline,After_Surgery_Form)
from surgery.models import Surgery_Master, Surgery_Steps, Patient_Surgery, Surgery_Doctor,After_Surgery
from django.utils.translation import ugettext_lazy as _


@login_required(login_url='/login')
def list_surgery_view(request):
    all_surgery = Surgery_Master.objects.all()
    master_form = Surgery_Master_Form()
    detail_fromset = Surgery_Inline()
    if request.method == 'POST':
        master_form = Surgery_Master_Form(request.POST)
        detail_fromset = Surgery_Inline(request.POST)
        if master_form.is_valid() and detail_fromset.is_valid():
            master_obj = master_form.save(commit=False)
            master_obj.created_by = request.user
            master_obj.last_update_by = request.user
            master_obj.save()
            detail_fromset = Surgery_Inline(
                request.POST, instance=master_obj)
            if detail_fromset.is_valid():
                det_obj = detail_fromset.save(commit=False)
                for obj in det_obj:
                    obj.created_by = request.user
                    obj.last_update_by = request.user
                    obj.save()
                    return redirect('surgery:list-surgery-types')
    surgeryContext = {
                      'page_title':_('قائمة الجراحات'),
                      "page_title_surgery": _('اضافة عملية جديدة'),
                      'all_surgery':all_surgery,
                      'master_form': master_form,
                      'detail_fromset': detail_fromset,
    }
    return render(request, 'list-surgery.html', surgeryContext)


@login_required(login_url='/login')
def create_surgery_view(request):
    master_form = Surgery_Master_Form()
    detail_fromset = Surgery_Inline()
    if request.method == 'POST':
        master_form = Surgery_Master_Form(request.POST)
        detail_fromset = Surgery_Inline(request.POST)
        if master_form.is_valid() and detail_fromset.is_valid():
            master_obj = master_form.save(commit=False)
            master_obj.created_by = request.user
            master_obj.last_update_by = request.user
            master_obj.save()
            detail_fromset = Surgery_Inline(
                request.POST, instance=master_obj)
            if detail_fromset.is_valid():
                det_obj = detail_fromset.save(commit=False)
                for obj in det_obj:
                    obj.created_by = request.user
                    obj.last_update_by = request.user
                    obj.save()
                    return redirect('surgery:list-surgery-types')
    surgeryContext = {
        "page_title": 'اضافة عملية جديدة',
        'master_form': master_form,
        'detail_fromset': detail_fromset,
    }
    return render(request, 'create-surgery.html', surgeryContext)


@login_required(login_url='/login')
def update_surgery_view(request, pk):
    required_surgery = get_object_or_404(Surgery_Master, pk=pk)
    surgery_master_form = Surgery_Master_Form(instance=required_surgery)
    surgery_det_form = Surgery_Inline(instance=required_surgery)
    if request.method == 'POST':
        surgery_master_form = Surgery_Master_Form(request.POST,instance=required_surgery)
        surgery_det_form = Surgery_Inline(request.POST,instance=required_surgery)
        if surgery_master_form.is_valid() and surgery_det_form.is_valid():
            surgery_master_form.save()
            surgery_det_obj = surgery_det_form.save(commit=False)
            for obj in surgery_det_obj:
                obj.created_by = request.user
                obj.last_update_by = request.user
                obj.save()
            return redirect('surgery:list-surgery-types')

    surgeryContext = {
        "page_title": 'تعديل بيانات عملية {}'.format(required_surgery),
        'master_form': surgery_master_form,
        'detail_fromset': surgery_det_form
    }
    return render(request, 'create-surgery.html', surgeryContext)


@login_required(login_url='/login')
def delete_surgery_view(request, pk):
    required_surgery = get_object_or_404(Surgery_Master, pk=pk)
    required_surgery.delete()
    return redirect('surgery:list-surgery-types')


@login_required(login_url='/login')
def view_surgery_view(request, pk):
    required_surgery = get_object_or_404(Surgery_Master, pk=pk)
    return render(request, 'view-surgery.html', {'surgery':required_surgery})


@login_required(login_url='/login')
def create_patient_surgery_view(request, patient_id):
    list_patient_surgery = Patient_Surgery.objects.filter(patient=patient_id)
    required_patient = get_object_or_404(Patient, id=patient_id)
    patient_surgery_form = Patient_Surgery_Form()
    if request.method == 'POST':
        patient_surgery_form = Patient_Surgery_Form(request.POST)
        if patient_surgery_form.is_valid():
            master_obj = patient_surgery_form.save(commit=False)
            master_obj.patient = required_patient
            master_obj.created_by = request.user
            master_obj.last_update_by = request.user
            master_obj.save()
            messages.success(request, 'تـــم التسجيل بنجــاح')
        else:
            messages.error(request, patient_surgery_form.errors)
    surgeryPatientContext = {
        "page_title": 'عمليات النسا',
        'patient_id':patient_id,
        'list_patient_surgery': list_patient_surgery,
        'patient_surgery_form': patient_surgery_form,
    }
    return render(request, 'create-patient-surgery.html', surgeryPatientContext)


@login_required(login_url='/login')
def list_surgery_doctor_view(request):
    all_doctors = Surgery_Doctor.objects.all()
    doctor_form = Surgery_Doctor_Form()
    # doctor_form = doctor_Inline(queryset=Surgery_Doctor.objects.none())
    if request.method == 'POST':
        # doctor_form = doctor_Inline(request.POST)
        doctor_form = Surgery_Doctor_Form(request.POST)
        if doctor_form.is_valid():
            master_obj = doctor_form.save(commit=False)
            # for x in master_obj:
            master_obj.hospital = request.user.clinic
            master_obj.created_by = request.user
            master_obj.last_update_by = request.user
            master_obj.save()
            return redirect('surgery:list-surgery-doctors')
            messages.success(request, _('Saved Successfully'))
        else:
            messages.error(request, doctor_form.errors)
    surgeryContext = {
                      'page_title':_('Doctors List'),
                      'all_doctors':all_doctors,
                      'page_title_doctor':_("Add New Doctor"),
                      'doctor_form':doctor_form
    }
    return render(request, 'list-doctors.html', surgeryContext)


@login_required(login_url='/login')
def create_surgery_doctor_view(request):
    doctor_form = doctor_Inline(queryset=Surgery_Doctor.objects.none())
    if request.method == 'POST':
        doctor_form = doctor_Inline(request.POST)
        if doctor_form.is_valid():
            master_obj = doctor_form.save(commit=False)
            for x in master_obj:
                x.hospital = request.user.clinic
                x.created_by = request.user
                x.last_update_by = request.user
                x.save()
            return redirect('surgery:list-surgery-doctors')
            messages.success(request, 'تـــم التسجيل بنجــاح')
        else:
            messages.error(request, doctor_form.errors)
    surgeryContext = {
                      'page_title':'اضافة دكتور جديد',
                      'doctor_form':doctor_form
    }
    return render(request, 'create-doctor.html', surgeryContext)

@login_required(login_url='/login')
def update_surgery_doctor_view(request,pk):
    required_doctor = get_object_or_404(Surgery_Doctor, pk=pk)
    doctor_form = Surgery_Doctor_Form(instance=required_doctor)
    if request.method == 'POST':
        doctor_form = Surgery_Doctor_Form(request.POST , instance=required_doctor)
        if doctor_form.is_valid():
            doctor_obj = doctor_form.save(commit=False)
            doctor_obj.created_by = request.user
            doctor_obj.last_update_by = request.user
            doctor_obj.save()
            return redirect('surgery:list-surgery-doctors')
            messages.success(request, 'تـــم التسجيل بنجــاح')
        else:
            messages.error(request, doctor_form.errors)
    surgeryContext = {
                      'page_title':_('EDIT {}').format(required_doctor.doctor_name),
                      'doctor_form':doctor_form
    }
    return render(request, 'update-doctors.html', surgeryContext)


@login_required(login_url='/login')
def delete_surgery_doctor_view(request, pk):
    required_doctor = get_object_or_404(Surgery_Doctor, pk=pk)
    required_doctor.delete()
    return redirect('surgery:list-surgery-doctors')

def create_after_surgery_view(request, surgery_id_v):
    after_surg_form = After_Surgery_Form()
    all_follow_ups = After_Surgery.objects.filter()
    if request.method == 'POST':
        after_surg_form = After_Surgery_Form(request.POST)
        if after_surg_form.is_valid():
            after_obj = after_surg_form.save(commit=False)
            after_obj.surgery = surgery_id_v
            after_obj.created_by = request.user
            after_obj.last_update_by = request.user
            after_obj.save()
            # return redirect('surgery:list-surgery-doctors')
            messages.success(request, 'تـــم التسجيل بنجــاح')
        else:
            messages.error(request, doctor_form.errors)
    surgeryContext = {
                      'page_title':'تسجيل متابعة مابعد العملية',
                      'after_surg_form':after_surg_form,
                      'all_follow_ups':all_follow_ups
    }
    return render(request, 'create-after-surgery.html', surgeryContext)
