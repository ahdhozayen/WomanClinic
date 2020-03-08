from django.urls import path
from report import views

app_name = 'report'

urlpatterns =[
          path('patient/api/', views.report_dashboard_view, name='rep-dashboard'),
          path('patient/details/api/', views.total_patients_details_view, name='total-patients-details'),
          path('all/patients/report/', views.list_all_patients_view, name='rep-all-patients'),
          path('cons/patients/report/', views.list_consultant_patients_view, name='rep-cons-patients'),
          path('clexane/patients/report/', views.list_clexane_patients_view, name='rep-clexane-patients'),
          path('view/patient/report/<int:patient_id>', views.view_patient_history_view, name='patient-report'),
          path('patients/entrance/chart/', views.patients_entrance_chart, name='patients-entrance-chart'),
]
