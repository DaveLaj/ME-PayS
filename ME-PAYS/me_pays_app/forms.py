from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from me_pays_app.models.users import CustomUser

# class RegisterForm(forms.Form):
#     email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
#     password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('first_name', 'last_name', 'contact_number')