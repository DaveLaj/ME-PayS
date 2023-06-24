from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from me_pays_app.models.users import *
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.core.validators import MaxLengthValidator
from django.utils.text import capfirst


def uncapitalize_string(text):
    return text.lower()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control form-control-sm', 'placeholder':'Enter My.IIT email'}),required=True, help_text='Required.')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'placeholder':'Enter first name', 'maxlength': '30'}),required=True, help_text='Required.')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'placeholder':'Enter last name'}),required=True, help_text='Required.')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm', 'placeholder':'Enter password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm', 'placeholder':'Confirm password'}))
    contact_number = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control form-control-sm', 'placeholder':'9xxxxxxxxx', 'id': 'contact_number', 'oninput':"this.value = this.value.slice(0, 10);"}),required=True, validators=[MaxLengthValidator(10, message='Please enter a 10-digit contact number.')], help_text='Required.')
    school_id= forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control form-control-sm', 'placeholder':'20190001'}),required=True, help_text='Required.')



    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name:
            first_name=capfirst(uncapitalize_string(first_name))
            return first_name
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name:
            last_name=capfirst(uncapitalize_string(last_name))
            return last_name
        return last_name


    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2', 'school_id', 'contact_number')


class LogSearchForm(forms.Form):
    search_date = forms.DateField(
        label='Search Date',
        widget=forms.DateInput(attrs={'type': 'date'})
    )



class EndUser_CreationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control form-control-sm', 'placeholder':'Enter New My.IIT Email'}),required=True, help_text='Required.')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'placeholder':'Enter first name', 'maxlength': '30'}),required=True, help_text='Required.')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'placeholder':'Enter last name'}),required=True, help_text='Required.')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm', 'placeholder':'Enter password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm', 'placeholder':'Confirm password'}))
    contact_number = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control form-control-sm', 'placeholder':'9xxxxxxxxx', 'id': 'contact_number', 'oninput':"this.value = this.value.slice(0, 10);"}),required=True, validators=[MaxLengthValidator(10, message='Please enter a 10-digit contact number.')], help_text='Required.')
    school_id= forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control form-control-sm', 'placeholder':'20190001'}), help_text='Required.')


    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name:
            first_name=capfirst(uncapitalize_string(first_name))
            return first_name
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name:
            last_name=capfirst(uncapitalize_string(last_name))
            return last_name
        return last_name




    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2', 'school_id', 'contact_number')











class Registrar_CreationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control form-control-sm', 'placeholder':'Enter New My.IIT Email'}),required=True, help_text='Required.')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'placeholder':'Enter first name', 'maxlength': '30'}),required=True, help_text='Required.')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'placeholder':'Enter last name'}),required=True, help_text='Required.')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm', 'placeholder':'Enter password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm', 'placeholder':'Confirm password'}))
    contact_number = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control form-control-sm', 'placeholder':'9xxxxxxxxx', 'id': 'contact_number', 'oninput':"this.value = this.value.slice(0, 10);"}),required=True, validators=[MaxLengthValidator(10, message='Please enter a 10-digit contact number.')], help_text='Required.')
    school_id= forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control form-control-sm', 'placeholder':'20190001'}), help_text='Required.')


    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name:
            first_name=capfirst(uncapitalize_string(first_name))
            return first_name
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name:
            last_name=capfirst(uncapitalize_string(last_name))
            return last_name
        return last_name


    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2', 'school_id', 'contact_number')





















class POS_CreationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control form-control-sm', 'maxlength':'100', 'placeholder':'Enter New My.IIT Email'}),required=True, help_text='Required.')
    store_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'placeholder':'Enter store name', 'maxlength': '30'}),required=True, help_text='Required.')
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm', 'placeholder':'Enter password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm', 'placeholder':'Confirm password'}))
    contact_number = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control form-control-sm limit-length',  'placeholder':'9xxxxxxxxx', 'id': 'contact_number', 'oninput':"formatNumberInput(this)"}),required=True, validators=[MaxLengthValidator(10, message='Please enter a 10-digit contact number.')], help_text='Required.')
    location = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'maxlength': '100'}),required=True, help_text='Required.')
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows':'5'}), required=False)
    school_id = forms.CharField(
    widget=forms.TextInput(attrs={
        'class': 'form-control form-control-sm',
        'placeholder': '2019-0001',
        'id': 'school_id',
        'name': 'school_id'
    }),
    help_text='Required.'
)


    class Meta:
        model = CustomUser
        fields = ('email', 'store_name', 'password1', 'password2', 'contact_number', 'location', 'description')


class Cashier_CreationForm(UserCreationForm):

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control form-control-sm', 'maxlength':'100', 'placeholder':'Enter New My.IIT Email'}),required=True, help_text='Required.')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'placeholder':'Enter the first name', 'maxlength': '30'}),required=True, help_text='Required.')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'placeholder':'Enter the last name', 'maxlength': '30'}),required=True, help_text='Required.')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm', 'placeholder':'Enter password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm', 'placeholder':'Confirm password'}))
    contact_number = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control form-control-sm limit-length',  'placeholder':'9xxxxxxxxx', 'id': 'contact_number', 'oninput':"this.value = this.value.slice(0, 10);"}),required=True, validators=[MaxLengthValidator(10, message='Please enter a 10-digit contact number.')], help_text='Required.')
    location = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'maxlength': '60'}),required=True, help_text='Required.')



    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name:
            first_name=capfirst(uncapitalize_string(first_name))
            return first_name
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name:
            last_name=capfirst(uncapitalize_string(last_name))
            return last_name
        return last_name
    
    
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2', 'contact_number', 'location')







# ⠀⠀⠀⠀⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣤⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⠀⠀⠀⢀⣴⠟⠉⠀⠀⠀⠈⠻⣦⡀⠀⠀⠀⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣷⣀⢀⣾⠿⠻⢶⣄⠀⠀⣠⣶⡿⠶⣄⣠⣾⣿⠗⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⢻⣿⣿⡿⣿⠿⣿⡿⢼⣿⣿⡿⣿⣎⡟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡟⠉⠛⢛⣛⡉⠀⠀⠙⠛⠻⠛⠑⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣧⣤⣴⠿⠿⣷⣤⡤⠴⠖⠳⣄⣀⣹⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣀⣟⠻⢦⣀⡀⠀⠀⠀⠀⣀⡈⠻⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⡿⠉⡇⠀⠀⠛⠛⠛⠋⠉⠉⠀⠀⠀⠹⢧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⡟⠀⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠃⠀⠈⠑⠪⠷⠤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣾⣿⣿⣿⣦⣼⠛⢦⣤⣄⡀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠑⠢⡀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⢀⣠⠴⠲⠖⠛⠻⣿⡿⠛⠉⠉⠻⠷⣦⣽⠿⠿⠒⠚⠋⠉⠁⡞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢦⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⢀⣾⠛⠁⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠤⠒⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢣⠀⠀⠀
# ⠀⠀⠀⠀⣰⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣑⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⡇⠀⠀
# ⠀⠀⠀⣰⣿⣁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣧⣄⠀⠀⠀⠀⠀⠀⢳⡀⠀
# ⠀⠀⠀⣿⡾⢿⣀⢀⣀⣦⣾⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡰⣫⣿⡿⠟⠻⠶⠀⠀⠀⠀⠀⢳⠀
# ⠀⠀⢀⣿⣧⡾⣿⣿⣿⣿⣿⡷⣶⣤⡀⠀⠀⠀⠀⠀⠀⠀⢀⡴⢿⣿⣧⠀⡀⠀⢀⣀⣀⢒⣤⣶⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇
# ⠀⠀⡾⠁⠙⣿⡈⠉⠙⣿⣿⣷⣬⡛⢿⣶⣶⣴⣶⣶⣶⣤⣤⠤⠾⣿⣿⣿⡿⠿⣿⠿⢿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇
# ⠀⣸⠃⠀⠀⢸⠃⠀⠀⢸⣿⣿⣿⣿⣿⣿⣷⣾⣿⣿⠟⡉⠀⠀⠀⠈⠙⠛⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇
# ⠀⣿⠀⠀⢀⡏⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⠿⠿⠛⠛⠉⠁⠀⠀⠀⠀⠀⠉⠠⠿⠟⠻⠟⠋⠉⢿⣿⣦⡀⢰⡀⠀⠀⠀⠀⠀⠀⠁
# ⢀⣿⡆⢀⡾⠀⠀⠀⠀⣾⠏⢿⣿⣿⣿⣯⣙⢷⡄⠀⠀⠀⠀⠀⢸⡄⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣿⣻⢿⣷⣀⣷⣄⠀⠀⠀⠀⢸⠀
# ⢸⠃⠠⣼⠃⠀⠀⣠⣾⡟⠀⠈⢿⣿⡿⠿⣿⣿⡿⠿⠿⠿⠷⣄⠈⠿⠛⠻⠶⢶⣄⣀⣀⡠⠈⢛⡿⠃⠈⢿⣿⣿⡿⠀⠀⠀⠀⠀⡀
# ⠟⠀⠀⢻⣶⣶⣾⣿⡟⠁⠀⠀⢸⣿⢅⠀⠈⣿⡇⠀⠀⠀⠀⠀⣷⠂⠀⠀⠀⠀⠐⠋⠉⠉⠀⢸⠁⠀⠀⠀⢻⣿⠛⠀⠀⠀⠀⢀⠇
# ⠀⠀⠀⠀⠹⣿⣿⠋⠀⠀⠀⠀⢸⣧⠀⠰⡀⢸⣷⣤⣤⡄⠀⠀⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡆⠀⠀⠀⠀⡾⠀⠀⠀⠀⠀⠀⢼⡇
# ⠀⠀⠀⠀⠀⠙⢻⠄⠀⠀⠀⠀⣿⠉⠀⠀⠈⠓⢯⡉⠉⠉⢱⣶⠏⠙⠛⠚⠁⠀⠀⠀⠀⠀⣼⠇⠀⠀⠀⢀⡇⠀⠀⠀⠀⠀⠀⠀⡇
# ⠀⠀⠀⠀⠀⠀⠻⠄⠀⠀⠀⢀⣿⠀⢠⡄⠀⠀⠀⣁⠁⡀⠀⢠⠀⠀⠀⠀⠀⠀⠀⠀⢀⣐⡟⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⢠⡇








            
class ChangePassword(UserChangeForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm', 'placeholder':'New Password', 'name':'password1'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-sm', 'placeholder':'Confirm New Password', 'name':'password2'}))
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('password1', 'password2')
    

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = EndUser
        fields = ('first_name', 'last_name', 'contact_number')


class CustomGroups(UserChangeForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = get_user_model()
        fields = '__all__'


# ⢀⡴⠑⡄⠀⠀⠀⠀⠀⠀⠀⣀⣀⣤⣤⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
# ⠸⡇⠀⠿⡀⠀⠀⠀⣀⡴⢿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
# ⠀⠀⠀⠀⠑⢄⣠⠾⠁⣀⣄⡈⠙⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀ 
# ⠀⠀⠀⠀⢀⡀⠁⠀⠀⠈⠙⠛⠂⠈⣿⣿⣿⣿⣿⠿⡿⢿⣆⠀⠀⠀⠀⠀⠀⠀ 
# ⠀⠀⠀⢀⡾⣁⣀⠀⠴⠂⠙⣗⡀⠀⢻⣿⣿⠭⢤⣴⣦⣤⣹⠀⠀⠀⢀⢴⣶⣆ 
# ⠀⠀⢀⣾⣿⣿⣿⣷⣮⣽⣾⣿⣥⣴⣿⣿⡿⢂⠔⢚⡿⢿⣿⣦⣴⣾⠁⠸⣼⡿ 
# ⠀⢀⡞⠁⠙⠻⠿⠟⠉⠀⠛⢹⣿⣿⣿⣿⣿⣌⢤⣼⣿⣾⣿⡟⠉⠀⠀⠀⠀⠀ 
# ⠀⣾⣷⣶⠇⠀⠀⣤⣄⣀⡀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀ 
# ⠀⠉⠈⠉⠀⠀⢦⡈⢻⣿⣿⣿⣶⣶⣶⣶⣤⣽⡹⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀ 
# ⠀⠀⠀⠀⠀⠀⠀⠉⠲⣽⡻⢿⣿⣿⣿⣿⣿⣿⣷⣜⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀ 
# ⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣷⣶⣮⣭⣽⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀ 
# ⠀⠀⠀⠀⠀⠀⣀⣀⣈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀ 
# ⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀ 
# ⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠻⠿⠿⠿⠿⠛⠉