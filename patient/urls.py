from django.urls import path
from patient import views

app_name = 'patient'

urlpatterns =[
    path('patient/list/', views.list_patients_view, name='all-patients'),
    path('patient/create/', views.create_patient_view, name='create-patient'),
    path('patient/view/<int:pk>', views.view_patient_view, name='view-patient'),
    path('patient/update/<int:pk>', views.update_patient_view, name='update-patient'),
    path('patient/delete/<int:pk>', views.delete_patient, name='delete-patient'),
    path('gyno/list/', views.list_gyno_view, name='all-gynos'),
    path('gyno/create/', views.create_gyno_view, name='create-gyno'),
    path('gyno/update/<int:pk>', views.update_gyno_view, name='update-gyno'),
    path('gyno/delete/<int:pk>', views.delete_gyno_view, name='delete-gyno'),
    path('delivery/create/list/<int:pk>', views.create_delivery_view, name='all-delivery'),
    path('delivery/update/list/<int:pk>/<int:patient_id>', views.update_delivery_view, name='update-delivery'),
    path('checkup/create/list/<int:patient_id>', views.create_list_check_up_view, name='all-checkup'),
    path('us/create/<int:check_id>/<int:patient_id>/', views.ultrasound_create_view, name='create-us'),
    path('checkup/view/<int:patient_id>/<int:chk_id>', views.view_list_check_up_view, name='view-checkup'),
    path('checkup/update/<int:patient_id>/<int:chk_id>', views.update_patient_medicine_view, name='update-checkup'),
    path('medicine/create/<int:patient_id>/<int:chk_id>', views.create_patient_medicine_view, name='create-med'),
    path('cons/list/', views.list_patient_consultant_view, name='all-con-patients'),
    path('create/days-off/<int:patient_id>', views.create_patient_days_off_view, name='create-days-off'),
    path('create/diabete/<int:patient_id>', views.create_diabetes_view, name='create-diabetes'),
    path('chart/diabete/<int:patient_id>', views.patient_diabete_chart, name='patients-diabetes-chart'),


    path('search/barcode/', views.view_patient_barcode, name='search-barcode'),
]
