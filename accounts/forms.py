from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import SubscriptionPlan


class SubscriptionPlanForm(forms.ModelForm):
    name = forms.CharField(max_length=60, required=True, label='Plan Name:')
    description = forms.CharField(max_length=120, required=True, label='Describe Plan:')
    
    class Meta:
        model = SubscriptionPlan
        fields = ['name', 'description', 'price']


class GenerateSubscriptionForm(forms.Form):
    plan_id = forms.ModelChoiceField(
        queryset=SubscriptionPlan.objects.all(),
        label="Select a Subscription Plan",
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    duration_days = forms.IntegerField(
        label="Duration in Days",
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=True,
    )


class ManagementStaffCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=[('principal', 'Principal'), ('dean', 'Dean of Studies')], widget=forms.Select())

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'role']


class SearchStaffForm(forms.Form):
    search_query = forms.CharField(max_length=100, required=False, label='Search by Name or Phone ')


class PasswordChangeForm(forms.Form):  # User Change Password Form
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)