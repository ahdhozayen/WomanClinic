from django import forms
from crispy_forms.helper import FormHelper
from patient.models import (Patient,Delivery,Check_Up,
                            Patient_Files,Gynecology, Patient_Medicine, Patient_Days_Off)

common_items_to_execlude = (
                            'start_date','end_date',
                            'created_by', 'creation_date',
                            'last_update_by',  'last_update_date', 'hospital',
)

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        form_type = kwargs.pop('form_type')
        super(PatientForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = True
        if form_type=='view':
            for field in self.fields:
                self.fields[field].widget.attrs['disabled'] = True

class Patient_FilesForm(forms.ModelForm):
    class Meta:
        model = Patient_Files
        fields = '__all__'
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(Patient_FilesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False

Patient_Files_formset = forms.inlineformset_factory(Patient, Patient_Files, form=Patient_FilesForm, can_delete=False, extra=6)

class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = '__all__'
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(DeliveryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = True

Patient_Delivery_formset = forms.inlineformset_factory(Patient, Delivery, form=DeliveryForm)

class CheckUpForm(forms.ModelForm):
    class Meta:
        model = Check_Up
        fields = '__all__'
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(CheckUpForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False

Delivery_Check_Up_formset = forms.inlineformset_factory(Delivery, Check_Up , form=CheckUpForm)

class GynecologyForm(forms.ModelForm):
    class Meta:
        model = Gynecology
        fields = '__all__'
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(GynecologyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False

Gynecology_formset = forms.modelformset_factory(Gynecology, form=GynecologyForm, extra=10)

class Check_Up_Form(forms.ModelForm):
    class Meta:
        model = Check_Up
        fields = '__all__'
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        form_type = kwargs.pop('form_type')
        super(Check_Up_Form, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = True
        self.fields['delivery'].queryset = Delivery.objects.filter().order_by('creation_date')
        if form_type=='view':
            for field in self.fields:
                self.fields[field].widget.attrs['disabled'] = True

class Patient_Medicine_Form(forms.ModelForm):
    class Meta:
        model = Patient_Medicine
        fields = (
                  'medicine',
                  'issue_date',
                  'dose',
                  'notes',
        )
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(Patient_Medicine_Form, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False

Patient_Medicine_formset = forms.modelformset_factory(Patient_Medicine , form=Patient_Medicine_Form, extra=5, can_delete=False)

class Patient_Days_Off_Form(forms.ModelForm):
    class Meta:
        model = Patient_Days_Off
        fields = (
                  'date_start',
                  'date_end',
                  'notes',
        )
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(Patient_Days_Off_Form, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False

Patient_Days_Off_formset = forms.modelformset_factory(Patient_Days_Off , form=Patient_Days_Off_Form, extra=5, can_delete=False)
