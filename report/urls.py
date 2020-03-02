from django.urls import path
from report import views

app_name = 'report'

urlpatterns =[
          path('patient/api/', views.report_dashboard_view, name='rep-dashboard'),
          path('patient/details/api/', views.total_patients_details_view, name='total-patients-details'),
          path('patient/api/', views.ChartData.as_view()),
          path('all/patients/report/', views.list_all_patients_view, name='rep-all-patients'),
          path('view/patient/report/<int:patient_id>', views.view_patient_history_view, name='patient-report'),
]
