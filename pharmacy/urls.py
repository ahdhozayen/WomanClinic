from django.urls import path
from pharmacy import views

app_name = 'pharmacy'

urlpatterns =[
    path('list/', views.list_medicines_view, name='all-medicines'),
    path('medicine/create/', views.create_medicine_view, name='create-medicine'),
    path('medicine/update/<int:pk>', views.update_medicine_view, name='update-medicine'),
]
