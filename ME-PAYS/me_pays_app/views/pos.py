from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from me_pays_app.forms import *
from me_pays_app.models.pos import menu
from django.core.paginator import Paginator
from django.db.models import Q
import logging
import hashlib
from django.http import JsonResponse
from me_pays_app.models.balance import Balance_Logs
from datetime import datetime
from django.db.models import Sum
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
import json
def user_has_pos_group(user):
    return user.groups.filter(name='pos').exists()


@login_required(login_url='index')
@user_passes_test(user_has_pos_group)
def insertMenu(request):
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

@user_passes_test(user_has_pos_group)
@login_required(login_url='index')
def updateMenu(request, item_id):
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
@user_passes_test(user_has_pos_group)
def deleteMenu(request, item_id):
    menu_item = menu.objects.get(id=item_id)

    if request.method == 'POST':
        menu_item.menu_is_active = 0
        menu_item.save()
        messages.success(request, "Product Deleted!")
    return redirect(request.META['HTTP_REFERER'])

@login_required(login_url='index')  
def tallyItems(request):
    selectedValues = json.loads(request.GET.get('selectedValues'))
    item_data = []
    print (selectedValues)
    # Fetch the item details and add them to the item_data list
    for item in selectedValues:
        item_id = item[0]
        quantity = int(item[1])
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
@user_passes_test(user_has_pos_group)
def FetchProducts(request):
    services = menu.objects.filter(
        menu_is_active=1, menu_owner=request.user
    ).order_by('menu_name')

    # Serialize the QuerySet data to a list of dictionaries
    serialized_services = serializers.serialize('python', services)

    # Extract the fields from the serialized data
    services_data = [item['fields'] for item in serialized_services]

    # Include the 'id' field by using the values() method
    services_with_ids = services.values('id', *services_data[0].keys())
    return JsonResponse({'services': list(services_with_ids)})


@login_required(login_url='index')
@user_passes_test(user_has_pos_group)
@require_POST
def cpay_rfid(request):
    rfid = request.POST.get('rfid')
    rfid = hashlib.sha256(rfid.encode()).hexdigest()
    amount = request.POST.get('FinalTotalAmount')
    user = EndUser.objects.filter(rfid_code=rfid).first()
    pos = POS.objects.get(user=request.user)
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
            pos_sender=pos,
            amount=-(amount),
            desc="POS Transaction",
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



@login_required(login_url='index')
@user_passes_test(user_has_pos_group)
@require_POST
def cload_validate_rfid(request):
    rfid = request.POST.get('rfid')
    rfid = hashlib.sha256(rfid.encode()).hexdigest()
    if EndUser.objects.filter(rfid_code=rfid, user__is_active=1).exists():
        # RFID instance already exists
        return JsonResponse({'exists': 0})
    else:
        # RFID code does not exist in the database
        return JsonResponse({'exists': 1})






@user_passes_test(user_has_pos_group)
@login_required(login_url='index')
def canteen_home(request):
    # initialize available products
    products = menu.objects.filter(
        menu_owner_id=request.user.id,
        menu_is_active=1 
    ).order_by('menu_name')

    current_date = datetime.now().date()
    pos = POS.objects.get(user=request.user)
    dailyPay = Balance_Logs.objects.filter(pos_sender=pos, desc='POS Transaction', datetime__date=current_date)
    # Initializes the Counts
    dailyPayCount = dailyPay.count()
    # Initializes the Total Amounts
    totalPay = dailyPay.aggregate(total_amount=Sum('amount'))['total_amount']
    UserAccount = CustomUser.objects.filter(id=request.user.id).first()
    POSCreds = POS.objects.filter(user=UserAccount).first()
    context={
        'dailyPayCount':dailyPayCount,
        'products':products,
        'dailyTotalPay': totalPay,
        'pos': POSCreds,
    }




    return render(request, "canteen/canteen_home.html", context)
    



@user_passes_test(user_has_pos_group)
@login_required(login_url='index')  
def searchProduct(request):
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
        'menu_data': menu_data
    }

    return render(request, "canteen/canteen_products.html", context)
    







@user_passes_test(user_has_pos_group)
@login_required(login_url='index')
def canteen_products(request):
    
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

    return render(request, "canteen/canteen_products.html", context)










@login_required(login_url='index')
@user_passes_test(user_has_pos_group)
def canteen_history(request):
    pos = POS.objects.get(user=request.user)
    loglist = Balance_Logs.objects.filter(pos_sender=pos).order_by('-id')
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
    return render(request, "canteen/canteen_history.html", context)








@login_required(login_url='index')
@user_passes_test(user_has_pos_group)
def searchHistory(request):
    pos = POS.objects.get(user=request.user)
    search_string = request.GET.get('query')
    date_string = request.GET.get('date')
    
    loglist = Balance_Logs.objects.filter(pos_sender=pos).order_by('-id')
    
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
    return render(request, "canteen/canteen_history.html", context)