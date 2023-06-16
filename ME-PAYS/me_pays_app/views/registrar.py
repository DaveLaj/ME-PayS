from me_pays_app.models.users import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST
from django_cryptography.fields import *
from me_pays_app.models.balance import *
from me_pays_app.models.pos import *
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
import json
import hashlib
from datetime import datetime
from django.db.models import Q
from me_pays_app.forms import *
from django.db.models import Sum

def user_has_registrar_group(user):
    return user.groups.filter(name='registrar').exists()





@login_required(login_url='index')
@user_passes_test(user_has_registrar_group)
def registrar_home(request):
    return render(request, "registrar/r_home.html", {})


@login_required(login_url='index')
@user_passes_test(user_has_registrar_group)
def registrar_services(request):
    return render(request, "registrar/r_product.html", {})


@login_required(login_url='index')
@user_passes_test(user_has_registrar_group)
def registrar_account(request):
    return render(request, "registrar/r_account.html", {})


@login_required(login_url='index')
@user_passes_test(user_has_registrar_group)
def registrar_transaction(request):
    return render(request, "registrar/r_transaction.html", {})