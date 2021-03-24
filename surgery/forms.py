from django import forms
from crispy_forms.helper import FormHelper
from surgery import models

common_items_to_execlude = (
                            'start_date','end_date',
                            'created_by', 'creation_date',
                            'last_update_by',  'last_update_date','hospital',
)

class Surgery_Master_Form(forms.ModelForm):
    class Meta:
        model = models.Surgery_Master
        fileds = '__all__'
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(Surgery_Master_Form, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class Surgery_Steps_Form(forms.ModelForm):
    class Meta:
        model = models.Surgery_Steps
        fileds = '__all__'
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(Surgery_Steps_Form, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

Surgery_Inline = forms.inlineformset_factory(models.Surgery_Master,
                                             models.Surgery_Steps,
                                             extra=2,
                                             form=Surgery_Steps_Form,
                                             can_delete=False)

class Patient_Surgery_Form(forms.ModelForm):
    class Meta:
        model = models.Patient_Surgery
        fileds = '__all__'
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(Patient_Surgery_Form, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class Surgery_Doctor_Form(forms.ModelForm):
    class Meta:
        model = models.Surgery_Doctor
        fileds = '__all__'
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(Surgery_Doctor_Form, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

doctor_Inline = forms.modelformset_factory(models.Surgery_Doctor,
                                             extra=8,
                                             form=Surgery_Doctor_Form,
                                             can_delete=False)

class After_Surgery_Form(forms.ModelForm):
    class Meta:
        model = models.After_Surgery
        fileds = ('after_surgery_notes','after_surgery_recomendations')
        exclude = common_items_to_execlude

    def __init__(self, *args, **kwargs):
        super(After_Surgery_Form, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
