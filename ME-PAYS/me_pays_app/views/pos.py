from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from me_pays_app.forms import *
from me_pays_app.models.pos import menu
from django.core.paginator import Paginator
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)

def user_has_pos_group(user):
    return user.groups.filter(name='pos').exists()

@user_passes_test(user_has_pos_group)
def insertMenu(request):
    if request.method == 'POST':
        existing_menu_obj = menu.objects.filter(menu_name=request.POST['product'])
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
                menu_item.save(update_fields=['menu_name', 'menu_price', 'menu_is_active'])
                messages.success(request, "Product Successfully Added!")
        else:
            insName = request.POST['product']
            insPrice = request.POST['product_price']
            insMenu=menu(menu_name=insName, menu_price=insPrice, menu_owner_id=(request.user.id))
            insMenu.save()
            messages.success(request, "Product Successfully Added!")
    return redirect(request.META['HTTP_REFERER'])

@user_passes_test(user_has_pos_group)
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
            messages.error(request, "Process Failure please contact admin")
            return redirect(request.META.get('HTTP_REFERER'))

        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.success(request, "Nothing to Update!")
        return redirect(request.META.get('HTTP_REFERER'))


@user_passes_test(user_has_pos_group)
def deleteMenu(request, item_id):
    menu_item = menu.objects.get(id=item_id)

    if request.method == 'POST':
        menu_item.menu_is_active = 0
        menu_item.save()
        messages.success(request, "Product Deleted!")
    return redirect(request.META['HTTP_REFERER'])



@login_required(login_url='index')
def canteen_home(request):
    return render(request, "canteen/canteen_home.html", {})
    



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
def canteen_history(request):
    return render(request, "canteen/canteen_history.html", {})




