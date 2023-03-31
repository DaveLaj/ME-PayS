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


def cash_division_home(request):
    return render(request, "cash_div/c_home.html", {})


def cash_division_transaction(request):
    return render(request, "cash_div/c_transaction.html", {})


def cash_division_account(request):
    return render(request, "cash_div/c_account.html", {})


