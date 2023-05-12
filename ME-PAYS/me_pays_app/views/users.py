from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.contrib import messages
from me_pays_app.forms import RegisterForm
from django.urls import reverse
from django.contrib.auth.views import auth_login
from me_pays_app.views.decorators import *
import time
from django.contrib.auth.mixins import PermissionRequiredMixin
from me_pays_app.models.users import *



# User Login
@redirect_if_logged_in
def index(request):
    CustomUser = get_user_model()
    if request.method == 'POST':
        # Process the request if posted data are available
        email = request.POST['email']
        password = request.POST['password']
        # Check username and password combination if correct
        try:
            user = CustomUser.objects.get(email=email)
        except:
            messages.error(request,  '')

        user = authenticate(request, email=email, password=password, backend = 'django.contrib.auth.backends.ModelBackend')

        if user is not None:
            
             # Save session as cookie to login the user
            login(request, user) 
            # Success, now let's login the user.
            # check user roles  
            if user.groups.all()[0].name == 'enduser':
                return redirect('home')
            elif user.groups.all()[0].name == 'admin':
                return redirect('admin_home')
            elif user.groups.all()[0].name == 'cashier':
                return redirect('cashdiv_home')
            elif user.groups.all()[0].name == 'pos':
                return redirect('canteen_home')
        else:
            # Incorrect credentials, let's throw an error to the screen.
            messages.error(request, "Incorrect username and / or password.")
            return render(request, 'index.html')
    else:
        # No post data availabe, let's just show the page to the user.
        return render(request, 'index.html')
    

@redirect_if_logged_in
def registerenduser(request):
    # if this is a POST request we need to process the form data
    template = 'register.html'
    CustomUser = get_user_model()
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            if CustomUser.objects.filter(email = form.cleaned_data['email']).exists():
                messages.error(request, "Account already exists!")
            elif form.cleaned_data['password1'] != form.cleaned_data['password2']:
                messages.error(request, "Password do not match!")
            elif EndUser.objects.filter(contact_number = form.cleaned_data['contact_number']).exists():
                messages.error(request, "Contact Number already in use!")
            elif EndUser.objects.filter(school_id = form.cleaned_data['school_id']).exists():
                messages.error(request, "School ID already in use!")
            else:
                # Create the user:

                user = CustomUser.objects.create_enduser(
                    form.cleaned_data['email'],
                    form.cleaned_data['password1']
                )
                
                enduser = EndUser.objects.create(
                user=user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                school_id=form.cleaned_data['school_id'],
                contact_number=form.cleaned_data['contact_number'],
                )
                user.save()   
                enduser.save()

                # Login the user
                login(request, user,  backend = 'django.contrib.auth.backends.ModelBackend')
                messages.success(request, "You're succesfully registered!")
                return HttpResponseRedirect('register')
        else:
            errors = form.errors
            return render(request, template, {'form': form, 'errors': errors})
   # No post data availabe, let's just show the page.
    else:

        form = RegisterForm()

    return render(request, template, {'form': form})








@allowed_users(allowed_roles=['enduser'])
@login_required(login_url='index')
def home(request):
    return render(request, "home.html", {})

@allowed_users(allowed_roles=['enduser'])
@login_required(login_url='index')
def transactions(request):
    return render(request, "transactions.html", {})


@login_required(login_url='index')
def account(request):
    return render(request, "account.html", {})


@login_required(login_url='index')
def cashdiv_home(request):
    return render(request, "cash_div/c_home.html", {})


@login_required(login_url='index')
def cashdiv_transaction(request):
    return render(request, "cash_div/c_transaction.html", {})


@login_required(login_url='index')
def cashdiv_account(request):
    return render(request, "cash_div/c_account.html", {})


@login_required(login_url='index')
def admin_home(request):
    return render(request, "admin/admin_home.html", {})


@login_required(login_url='index')
def admin_addUser(request):
    return render(request, "admin/admin_addUser.html", {})


@login_required(login_url='index')
def admin_listOfStaff(request):
    return render(request, "admin/admin_listOfStaff.html", {})


@login_required(login_url='index')
def admin_listOfStudent(request):
    return render(request, "admin/admin_listOfStudent.html", {})


@login_required(login_url='index')
def canteen_home(request):
    return render(request, "canteen/canteen_home.html", {})


@login_required(login_url='index')
def canteen_products(request):
    return render(request, "canteen/canteen_products.html", {})


@login_required(login_url='index')
def canteen_history(request):
    return render(request, "canteen/canteen_history.html", {})


@login_required(login_url='index')
def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("index")



