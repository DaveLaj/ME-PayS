from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from me_pays_app.models.users import *

# class RegisterForm(UserCreationForm):
#     email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
#     password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
#     password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
#     class Meta(UserCreationForm.Meta):
#         model = CustomUser
#         fields = ('email', 'password1', 'password2')

# in forms.py

class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}),required=True, help_text='Required.')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=True, help_text='Required.')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=True, help_text='Required.')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    contact_number = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control'}),required=True, help_text='Required.')
    school_id= forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control'}),required=True, help_text='Required.')

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2', 'school_id', 'contact_number')


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = EndUser
        fields = ('first_name', 'last_name', 'contact_number')





