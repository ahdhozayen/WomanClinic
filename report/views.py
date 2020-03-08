from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from datetime import date
from django.db.models import Count
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from patient.models import Patient, Delivery, Check_Up, Gynecology, Patient_Medicine, Patient_Days_Off
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions


@login_required(login_url='/login')
def report_dashboard_view(request):
    patient_count = Patient.objects.all().count()
    patient_exit_chart = Patient.objects.filter(exit_date__isnull=False)
    patients_consult_count = Patient.objects.filter(transferred_from__isnull = False).count()
    patients_clexane_count = Patient.objects.filter(clexane_order_number__isnull = False).count()
    labels = []
    chart_data = []
    for x in patient_exit_chart.values('exit_date').annotate(num_of_exit_patient = Count('exit_date')):
        labels.append(x['exit_date'].month)
        chart_data.append(x['num_of_exit_patient'])
    repContext={
                'page_title':'شاشة التقارير الرئيسية',
                'patient_count':patient_count,
                'patients_consult_count':patients_consult_count,
                'patients_clexane_count':patients_clexane_count,
                'patient_exit_chart':patient_exit_chart,
                "labels":labels,
                "chart_data":chart_data,
    }
    return render(request, 'report-dashboard.html', repContext)

@login_required(login_url='/login')
def list_all_patients_view(request):
    all_patients = Patient.objects.all()
    context={'page_title':'شاشة تقارير كافة المريضات',
             'all_patients':all_patients
             }
    return render(request, 'list-all-patients-report.html', context=context)

@login_required(login_url='/login')
def view_patient_history_view(request, patient_id):
    # patient info
    required_patient = get_object_or_404(Patient, id = patient_id)
    # patient medicine
    patient_check_ups = Check_Up.objects.filter(patient = patient_id)
    patient_medicine = Patient_Medicine.objects.filter(check_up__in = patient_check_ups)
    # patient days off
    patient_days_off = Patient_Days_Off.objects.filter(patient = patient_id)
    context={'page_title':'تقرير عام عن المريضة  {}'.format(required_patient),
             'required_patient':required_patient,
             'patient_medicine':patient_medicine,
             'patient_days_off':patient_days_off,
             }
    return render(request, 'patient-history-report.html', context=context)

@login_required(login_url='/login')
def list_consultant_patients_view(request):
    all_patients = Patient.objects.filter(transferred_from__isnull = False)
    context={'page_title':'عرض المريضات',
             'all_patients':all_patients
             }
    return render(request, 'list-cons-patients-report.html', context=context)

@login_required(login_url='/login')
def list_clexane_patients_view(request):
    all_patients = Patient.objects.filter(clexane_order_number__isnull = False)
    context={'page_title':'مريضات الكلكسان',
             'all_patients':all_patients
             }
    return render(request, 'list-clexane-patients-report.html', context=context)

@login_required(login_url='/login')
def total_patients_details_view(request):
    all_patients = Patient.objects.filter(transferred_from__isnull = False)
    context={'page_title':'احصائيات عن اجمالي المريضات',
             'all_patients':all_patients
             }
    return render(request, 'total-patients-details.html', context=context)

@login_required(login_url='/login')
def list_surgery_patients_view(request):
    surgery_patients = Patient_Surgery.objects.all()
    context={'page_title':'مريضات العمليات',
             'surgery_patients':surgery_patients
             }
    return render(request, 'list-patients.html', context=context)

@login_required(login_url='/login')
def list_surgery_patients_view(request):
    days_off_patients = Patient_Days_Off.objects.all()
    context={'page_title':'اجازات المرضي',
             'days_off_patients':days_off_patients
             }
    return render(request, 'list-patients.html', context=context)

# def pie_chart(request):
#     labels = []
#     data = []
#     queryset = Patient.objects.filter()
#     for x in queryset:
#         labels.append(x.entrance_date.month)
#         data.append(x.name)
#     print(data)
#     return render(request, 'pie_chart.html', {'labels': labels,'data': data,})

@login_required(login_url='/login')
def patients_entrance_chart(request):
    labels = []
    qs1 = []
    qs2 = [0]

    queryset = Patient.objects.values('entrance_date').annotate(num_of_entrance_patient = Count('entrance_date'))
    queryset2 = Patient.objects.values('exit_date').annotate(num_of_exit_patient = Count('exit_date'))
    for entry in queryset:
        labels.append(entry['entrance_date'])
        qs1.append(entry['num_of_entrance_patient'])

    for exit in queryset2:
        qs2.append(exit['num_of_exit_patient']*3)

    return JsonResponse(data={
        'labels': labels,
        'qs1': qs1,
        'qs2': qs2
    })
