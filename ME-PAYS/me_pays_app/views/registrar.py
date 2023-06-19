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
from me_pays_app.models.order import *
import hashlib
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.db.models import Q
from me_pays_app.forms import *
from django.db.models import Sum
def user_has_registrar_group(user):
    return user.groups.filter(name='registrar').exists()





@login_required(login_url='index')
@user_passes_test(user_has_registrar_group)
def registrar_home(request):
    # initialize available services
    services = service.objects.filter(
        is_active=1 
    ).order_by('name')
    context={
        'services':services,
    }
    return render(request, "registrar/r_home.html", context)





@login_required(login_url='index')
@user_passes_test(user_has_registrar_group)
def registrar_account(request):
    return render(request, "registrar/r_account.html", {})








@login_required(login_url='index')
@user_passes_test(user_has_registrar_group)
def registrar_transaction(request):
    orderlist = Order.objects.filter().order_by('paid')
    paginator = Paginator(orderlist, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count = orderlist.count()
    form = LogSearchForm()
    context = {
        'form': form,
        'count' : count,
        'page_obj': page_obj,
    }
    return render(request, "registrar/r_transaction.html", context)







@login_required(login_url='index')
@user_passes_test(user_has_registrar_group)
def search_RegistrarTransaction(request):
    search_string = request.GET.get('query')
    date_string = request.GET.get('date')
    
    orderlist = Order.objects.filter().order_by('paid')
    
    if search_string:
        orderlist = orderlist.filter(reference_number__icontains=search_string).order_by('paid')
    
    if date_string:
        try:
            date = datetime.strptime(date_string, '%Y-%m-%d').date()
            orderlist = orderlist.filter(datetime__date=date)
        except ValueError:
            pass
    
    paginator = Paginator(orderlist, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count = orderlist.count()
    
    context = {
        'count': count,
        'page_obj': page_obj,
        'search_string': search_string,  # Pass the search query back to the template
        'date_string': date_string,      # Pass the date input back to the template
    }
    return render(request, "registrar/r_transaction.html", context)



@login_required(login_url='index') 
@user_passes_test(user_has_registrar_group)
def registrar_transaction_info(request, order_id):
    order = Order.objects.filter(id=order_id).first()
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

    context = {
        'cart': item_details,
        'total_price': total_price,
        'student_id': student_id,
        'reference_number': refnum
    }
    return render(request, "registrar/r_transinfo.html", context)









# def updateStats(request):
#     # initialize available services
#     current_date = datetime.now().date()
#     cashier = Cashier.objects.get(user=request.user)
#     dailyCashIn = Balance_Logs.objects.filter(cashier_sender=cashier, desc='Cash In', datetime__date=current_date)
#     dailyPay = Balance_Logs.objects.filter(cashier_sender=cashier, desc='Payment', datetime__date=current_date)
#     # Initializes the Counts
#     dailyCashInCount = dailyCashIn.count()
#     dailyPayCount = dailyPay.count()
#     # Initializes the Total Amounts
#     totalCashIn = dailyCashIn.aggregate(total_amount=Sum('amount'))['total_amount']
#     totalPay = dailyPay.aggregate(total_amount=Sum('amount'))['total_amount']
#     if totalPay is None:
#         totalPay=0
#     context={
#         'dailyCashInCount': dailyCashInCount,
#         'dailyPayCount': dailyPayCount,
#         'dailyTotalCashIn': totalCashIn,
#         'dailyTotalPay': -totalPay,
#     }
#     return JsonResponse(context)







# @login_required(login_url='index')
# @user_passes_test(user_has_cashier_group)
# def cashdiv_home(request):
#     # initialize available services
#     services = menu.objects.filter(
#         menu_owner_id=request.user.id,
#         menu_is_active=1 
#     ).order_by('menu_name')
#     current_date = datetime.now().date()
#     cashier = Cashier.objects.get(user=request.user)
#     dailyCashIn = Balance_Logs.objects.filter(cashier_sender=cashier, desc='Cash In', datetime__date=current_date)
#     dailyPay = Balance_Logs.objects.filter(cashier_sender=cashier, desc='Payment', datetime__date=current_date)
#     # Initializes the Counts
#     dailyCashInCount = dailyCashIn.count()
#     dailyPayCount = dailyPay.count()
#     # Initializes the Total Amounts
#     totalCashIn = dailyCashIn.aggregate(total_amount=Sum('amount'))['total_amount']
#     totalPay = dailyPay.aggregate(total_amount=Sum('amount'))['total_amount']
#     UserAccount = CustomUser.objects.filter(id=request.user.id).first()
#     CashierCreds = Cashier.objects.filter(user=UserAccount).first()
#     context={
#         'dailyCashInCount':dailyCashInCount,
#         'dailyPayCount':dailyPayCount,
#         'services':services,
#         'dailyTotalCashIn': totalCashIn,
#         'dailyTotalPay': totalPay,
#         'cashier': CashierCreds
#     }
#     return render(request, "cash_div/c_home.html", context)
 

# @user_passes_test(user_has_cashier_group)
# @require_GET
# def validate_SID(request):
#     student_id = request.GET.get('school_id')
    
#     if EndUser.objects.filter(school_id=student_id, user__is_active=1, rfid_code__isnull=True).exists():
#         # Student ID is active and doesn't have an associated RFID
#         return JsonResponse({'exists': 2})
#     elif EndUser.objects.filter(school_id=student_id, user__is_active=1).exists():
#         # Student ID already has an RFID associated and is active
#         return JsonResponse({'exists': 3})
#     elif EndUser.objects.filter(school_id=student_id, user__is_active=0).exists():
#         # Student ID is inactive
#         return JsonResponse({'exists': 1})
#     else:
#     # Student ID does not exist in the database
#         return JsonResponse({'exists': 0})
    
# @user_passes_test(user_has_cashier_group)
# @require_GET
# def load_validate_SID(request):
#     student_id = request.GET.get('school_id')
    
#     if EndUser.objects.filter(school_id=student_id, user__is_active=1, rfid_code__isnull=True).exists():
#         # Student ID is active and doesn't have an associated RFID
#         return JsonResponse({'exists': 2})
#     elif EndUser.objects.filter(school_id=student_id, user__is_active=1).exists():
#         # Student ID has an RFID associated
#         return JsonResponse({'exists': 1})
#     else:
#     # Student ID does not exist in the database
#         return JsonResponse({'exists': 3})

# @user_passes_test(user_has_cashier_group)
# @require_POST
# def register_rfid_code(request):
#     school_id = request.POST.get('school_id')
#     rfid = request.POST.get('rfid')
#     rfid = hashlib.sha256(rfid.encode()).hexdigest()
#     try:
#         end_user = EndUser.objects.get(school_id=school_id)
#         end_user.rfid_code = rfid
#         end_user.save()

#         return JsonResponse({'success': True, 'message': 'Registration Successful'})
#     except EndUser.DoesNotExist:
#         return JsonResponse({'success': False, 'message': 'EndUser not found; Call the Administrator Immediately'})
    
 









# @user_passes_test(user_has_cashier_group)
# @require_GET
# def validate_rfid(request):
#     rfid = request.GET.get('rfid')
#     hashed_rfid = hashlib.sha256(rfid.encode()).hexdigest()
#     end_user = EndUser.objects.filter(rfid_code=hashed_rfid, user__is_active=1).first()
    
#     if end_user is not None:
#         # RFID instance already exists
#         return JsonResponse({'exists': 1})
#     else:
#         # RFID code does not exist in the database
#         return JsonResponse({'exists': 0})
    


# @user_passes_test(user_has_cashier_group)
# @require_POST
# def load_validate_rfid(request):
#     rfid = request.POST.get('rfid')
#     rfid = hashlib.sha256(rfid.encode()).hexdigest()
#     if EndUser.objects.filter(rfid_code=rfid, user__is_active=1).exists():
#         # RFID instance already exists
#         return JsonResponse({'exists': 0})
#     else:
#         # RFID code does not exist in the database
#         return JsonResponse({'exists': 1})
    
# @user_passes_test(user_has_cashier_group)
# @require_GET
# def  load_rfid_creds(request):
#     rfid = request.GET.get('rfid')
#     rfid = hashlib.sha256(rfid.encode()).hexdigest()
#     user=EndUser.objects.filter(rfid_code=rfid).first()
#     fullname = user.first_name+" "+user.last_name
#     response = {
#         'fullname': fullname,
#         'personID': user.school_id
#     }
#     return JsonResponse(response)


# @user_passes_test(user_has_cashier_group)
# @require_GET
# def load_cred_amount(request):
#     rfid = request.GET.get('rfid')
#     rfid = hashlib.sha256(rfid.encode()).hexdigest()
#     amount = request.GET.get('amount')
#     user=EndUser.objects.filter(rfid_code=rfid).first()
#     cashier = Cashier.objects.get(user=request.user)
#     if user is not None:
#         # Convert the amount to an integer if needed
#         amount = int(amount)
#         totalamount = amount*1.05
#         # Add the amount to the current credit_balance
#         user.credit_balance += totalamount
#         # Save the updated user object
#         user.save()
#         # Save to Balance Logs
#         log = Balance_Logs.objects.create(
#             account_Owner = user,
#             cashier_sender = cashier,
#             amount = amount,
#             desc = "Cash In",
#         )  
#         log.save()

#         return JsonResponse({'status': 'success', 'message': 'Payment Successful, Please Check Your Load Balance'})
#     else:
#         return JsonResponse({'status': 'error', 'message': 'User not found, Contact Admin Immediately'})



       


@login_required(login_url='index')
@user_passes_test(user_has_registrar_group)
@require_POST
def insertServices(request):
    if request.method == 'POST':
        existing_menu_obj = service.objects.filter(name=request.POST['product'])
        if existing_menu_obj.exists():
            if existing_menu_obj.first().is_active == 1:
                messages.error(request, "Service Already Exists!")
            elif existing_menu_obj.first().is_active == 0:
                insName = request.POST['product']
                insPrice = request.POST['product_price']
                item = service.objects.get(name=insName)
                item.name = insName
                item.price = insPrice
                item.is_active = 1
                item.save(update_fields=['name', 'price', 'is_active'])
                messages.success(request, "Service Successfully Added!")
        else:
            insName = request.POST['product']
            insPrice = request.POST['product_price']
            item=service(name=insName, price=insPrice)
            item.save()
            messages.success(request, "Service Successfully Added!")
    return redirect(request.META['HTTP_REFERER'])





@login_required(login_url='index')
@user_passes_test(user_has_registrar_group)
@require_GET
def registrar_services(request):
    
    data = service.objects.filter(is_active=True).order_by('id')
    paginator = Paginator(data, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count = data.count()
    context = {
        'count' : count,
        'page_obj': page_obj,
    }

    return render(request, "registrar/r_product.html", context)


@login_required(login_url='index')
@user_passes_test(user_has_registrar_group)
def updateServices(request, item_id):
    item = service.objects.get(id=item_id)

    if request.method == 'POST':
        updated_name = request.POST.get('product')
        updated_price = request.POST.get('product_price')

        if updated_name or updated_price:  # Check if any field is updated
            if updated_name:
                if service.objects.filter(name=updated_name).exists():
                    messages.success(request, "Service Name Already Taken")
                    return redirect(request.META.get('HTTP_REFERER'))
                else:
                    item.name = updated_name
            if updated_price:
                item.price = updated_price

            item.save(update_fields=['name', 'price'])
            messages.success(request, "Service Successfully Updated!")
        else:
            messages.error(request, "Nothing to Update.")
            return redirect(request.META.get('HTTP_REFERER'))

        return redirect(request.META.get('HTTP_REFERER'))
    



@login_required(login_url='index') 
@user_passes_test(user_has_registrar_group)
def deleteServices(request, item_id):
    item = service.objects.get(id=item_id)

    if request.method == 'POST':
        item.is_active = 0
        item.save()
        messages.success(request, "Service Deleted!")
    return redirect(request.META['HTTP_REFERER'])



@login_required(login_url='index') 
@user_passes_test(user_has_registrar_group)
def searchServices(request):
    search_string = request.GET.get('query')
    if search_string:
        data = service.objects.filter(
            name__icontains=search_string, 
            is_active=True
        ).order_by('id')
    else:
        data = service.objects.filter(is_active=True).order_by('id')
    paginator = Paginator(data, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count = data.count()
    context = {
        'count' : count,
        'page_obj': page_obj,
        'search_string': search_string
    }

    return render(request, "registrar/r_product.html", context)




@login_required(login_url='index') 
@user_passes_test(user_has_registrar_group)
def FetchServices(request):
    services = service.objects.filter(
        is_active=1
    ).order_by('name')

    # Serialize the QuerySet data to a list of dictionaries
    serialized_services = serializers.serialize('python', services)

    # Extract the fields from the serialized data
    services_data = [item['fields'] for item in serialized_services]

    # Include the 'id' field by using the values() method
    services_with_ids = services.values('id', *services_data[0].keys())
    return JsonResponse({'services': list(services_with_ids)})






@login_required(login_url='index') 
@user_passes_test(user_has_registrar_group)
@require_GET
def registrar_validate_SID(request):
    student_id = request.GET.get('school_id')
    if EndUser.objects.filter(school_id=student_id, user__is_active=1).exists():
        # Student ID is active and doesn't have an associated RFID
        return JsonResponse({'exists': 1})
    else:
    # Student ID does not exist in the database
        return JsonResponse({'exists': 0})


@login_required(login_url='index') 
@user_passes_test(user_has_registrar_group)
@require_POST
def registrar_sendItems(request):
    school_id = request.POST.get('school_id')
    enduser = get_object_or_404(EndUser, school_id=school_id)

    order = Order.objects.create(
        enduser=enduser,
        items=request.POST.get('selectedValues'),
    )

    refnum = order.reference_number

    return JsonResponse({'refnum': refnum})




@login_required(login_url='index')  
@require_GET
def registrar_tallyItems(request):
    selectedValues = json.loads(request.GET.get('selectedValues'))
    item_data = []
    
    # Fetch the item details and add them to the item_data list
    for item in selectedValues:
        item_id = item[0]
        quantity = item[1]
        try:
            service_item = service.objects.get(id=int(item_id), is_active=1)
            item_data.append({
                'id': item_id,
                'name': service_item.name,
                'price': service_item.price * int(quantity),
                'quantity': int(quantity),
                # Add more fields as needed
            })
        except service.DoesNotExist:
            # Handle the case if the item is not found
            pass

    serialized_data = json.dumps(item_data, cls=DjangoJSONEncoder)
    return JsonResponse({'itemlist': serialized_data})



# @login_required(login_url='index')
# @require_POST
# def pay_rfid(request):
#     rfid = request.POST.get('rfid')
#     rfid = hashlib.sha256(rfid.encode()).hexdigest()
#     amount = request.POST.get('FinalTotalAmount')
#     user = EndUser.objects.filter(rfid_code=rfid).first()
#     cashier = Cashier.objects.get(user=request.user)
#     # Convert the amount to an integer if needed
#     amount = int(amount)
    
#     if user.credit_balance > amount:
#         # Deduct the amount from the current credit_balance
#         user.credit_balance -= amount
#         # Save the updated user object
#         user.save()
        
#         # Save to Balance Logs
#         log = Balance_Logs.objects.create(
#             account_Owner=user,
#             cashier_sender=cashier,
#             amount=-(amount),
#             desc="Payment",
#         )  
#         log.save()

#         current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
#         response_data = {
#             'status': 'success',
#             'message': 'Payment Successful, Please Check Your Load Balance',
#             'school_id': user.school_id,
#             'current_datetime': current_datetime
#         }
        
#         return JsonResponse(response_data)
#     else:
#         return JsonResponse({'status': 'error', 'message': 'User does not have enough credits'})







# # ---------------------------------------------------------------------------------------------------------------------------------------
# # Transaction Logs
# # ---------------------------------------------------------------------------------------------------------------------------------------


# @login_required(login_url='index')
# @user_passes_test(user_has_cashier_group)
# def cashdiv_transaction(request):
#     cashier = Cashier.objects.get(user=request.user)
#     loglist = Balance_Logs.objects.filter(cashier_sender=cashier).order_by('-id')
#     paginator = Paginator(loglist, 8)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     count = loglist.count()
#     form = LogSearchForm()
#     context = {
#         'form': form,
#         'count' : count,
#         'page_obj': page_obj,
#     }
#     return render(request, "cash_div/c_transaction.html", context)








# @login_required(login_url='index')
# @user_passes_test(user_has_cashier_group)
# def searchTransaction(request):
#     cashier = Cashier.objects.get(user=request.user)
#     search_string = request.GET.get('query')
#     date_string = request.GET.get('date')
    
#     loglist = Balance_Logs.objects.filter(cashier_sender=cashier).order_by('-id')
    
#     if search_string:
#         loglist = loglist.filter(Q(id=search_string))
    
#     if date_string:
#         try:
#             date = datetime.strptime(date_string, '%Y-%m-%d').date()
#             loglist = loglist.filter(datetime__date=date)
#         except ValueError:
#             pass
    
#     paginator = Paginator(loglist, 8)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     count = loglist.count()
    
#     context = {
#         'count': count,
#         'page_obj': page_obj,
#         'search_string': search_string,  # Pass the search query back to the template
#         'date_string': date_string,      # Pass the date input back to the template
#     }
#     return render(request, "cash_div/c_transaction.html", context)













