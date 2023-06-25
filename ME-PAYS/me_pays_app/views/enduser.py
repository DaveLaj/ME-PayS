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



def user_has_enduser_group(user):
    return user.groups.filter(name='enduser').exists()



@login_required(login_url='index')
@user_passes_test(user_has_enduser_group)
def home(request):
    return render(request, "home.html", {})



@login_required(login_url='index')
@require_POST
def share_validate_sid(request):
    sid = request.POST.get('school_id')
    if EndUser.objects.filter(school_id=sid, user__is_active=1).exists():
        # RFID instance already exists
        return JsonResponse({'exists': 1})
    else:
        # RFID code does not exist in the database
        return JsonResponse({'exists': 0})
    


@require_GET
def  share_sid_creds(request):
    school_id = request.GET.get('school_id')
    user=EndUser.objects.filter(school_id=school_id).first()
    fullname = user.first_name+" "+user.last_name
    response = {
        'fullname': fullname,
        'personID': user.school_id
    }
    return JsonResponse(response)
    
@login_required(login_url='index')
@user_passes_test(user_has_enduser_group)
@require_POST
def shareAmount(request):
    sid = request.POST.get('sid')
    amount = request.POST.get('amount')
    recipient = EndUser.objects.filter(school_id=sid).first()
    sender = EndUser.objects.get(user=request.user)
    # Convert the amount to an integer if needed
    amount = float(amount)
    amount = abs(amount)
    if recipient.rfid_code is None:
        response_data = {
            'status': 'error',
            'message': 'Recipient has not activated Wallet Pay Services',
        }
        return JsonResponse(response_data)
    elif sender.credit_balance >= amount:
        # Deduct the amount from the current credit_balance
        sender.credit_balance -= amount
        # Save the updated user object
        sender.save()
        # Add to recipient
        recipient.credit_balance += amount
        # Save the updated user object
        recipient.save()
        
        # Save to Balance Logs
        receive_log = Balance_Logs.objects.create(
            account_Owner=recipient,
            enduser_sender=sender,
            amount=amount,
            desc="Share",
        )  
        receive_log.save()
        send_log = Balance_Logs.objects.create(
            account_Owner=sender,
            enduser_sender=recipient,
            amount=-(amount),
            desc="Send",
        )  
        send_log.save()
        
        response_data = {
            'status': 'success',
            'message': 'Payment Successful, Please Check Your Load Balance',
        }
        
        return JsonResponse(response_data)
    else:
        return JsonResponse({'status': 'error', 'message': 'Insufficient Credits'})




def updateBalance(request):
    # initialize available services
    user = EndUser.objects.get(user=request.user)
    balance = user.credit_balance
    context={
        'balance': balance,
    }
    return JsonResponse(context)




@login_required(login_url='index')
@user_passes_test(user_has_enduser_group)
def transactions(request):
    enduser = EndUser.objects.get(user=request.user)
    loglist = Balance_Logs.objects.filter(account_Owner=enduser).order_by('-id')
    paginator = Paginator(loglist, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count = loglist.count()
    form = LogSearchForm()
    context = {
        'form': form,
        'count' : count,
        'page_obj': page_obj,
    }
    return render(request, "transactions.html", context)

@login_required(login_url='index')
@user_passes_test(user_has_enduser_group)
def enduser_searchTransaction(request):
    enduser = EndUser.objects.get(user=request.user)
    search_string = request.GET.get('query')
    date_string = request.GET.get('date')
    
    loglist = Balance_Logs.objects.filter(account_Owner=enduser).order_by('-id')
    
    if search_string:
        loglist = loglist.filter(Q(desc__icontains=search_string))
    
    if date_string:
        try:
            date = datetime.strptime(date_string, '%Y-%m-%d').date()
            loglist = loglist.filter(datetime__date=date)
        except ValueError:
            pass
    
    paginator = Paginator(loglist, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count = loglist.count()
    
    context = {
        'count': count,
        'page_obj': page_obj,
        'search_string': search_string,  # Pass the search query back to the template
        'date_string': date_string,      # Pass the date input back to the template
    }
    return render(request, "transactions.html", context)