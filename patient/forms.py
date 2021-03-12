from django import forms
from crispy_forms.helper import FormHelper
from patient.models import (Patient,Delivery,Check_Up,
                            Patient_Files,Gynecology, Patient_Medicine,
                            Patient_Days_Off, Ultrasound, Diabetes,
                             Patient_Exit, Past_Medical_History)

common_items_to_execlude = (
                            'start_date','end_date',
                            'created_by', 'creation_date', 'patient',
                            'last_update_by',  'last_update_date', 'hospital','barcode'
)

class PatientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        form_type = kwargs.pop('form_type')
        super(PatientForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = True
        self.fields['date_of_birth'].widget.input_type = 'date'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        if form_type=='view':
            for field in self.fields:
                self.fields[field].widget.attrs['disabled'] = True

    class Meta:
        model = Patient
        fields = '__all__'
        exclude = common_items_to_execlude

class Past_Medical_History_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        form_type = kwargs.pop('form_type')
        super(Past_Medical_History_Form, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = True
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        if form_type=='view':
            for field in self.fields:
                self.fields[field].widget.attrs['disabled'] = True

    class Meta:
        model = Past_Medical_History
        fields = '__all__'
        exclude = ('created_by', 'creation_date', 'patient',
                    'last_update_by',  'last_update_date',)


class Patient_Exit_Form(forms.ModelForm):
    class Meta:
        model = Patient_Exit
        fields = ('exit_date', 'exit_note')
        exclude = common_items_to_execlude
    def __init__(self, *args, **kwargs):
        super(Patient_Exit_Form, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = True
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class Patient_FilesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Patient_FilesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Patient_Files
        fields = '__all__'
        exclude = common_items_to_execlude



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
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

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
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

Delivery_Check_Up_formset = forms.inlineformset_factory(Patient, Check_Up , form=CheckUpForm)

class GynecologyForm(forms.ModelForm):
    class Meta:
        model = Gynecology
        fields = '__all__'
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(GynecologyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

Gynecology_formset = forms.modelformset_factory(Gynecology, form=GynecologyForm, extra=10)

class Check_Up_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        form_type = kwargs.pop('form_type')
        super(Check_Up_Form, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = True
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        if form_type=='view':
            for field in self.fields:
                self.fields[field].widget.attrs['disabled'] = True

    class Meta:
        model = Check_Up
        fields = '__all__'
        exclude = common_items_to_execlude
        widgets = {
            'mhx': forms.Textarea(attrs={
                                                'rows': 2,'cols': 40,
                                                'style': 'height: 8em;',
                                                'class': 'form-control parsley-validated'}),
            'shx': forms.Textarea(attrs={
                                                'rows': 2,'cols': 40,
                                                'style': 'height: 8em;',
                                                'class': 'form-control parsley-validated'}),
            'allergy_hx': forms.Textarea(attrs={
                                                'rows': 2,'cols': 40,
                                                'style': 'height: 8em;',
                                                'class': 'form-control parsley-validated'}),
        }



class Patient_Medicine_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Patient_Medicine_Form, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Patient_Medicine
        fields = (
                  'medicine',
                  'issue_date',
                  'dose',
                  'notes',
        )
        exclude = common_items_to_execlude



Patient_Medicine_formset = forms.modelformset_factory(Patient_Medicine , form=Patient_Medicine_Form, extra=5, can_delete=False)

class Patient_Days_Off_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Patient_Days_Off_Form, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Patient_Days_Off
        fields = (
                  'date_start',
                  'date_end',
                  'notes',
        )
        exclude = common_items_to_execlude


Patient_Days_Off_formset = forms.modelformset_factory(Patient_Days_Off , form=Patient_Days_Off_Form, extra=5, can_delete=False)

class Ultrasound_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Ultrasound_Form, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = True
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Ultrasound
        fields = '__all__'
        exclude = common_items_to_execlude



class Diabetes_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Diabetes_Form, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = True
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Diabetes
        fields = ('bs','bp_up','bp_down','reading_date', 'temp')
        exclude = common_items_to_execlude
