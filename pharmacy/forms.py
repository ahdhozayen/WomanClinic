from django import forms
from crispy_forms.helper import FormHelper
from pharmacy.models import Medicine

common_items_to_execlude = (
                            'start_date','end_date',
                            'created_by', 'creation_date',
                            'last_update_by',  'last_update_date',
)

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = '__all__'
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(MedicineForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False

Medicine_formset = forms.modelformset_factory(Medicine, form=MedicineForm, extra=10)
