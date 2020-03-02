from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.contrib.auth.decorators import login_required
from datetime import date
from surgery.forms import (Surgery_Inline, Surgery_Master_Form,
                           Patient_Surgery_Form, Surgery_Doctor_Form, doctor_Inline)
from surgery.models import Surgery_Master, Surgery_Steps, Patient_Surgery, Surgery_Doctor

@login_required(login_url='/login')
def list_surgery_view(request):
    all_surgery = Surgery_Master.objects.all()
    surgeryContext = {
                      'page_title':'',
                      'all_surgery':all_surgery
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
        "page_title": '',
        'master_form': master_form,
        'detail_fromset': detail_fromset,
    }
    return render(request, 'create-surgery.html', surgeryContext)
#dina
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
#dina
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
    patient_surgery_form = Patient_Surgery_Form()
    if request.method == 'POST':
        patient_surgery_form = Patient_Surgery_Form(request.POST)
        if patient_surgery_form.is_valid():
            master_obj = patient_surgery_form.save(commit=False)
            master_obj.patient = patient_id
            master_obj.created_by = request.user
            master_obj.last_update_by = request.user
            master_obj.save()
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
    surgeryContext = {
                      'page_title':'',
                      'all_doctors':all_doctors
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
    surgeryContext = {
                      'page_title':'اضافة دكتور جديد',
                      'doctor_form':doctor_form
    }
    return render(request, 'create-doctor.html', surgeryContext)
