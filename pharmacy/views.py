from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from datetime import date
from django.contrib.auth.decorators import login_required
from pharmacy.models import Medicine
from pharmacy.forms import MedicineForm, Medicine_formset


@login_required(login_url='/login')
def list_medicines_view(request):
    all_medicines = Medicine.objects.all()
    return render(request, 'list-medicine.html', context={'page_title':'عرض الادوية','all_medicines':all_medicines})

@login_required(login_url='/login')
def create_medicine_view(request):
    # medicine_form = Medicine_formset(queryset = Medicine.objects.none())
    medicine_form = MedicineForm()
    if request.method == 'POST':
        medicine_form = MedicineForm(request.POST)
        if medicine_form.is_valid():
            med_obj = medicine_form.save(commit=False)
            # for x in med_obj:
            med_obj.created_by = request.user
            med_obj.last_update_by = request.user
            med_obj.save()
            return redirect('pharmacy:create-medicine')
    medContext = {
                  'page_title':'تسجيل الادوية',
                  'medicine_form':medicine_form,
    }
    return render(request, 'create-medicine-form.html', medContext)

@login_required(login_url='/login')
def update_medicine_view(request, pk):
    required_medicine = get_object_or_404(Medicine, pk=pk)
    medicine_form = MedicineForm(instance=required_medicine)
    if request.method == 'POST':
        medicine_form = MedicineForm(request.POST, instance=required_medicine)
        if medicine_form.is_valid():
            medicine_form.save()
    medContext = {
                  'page_title':'تعديل دواء {}'.format(required_medicine.scientific_name),
                  'medicine_form':medicine_form,
    }
    return render(request, 'update-medicine.html', medContext)
