from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class PasswordChangeForm(forms.Form):  # User Change Password Form
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)


class ManagementStaffCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=[('principal', 'Principal'), ('dean', 'Dean of Studies')], widget=forms.Select())

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'role']


class SearchStaffForm(forms.Form):
    search_query = forms.CharField(max_length=100, required=False, label='Search by Name or Phone ')
