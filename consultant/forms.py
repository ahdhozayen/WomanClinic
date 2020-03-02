from django import forms
from crispy_forms.helper import FormHelper

common_items_to_execlude = (
                            'start_date','end_date',
                            'created_by', 'creation_date',
                            'last_update_by',  'last_update_date',
)

# class PatientForm(forms.ModelForm):
#     class Meta:
#         model = Patient
#         fields = '__all__'
#         exclude = common_items_to_execlude
#
#     def __init__(self, *args, **kwargs):
#         form_type = kwargs.pop('form_type')
#         super(PatientForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper(self)
#         self.helper.form_show_labels = True
#         if form_type=='view':
#             for field in self.fields:
#                 self.fields[field].widget.attrs['disabled'] = True
