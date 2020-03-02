from django import forms
from crispy_forms.helper import FormHelper
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from custom_user.models import User


class CustomUserCreationForm(UserCreationForm):
    clinic_form_name = forms.CharField(max_length=30, required=False, help_text='Required.')
    class Meta(UserCreationForm):
        model = User
        fields = ('clinic_form_name','username', 'email')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email')

class AddUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'clinic')

    def __init__(self, *args, **kwargs):
        super(AddUserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False
