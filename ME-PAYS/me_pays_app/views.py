from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages
from .forms import RegisterForm

# Create your views here.


# User Login
def index(request):
    if request.method == 'POST':
        # Process the request if posted data are available
        username = request.POST['username']
        password = request.POST['password']
        # Check username and password combination if correct
        user = authenticate(username=username, password=password)
        login(request, user)
        if user is not None:
            
            # Save session as cookie to login the user
            login(request, user)
            # Success, now let's login the user.
            return render(request, 'home.html')
        else:
            # Incorrect credentials, let's throw an error to the screen.
            messages.error(request, "Incorrect username and / or password.")
            return render(request, 'index.html')
    else:
        # No post data availabe, let's just show the page to the user.
        return render(request, 'index.html')
    

# Admin Login
def admin_login(request):
    if request.user.is_authenticated:
        return redirect(reverse("admin")) 
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request,username = username, password = password)
        if user is not None:
            if(user.is_superuser):
                auth_login(request, user)
                return redirect(reverse("dashboard"))
            else:
                messages.info(request, "invalid credentials")
            return redirect(reverse("admin"))
         
    return render(request,'login.html') 

    


def register(request):
    # if this is a POST request we need to process the form data
    template = 'register.html'
   
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                messages.error(request, "Account already exists!")
            elif User.objects.filter(email=form.cleaned_data['email']).exists():
                messages.error(request, "Account already exists!")
            elif form.cleaned_data['password'] != form.cleaned_data['password_repeat']:
                messages.error(request, "Password do not match!")
            else:
                # Create the user:
                user = User.objects.create_user(
                    form.cleaned_data['username'],
                    form.cleaned_data['email'],
                    form.cleaned_data['password']
                )
                user.save()

                # Login the user
                login(request, user)
                messages.success(request, "You're succesfully registered!")
                return HttpResponseRedirect('register')

   # No post data availabe, let's just show the page.
    else:
        form = RegisterForm()

    return render(request, template, {'form': form})



@login_required(login_url='index')
def home(request):
    return render(request, "home.html", {})


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



