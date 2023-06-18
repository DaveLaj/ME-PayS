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
    dailyPay = Balance_Logs.objects.filter(cashier_sender=cashier, desc='Payment', datetime__date=current_date)
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
    dailyPay = Balance_Logs.objects.filter(cashier_sender=cashier, desc='Payment', datetime__date=current_date)
    # Initializes the Counts
    dailyCashInCount = dailyCashIn.count()
    dailyPayCount = dailyPay.count()
    # Initializes the Total Amounts
    totalCashIn = dailyCashIn.aggregate(total_amount=Sum('amount'))['total_amount']
    totalPay = dailyPay.aggregate(total_amount=Sum('amount'))['total_amount']
    UserAccount = CustomUser.objects.filter(id=request.user.id).first()
    CashierCreds = Cashier.objects.filter(user=UserAccount).first()
    context={
        'dailyCashInCount':dailyCashInCount,
        'dailyPayCount':dailyPayCount,
        'services':services,
        'dailyTotalCashIn': totalCashIn,
        'dailyTotalPay': totalPay,
        'cashier': CashierCreds
    }
    return render(request, "cash_div/c_home.html", context)
 

@user_passes_test(user_has_cashier_group)
@require_GET
def validate_SID(request):
    student_id = request.GET.get('school_id')
    
    if EndUser.objects.filter(school_id=student_id, user__is_active=1, rfid_code__isnull=True).exists():
        # Student ID is active and doesn't have an associated RFID
        return JsonResponse({'exists': 2})
    elif EndUser.objects.filter(school_id=student_id, user__is_active=1).exists():
        # Student ID already has an RFID associated and is active
        return JsonResponse({'exists': 3})
    elif EndUser.objects.filter(school_id=student_id, user__is_active=0).exists():
        # Student ID is inactive
        return JsonResponse({'exists': 1})
    else:
    # Student ID does not exist in the database
        return JsonResponse({'exists': 0})
    
@user_passes_test(user_has_cashier_group)
@require_GET
def load_validate_SID(request):
    student_id = request.GET.get('school_id')
    
    if EndUser.objects.filter(school_id=student_id, user__is_active=1, rfid_code__isnull=True).exists():
        # Student ID is active and doesn't have an associated RFID
        return JsonResponse({'exists': 2})
    elif EndUser.objects.filter(school_id=student_id, user__is_active=1).exists():
        # Student ID has an RFID associated
        return JsonResponse({'exists': 1})
    else:
    # Student ID does not exist in the database
        return JsonResponse({'exists': 3})

@user_passes_test(user_has_cashier_group)
@require_POST
def register_rfid_code(request):
    school_id = request.POST.get('school_id')
    rfid = request.POST.get('rfid')
    rfid = hashlib.sha256(rfid.encode()).hexdigest()
    try:
        end_user = EndUser.objects.get(school_id=school_id)
        end_user.rfid_code = rfid
        end_user.save()

        return JsonResponse({'success': True, 'message': 'Registration Successful'})
    except EndUser.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'EndUser not found; Call the Administrator Immediately'})
    
 









@user_passes_test(user_has_cashier_group)
@require_GET
def validate_rfid(request):
    rfid = request.GET.get('rfid')
    hashed_rfid = hashlib.sha256(rfid.encode()).hexdigest()
    end_user = EndUser.objects.filter(rfid_code=hashed_rfid, user__is_active=1).first()
    
    if end_user is not None:
        # RFID instance already exists
        return JsonResponse({'exists': 1})
    else:
        # RFID code does not exist in the database
        return JsonResponse({'exists': 0})
    


@user_passes_test(user_has_cashier_group)
@require_POST
def load_validate_rfid(request):
    rfid = request.POST.get('rfid')
    rfid = hashlib.sha256(rfid.encode()).hexdigest()
    if EndUser.objects.filter(rfid_code=rfid, user__is_active=1).exists():
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
    user=EndUser.objects.filter(rfid_code=rfid).first()
    fullname = user.first_name+" "+user.last_name
    response = {
        'fullname': fullname,
        'personID': user.school_id
    }
    return JsonResponse(response)


@user_passes_test(user_has_cashier_group)
@require_GET
def load_cred_amount(request):
    rfid = request.GET.get('rfid')
    rfid = hashlib.sha256(rfid.encode()).hexdigest()
    amount = request.GET.get('amount')
    user=EndUser.objects.filter(rfid_code=rfid).first()
    cashier = Cashier.objects.get(user=request.user)
    if user is not None:
        # Convert the amount to an integer if needed
        amount = int(amount)
        totalamount = amount*1.05
        # Add the amount to the current credit_balance
        user.credit_balance += totalamount
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







@login_required(login_url='index')  
def tallyItems(request):
    selectedValues = json.loads(request.GET.get('selectedValues'))
    quantityTracker = {}
    item_data = []

    # Count the quantity for each item
    for item in selectedValues:
        if item in quantityTracker:
            quantityTracker[item] += 1
        else:
            quantityTracker[item] = 1

    # Fetch the item details and add them to the item_data list
    for item_id, quantity in quantityTracker.items():
        try:
            item = menu.objects.get(id=int(item_id), menu_is_active=1)
            item_data.append({
                'id': item_id,
                'name': item.menu_name,
                'price': item.menu_price * quantity,
                'quantity': quantity,
                # Add more fields as needed
            })
        except menu.DoesNotExist:
            # Handle the case if the item is not found
            pass

    serialized_data = json.dumps(item_data, cls=DjangoJSONEncoder)

    return JsonResponse({'itemlist': serialized_data})



@login_required(login_url='index')
@require_POST
def pay_rfid(request):
    rfid = request.POST.get('rfid')
    rfid = hashlib.sha256(rfid.encode()).hexdigest()
    amount = request.POST.get('FinalTotalAmount')
    user = EndUser.objects.filter(rfid_code=rfid).first()
    cashier = Cashier.objects.get(user=request.user)
    # Convert the amount to an integer if needed
    amount = int(amount)
    
    if user.credit_balance > amount:
        # Deduct the amount from the current credit_balance
        user.credit_balance -= amount
        # Save the updated user object
        user.save()
        
        # Save to Balance Logs
        log = Balance_Logs.objects.create(
            account_Owner=user,
            cashier_sender=cashier,
            amount=-(amount),
            desc="Payment",
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






from datetime import datetime

@login_required(login_url='index')
@user_passes_test(user_has_cashier_group)
def searchTransaction(request):
    cashier = Cashier.objects.get(user=request.user)
    search_string = request.GET.get('query')
    date_string = request.GET.get('date')
    
    loglist = Balance_Logs.objects.filter(cashier_sender=cashier).order_by('-id')
    
    if search_string:
        loglist = loglist.filter(Q(id=search_string))
    
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

