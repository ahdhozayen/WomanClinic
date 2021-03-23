from django.urls import path
from surgery import views

app_name = 'surgery'

urlpatterns =[
              path('list/', views.list_surgery_view, name='list-surgery-types'),
              path('create/', views.create_surgery_view, name='create-surgery'),
              path('update/<int:pk>', views.update_surgery_view, name='update-surgery'),
              path('view/<int:pk>', views.view_surgery_view, name='view-surgery'),
              path('delete/<int:pk>', views.delete_surgery_view, name='delete-surgery'),
              path('create/patient/surgery/<int:patient_id>', views.create_patient_surgery_view, name='create-patient-surgery'),
              path('list/doctors/', views.list_surgery_doctor_view, name='list-surgery-doctors'),
              path('create/doctor/', views.create_surgery_doctor_view, name='create-doctor'),
              path('update/doctor/<int:pk>', views.update_surgery_doctor_view, name='update-doctor'),
              path('delete/doctor/<int:pk>', views.delete_surgery_doctor_view, name='delete-doctor'),
]
