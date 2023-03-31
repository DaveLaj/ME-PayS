from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, "index.html", {})


def register(request):
    return render(request, "register.html", {})


def home(request):
    return render(request, "home.html", {})


def transactions(request):
    return render(request, "transactions.html", {})


def account(request):
    return render(request, "account.html", {})


def cashdiv_home(request):
    return render(request, "cash_div/c_home.html", {})


def cashdiv_transaction(request):
    return render(request, "cash_div/c_transaction.html", {})


def cashdiv_account(request):
    return render(request, "cash_div/c_account.html", {})


def admin_home(request):
    return render(request, "admin/admin_home.html", {})


def admin_addUser(request):
    return render(request, "admin/admin_addUser.html", {})


def admin_listOfStaff(request):
    return render(request, "admin/admin_listOfStaff.html", {})


def admin_listOfStudent(request):
    return render(request, "admin/admin_listOfStudent.html", {})




