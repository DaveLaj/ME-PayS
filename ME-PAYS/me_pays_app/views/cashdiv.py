from me_pays_app.models.users import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST
from django_cryptography.fields import *
from me_pays_app.models.balance import *
from me_pays_app.models.pos import *
from me_pays_app.models.order import *
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
from django.db.models import Count
from django.db.models.functions import TruncDate
from datetime import date, timedelta
# Rest of your code...



def user_has_cashier_group(user):
    return user.groups.filter(name='cashier').exists()


@login_required(login_url='index')
@user_passes_test(user_has_cashier_group)
def cashdiv_account(request):


    UserAccount = CustomUser.objects.filter(id=request.user.id).first()
    CashierCreds = Cashier.objects.filter(user=UserAccount).first()
    context={
        'cashier': CashierCreds
    }
    return render(request, "cash_div/c_account.html", context)



def updateStats(request):
    # initialize available services
    current_date = datetime.now().date()
    cashier = Cashier.objects.get(user=request.user)
    dailyCashIn = Balance_Logs.objects.filter(cashier_sender=cashier, desc='Cash In', datetime__date=current_date)
    dailyPay = Balance_Logs.objects.filter(cashier_sender=cashier, desc='Fee Payment', datetime__date=current_date)
    # Initializes the Counts
    dailyCashInCount = dailyCashIn.count()
    dailyPayCount = dailyPay.count()
    # Initializes the Total Amounts
    totalCashIn = dailyCashIn.aggregate(total_amount=Sum('amount'))['total_amount']
    totalPay = dailyPay.aggregate(total_amount=Sum('amount'))['total_amount']
    if totalPay is None:
        totalPay=0
    context={
        'dailyCashInCount': dailyCashInCount,
        'dailyPayCount': dailyPayCount,
        'dailyTotalCashIn': totalCashIn,
        'dailyTotalPay': -totalPay,
    }
    return JsonResponse(context)







@login_required(login_url='index')
@user_passes_test(user_has_cashier_group)
def cashdiv_home(request):
    # initialize available services
    services = menu.objects.filter(
        menu_owner_id=request.user.id,
        menu_is_active=1 
    ).order_by('menu_name')
    current_date = datetime.now().date()
    cashier = Cashier.objects.get(user=request.user)
    dailyCashIn = Balance_Logs.objects.filter(cashier_sender=cashier, desc='Cash In', datetime__date=current_date)
    dailyPay = Balance_Logs.objects.filter(cashier_sender=cashier, desc='Fee Payment', datetime__date=current_date)
    # Initializes the Counts
    dailyCashInCount = dailyCashIn.count()
    dailyPayCount = dailyPay.count()
    # Initializes the Total Amounts
    totalCashIn = dailyCashIn.aggregate(total_amount=Sum('amount'))['total_amount']
    totalPay = dailyPay.aggregate(total_amount=Sum('amount'))['total_amount']
    UserAccount = CustomUser.objects.filter(id=request.user.id).first()
    CashierCreds = Cashier.objects.filter(user=UserAccount).first()


    end_date = date.today()
    start_date = end_date - timedelta(days=6)  # Retrieve data for the last 7 days




    # Query the database for "Cash In" transactions within the specified date range
    cash_in_logs = Balance_Logs.objects.filter(cashier_sender=request.user.cashier, desc='Cash In', datetime__date__range=[start_date, end_date]) \
        .annotate(date=TruncDate('datetime')).values('date') \
        .annotate(count=Count('id')).order_by('date')


    # Query the database for "Fee Payment" transactions within the specified date range
    fee_payment_logs = Balance_Logs.objects.filter(cashier_sender=request.user.cashier,desc='Fee Payment', datetime__date__range=[start_date, end_date]) \
        .annotate(date=TruncDate('datetime')).values('date') \
        .annotate(count=Count('id')).order_by('date')

    cash_in_logs_amount = Balance_Logs.objects.filter(cashier_sender=request.user.cashier, desc='Cash In', datetime__date__range=[start_date, end_date])\
    .values('datetime__date') \
    .annotate(total_amount=Sum('amount')) \
    .order_by('datetime__date')
    fee_payment_logs_amount = Balance_Logs.objects.filter(cashier_sender=request.user.cashier, desc='Fee Payment', datetime__date__range=[start_date, end_date]) \
    .values('datetime__date') \
    .annotate(total_amount=Sum('amount')) \
    .order_by('datetime__date')

    cash_in_dates = [entry['date'].strftime('%Y-%m-%d') for entry in cash_in_logs]
    cash_in_counts = [entry['count'] for entry in cash_in_logs]
    cash_in_amounts = [entry['total_amount'] for entry in cash_in_logs_amount]
    fee_payment_dates = [entry['date'].strftime('%Y-%m-%d') for entry in fee_payment_logs]
    fee_payment_counts = [entry['count'] for entry in fee_payment_logs]
    fee_payment_amounts = [-entry['total_amount'] for entry in fee_payment_logs_amount]
    context = {
        'cash_in_dates': cash_in_dates,
        'cash_in_counts': cash_in_counts,
        'fee_payment_dates': fee_payment_dates,
        'fee_payment_counts': fee_payment_counts,
        'fee_payment_amounts': fee_payment_amounts,
        'cash_in_amounts':cash_in_amounts,



        'dailyCashInCount':dailyCashInCount,
        'dailyPayCount':dailyPayCount,
        'services':services,
        'dailyTotalCashIn': totalCashIn,
        'dailyTotalPay': totalPay,
        'cashier': CashierCreds
    }
    return render(request, "cash_div/c_home.html", context)
 

    

    
 










    


@user_passes_test(user_has_cashier_group)
@require_POST
def load_validate_rfid(request):
    rfid = request.POST.get('rfid')
    rfid = hashlib.sha256(rfid.encode()).hexdigest()
    if EndUser.objects.filter(rfid_code=rfid, user__is_active=1).exists():
        # RFID instance already exists
        return JsonResponse({'exists': 0})
    if POS.objects.filter(rfid_code=rfid, user__is_active=1).exists():
        # RFID instance already exists
        return JsonResponse({'exists': 0})
    else:
        # RFID code does not exist in the database
        return JsonResponse({'exists': 1})
    

@user_passes_test(user_has_cashier_group)
@require_POST
def cashout_validate_rfid(request):
    rfid = request.POST.get('rfid')
    rfid = hashlib.sha256(rfid.encode()).hexdigest()
    if EndUser.objects.filter(rfid_code=rfid, user__is_active=1).exists():
        # RFID instance already exists
        return JsonResponse({'exists': 0})
    if POS.objects.filter(rfid_code=rfid, user__is_active=1).exists():
        # RFID instance already exists
        return JsonResponse({'exists': 0})
    else:
        # RFID code does not exist in the database
        return JsonResponse({'exists': 1})



@user_passes_test(user_has_cashier_group)
@require_GET
def  load_rfid_creds(request):
    rfid = request.GET.get('rfid')
    rfid = hashlib.sha256(rfid.encode()).hexdigest()
    enduser=EndUser.objects.filter(rfid_code=rfid).first()
    pos=POS.objects.filter(rfid_code=rfid).first()
    if enduser:
        fullname = enduser.first_name+" "+enduser.last_name
        response = {
            'fullname': fullname,
            'personID': enduser.school_id
        }
    elif pos:
        fullname = pos.store_name
        response = {
            'fullname': fullname,
            'personID': pos.school_id
        }
    return JsonResponse(response)




@user_passes_test(user_has_cashier_group)
@require_GET
def cashout_rfid_creds(request):
    rfid = request.GET.get('rfid')
    rfid = hashlib.sha256(rfid.encode()).hexdigest()
    enduser=EndUser.objects.filter(rfid_code=rfid).first()
    pos=POS.objects.filter(rfid_code=rfid).first()
    if enduser:
        fullname = enduser.first_name+" "+enduser.last_name
        response = {
            'fullname': fullname,
            'personID': enduser.school_id,
            'balance' : enduser.credit_balance,
        }
    elif pos:
        fullname = pos.store_name
        response = {
            'fullname': fullname,
            'personID': pos.school_id,
            'balance' : pos.credit_balance,
        }
    return JsonResponse(response)


@user_passes_test(user_has_cashier_group)
@require_GET
def cashout_validate_balance(request):
    rfid = request.GET.get('rfid')
    rfid = hashlib.sha256(rfid.encode()).hexdigest()
    amount = request.GET.get('amount')
    amount = float(amount)
    amount = abs(amount)
    enduser=EndUser.objects.filter(rfid_code=rfid).first()
    pos=POS.objects.filter(rfid_code=rfid).first()
    if enduser:
        user = enduser
    elif pos:
        user = pos

    if user.credit_balance >= float(amount):
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Cannot Withdraw Exceeding Amount'})





@user_passes_test(user_has_cashier_group)
@require_GET
def load_cred_amount(request):
    rfid = request.GET.get('rfid')
    rfid = hashlib.sha256(rfid.encode()).hexdigest()
    amount = request.GET.get('amount')
    amount = float(amount)
    enduser=EndUser.objects.filter(rfid_code=rfid).first()
    pos=POS.objects.filter(rfid_code=rfid).first()
    if enduser:
        user = enduser.user
    elif pos:
        user = pos.user
    cashier = Cashier.objects.get(user=request.user)
    if user is not None and amount < 0:
        return JsonResponse({'status': 'success', 'message': 'Cannot Accept Negative Amount'})
    elif user is not None:
        # Convert the amount to an integer if needed
        
        amount = abs(amount)
        # Add the amount to the current credit_balance
        if hasattr(user, 'enduser'):
            user.enduser.credit_balance += amount 
            user.enduser.save()
        elif hasattr(user, 'pos'):
            user.pos.credit_balance += amount
            user.pos.save()
        else: 
            return print("error")
        
        # Save the updated user object
        user.save()
        # Save to Balance Logs
        log = Balance_Logs.objects.create(
            account_Owner = user,
            cashier_sender = cashier,
            amount = amount,
            desc = "Cash In",
        )  
        log.save()

        return JsonResponse({'status': 'success', 'message': 'Payment Successful, Please Check Your Load Balance'})
    else:
        return JsonResponse({'status': 'error', 'message': 'User not found, Contact Admin Immediately'})




@user_passes_test(user_has_cashier_group)
@require_GET
def cashout_cred_amount(request):
    rfid = request.GET.get('rfid')
    rfid = hashlib.sha256(rfid.encode()).hexdigest()
    amount = request.GET.get('amount')
    enduser=EndUser.objects.filter(rfid_code=rfid).first()
    pos=POS.objects.filter(rfid_code=rfid).first()
    if enduser:
        user = enduser
    elif pos:
        user = pos
    cashier = Cashier.objects.get(user=request.user)
    amount = float(amount)
    if amount < 0:
        return JsonResponse({'status': 'success', 'message': 'Cannot Accept Negative Amount'})
    elif user.credit_balance >= float(amount):
        # Convert the amount to an integer if needed
        
        amount = abs(amount)
        # Add the amount to the current credit_balance
        user.credit_balance -= amount
        # Save the updated user object
        user.save()
        # Save to Balance Logs
        log = Balance_Logs.objects.create(
            account_Owner = user.user,
            cashier_sender = cashier,
            amount = -amount,
            desc = "Cash Out",
        )  
        log.save()
        
        return JsonResponse({'status': 'success', 'message': 'Cash Out Successful, Please Check Your Load Balance'})
    else:
        return JsonResponse({'status': 'error', 'message': 'User not found, Contact Admin Immediately'})



       

@login_required(login_url='index')
@user_passes_test(user_has_cashier_group)
@require_POST
def insertServices(request):
    if request.method == 'POST':
        existing_menu_obj = menu.objects.filter(menu_name=request.POST['product'], menu_owner_id=request.user.id)
        if existing_menu_obj.exists():
            if existing_menu_obj.first().menu_is_active == 1:
                messages.error(request, "Product Already Exists!")
            elif existing_menu_obj.first().menu_is_active == 0:
                insName = request.POST['product']
                insPrice = request.POST['product_price']
                menu_item = menu.objects.get(menu_name=insName)
                menu_item.menu_name = insName
                menu_item.menu_price = insPrice
                menu_item.menu_is_active = 1
                menu_item.menu_owner_id = request.user.id
                menu_item.save(update_fields=['menu_name', 'menu_price', 'menu_is_active', 'menu_owner_id'])
                messages.success(request, "Product Successfully Added!")
        else:
            insName = request.POST['product']
            insPrice = request.POST['product_price']
            insMenu=menu(menu_name=insName, menu_price=insPrice, menu_owner_id=(request.user.id))
            insMenu.save()
            messages.success(request, "Product Successfully Added!")
    return redirect(request.META['HTTP_REFERER'])





@login_required(login_url='index')
@user_passes_test(user_has_cashier_group)
@require_GET
def cashier_services(request):
    
    menu_data = menu.objects.filter(menu_owner_id=request.user.id, menu_is_active=True).order_by('id')
    paginator = Paginator(menu_data, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count = menu_data.count()
    context = {
        'count' : count,
        'page_obj': page_obj,
        'menu_data': menu_data
    }

    return render(request, "cash_div/c_product.html", context)


@login_required(login_url='index')
@user_passes_test(user_has_cashier_group)
def updateServices(request, item_id):
    menu_item = menu.objects.get(id=item_id)

    if request.method == 'POST':
        updated_name = request.POST.get('product')
        updated_price = request.POST.get('product_price')

        if updated_name or updated_price:  # Check if any field is updated
            if updated_name:
                if menu.objects.filter(menu_name=updated_name).exists():
                    messages.success(request, "Product Name Already Taken")
                    return redirect(request.META.get('HTTP_REFERER'))
                else:
                    menu_item.menu_name = updated_name
            if updated_price:
                menu_item.menu_price = updated_price

            menu_item.save(update_fields=['menu_name', 'menu_price'])
            messages.success(request, "Product Successfully Updated!")
        else:
            messages.error(request, "Nothing to Update.")
            return redirect(request.META.get('HTTP_REFERER'))

        return redirect(request.META.get('HTTP_REFERER'))
    



@login_required(login_url='index') 
@user_passes_test(user_has_cashier_group)
def deleteServices(request, item_id):
    menu_item = menu.objects.get(id=item_id)

    if request.method == 'POST':
        menu_item.menu_is_active = 0
        menu_item.save()
        messages.success(request, "Product Deleted!")
    return redirect(request.META['HTTP_REFERER'])



@login_required(login_url='index')  
@user_passes_test(user_has_cashier_group)
def searchServices(request):
    search_string = request.GET.get('query')
    if search_string:
        menu_data = menu.objects.filter(
            menu_name__icontains=search_string, 
            menu_owner_id=request.user.id, 
            menu_is_active=True
        ).order_by('id')
    else:
        menu_data = menu.objects.filter(menu_owner_id=request.user.id, menu_is_active=True).order_by('id')
    paginator = Paginator(menu_data, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count = menu_data.count()
    context = {
        'count' : count,
        'page_obj': page_obj,
        'menu_data': menu_data,
        'search_string': search_string
    }

    return render(request, "cash_div/c_product.html", context)








@user_passes_test(user_has_cashier_group)
@require_POST
def validate_refnum(request):
    refnum = request.POST.get('refnum')
    
    if Order.objects.filter(paid=1, reference_number=refnum).exists():
        return JsonResponse({'exists': 2})
    elif Order.objects.filter(paid=0, reference_number=refnum).exists():
        return JsonResponse({'exists': 1})
    else:
        return JsonResponse({'exists': 0})



@login_required(login_url='index') 
@user_passes_test(user_has_cashier_group)
@require_GET
def cashier_order_info(request):
    refnum = request.GET.get('refnum')
    order = Order.objects.filter(reference_number=refnum).first()
    student_id = order.enduser.school_id
    orderlist = order.get_items()
    total_price=0
    refnum = order.reference_number
    item_details = []
    for item in orderlist:
        item_id = item[0]
        qty = int(item[1])
        service_obj = service.objects.filter(id=item_id).first()
        if service_obj:
            price = service_obj.price
            name = service_obj.name
            item_data = {
                'id': item_id,
                'name': name,
                'price': price*qty,
                'qty': qty
            }
            item_details.append(item_data)
            total_price += int(price * qty)
    item_details = json.dumps(item_details, cls=DjangoJSONEncoder)
    return JsonResponse({'cart': item_details, 'total_price': total_price, 'student_id': student_id, 'reference_number': refnum})












@login_required(login_url='index')
@require_POST
def pay_rfid(request):
    rfid = request.POST.get('rfid')
    rfid = hashlib.sha256(rfid.encode()).hexdigest()
    amount = request.POST.get('FinalTotalAmount')
    refnum = request.POST.get('refnum')
    user = EndUser.objects.filter(rfid_code=rfid).first()
    cashier = Cashier.objects.get(user=request.user)
    order = Order.objects.get(reference_number=refnum)
    # Convert the amount to an integer if needed
    amount = float(amount)
    amount = abs(amount)
    if user.credit_balance > amount:
        # Deduct the amount from the current credit_balance
        user.credit_balance -= amount
        # Save the updated user object
        user.save()
        
        cashier.credit_balance += amount
        cashier.save()

        order.paid = 1
        order.save()
        
        # Save to Balance Logs
        log = Balance_Logs.objects.create(
            account_Owner=user,
            cashier_sender=cashier,
            amount=-(amount),
            desc="Fee Payment",
        )  
        log.save()

        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        response_data = {
            'status': 'success',
            'message': 'Payment Successful, Please Check Your Load Balance',
            'school_id': user.school_id,
            'current_datetime': current_datetime
        }
        
        return JsonResponse(response_data)
    else:
        return JsonResponse({'status': 'error', 'message': 'User does not have enough credits'})







# ---------------------------------------------------------------------------------------------------------------------------------------
# Transaction Logs
# ---------------------------------------------------------------------------------------------------------------------------------------


@login_required(login_url='index')
@user_passes_test(user_has_cashier_group)
def cashdiv_transaction(request):
    cashier = Cashier.objects.get(user=request.user)
    loglist = Balance_Logs.objects.filter(cashier_sender=cashier).order_by('-id')
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
    return render(request, "cash_div/c_transaction.html", context)








@login_required(login_url='index')
@user_passes_test(user_has_cashier_group)
def searchTransaction(request):
    cashier = Cashier.objects.get(user=request.user)
    search_string = request.GET.get('query')
    date_string = request.GET.get('date')
    
    loglist = Balance_Logs.objects.filter(cashier_sender=cashier).order_by('-id')
    
    if search_string:
        loglist = loglist.filter(Q(account_Owner__enduser__school_id=search_string) | Q(account_Owner__pos__school_id=search_string))
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
    return render(request, "cash_div/c_transaction.html", context)



# joint function of showing list and adding enduser account
@user_passes_test(user_has_cashier_group)
@login_required(login_url='index')
def balances_enduser_list(request):
    CustomUser = get_user_model()
    template = 'cash_div/c_transaction_enduserlist.html'
    enduser_group = Group.objects.get(name='enduser')
    # Search Mechanism---------------------------------------------------------------------------------------------------------
    # Get the search query from the request
    search_query = request.GET.get('query')

    if search_query:
        # Apply search filter to the queryset
        enduser_data = CustomUser.objects.filter(
            Q(groups=enduser_group),
            Q(is_active=1),
            Q(enduser__school_id__icontains=search_query)
        ).order_by('id')
    else:
        enduser_data = CustomUser.objects.filter(groups=enduser_group, is_active=1).order_by('id')

    paginator = Paginator(enduser_data, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count = enduser_data.count()
    context = {
        'count' : count,
        'page_obj': page_obj,
    }
      
    return render(request, template, context)

# joint function of showing list and adding enduser account
@user_passes_test(user_has_cashier_group)
@login_required(login_url='index')
def balances_pos_list(request):
    CustomUser = get_user_model()
    template = 'cash_div/c_transaction_poslist.html'
    pos_group = Group.objects.get(name='pos')
    # Search Mechanism---------------------------------------------------------------------------------------------------------
    # Get the search query from the request
    search_query = request.GET.get('query')

    if search_query:
        # Apply search filter to the queryset
        pos_data = CustomUser.objects.filter(
            Q(groups=pos_group),
            Q(is_active=1),
            Q(pos__school_id__icontains=search_query)
        ).order_by('id')
    else:
        pos_data = CustomUser.objects.filter(groups=pos_group, is_active=1).order_by('id')

    paginator = Paginator(pos_data, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count = pos_data.count()
    context = {
        'count' : count,
        'page_obj': page_obj,
    }
      
    return render(request, template, context)











@login_required(login_url='index')
@user_passes_test(user_has_cashier_group)
def cashdiv_transactions_user(request, account_id, group):
    user = CustomUser.objects.get(id=account_id)  
    loglist = Balance_Logs.objects.filter(account_Owner=user).order_by('-id')
    if hasattr(user, 'enduser'):
        sid = user.enduser.school_id
    elif hasattr(user, 'pos'):
        sid = user.pos.school_id
    
    paginator = Paginator(loglist, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count = loglist.count()
    form = LogSearchForm()
    context = {
        'form': form,
        'count' : count,
        'page_obj': page_obj,
        'school_id': sid,
        'account_id': account_id,
        'group': group  
    }
    return render(request, "cash_div/c_transaction_user.html", context)



@login_required(login_url='index')
@user_passes_test(user_has_cashier_group)
def cashdiv_transactions_user_search(request, account_id, group):
    search_string = request.GET.get('query')
    date_string = request.GET.get('date')
    user = CustomUser.objects.get(id=account_id)  
    loglist = Balance_Logs.objects.filter(account_Owner=user).order_by('-id')
    if hasattr(user, 'enduser'):
        sid = user.enduser.school_id
    elif hasattr(user, 'pos'):
        sid = user.pos.school_id
    

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
    form = LogSearchForm()
    context = {
        'form': form,
        'count' : count,
        'page_obj': page_obj,
        'school_id': sid,
        'account_id': account_id,
        'group': group  
    }
    return render(request, "cash_div/c_transaction_user.html", context)
