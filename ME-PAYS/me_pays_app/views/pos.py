from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.contrib import messages
from me_pays_app.forms import *
from me_pays_app.models.pos import menu
from django.core.paginator import Paginator
import logging

logger = logging.getLogger(__name__)

def user_has_pos_group(user):
    return user.groups.filter(name='pos').exists()

@user_passes_test(user_has_pos_group)
def insertMenu(request):
    if request.method == 'POST':
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
        updated_name = request.POST['product']
        updated_price = request.POST['product_price']

        menu_item.menu_name = updated_name
        menu_item.menu_price = updated_price
        menu_item.save()
        messages.success(request, "Product Successfully Updated!")
    return redirect(request.META['HTTP_REFERER'])


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
    

@login_required(login_url='index')
def canteen_products(request):

    menu_data = menu.objects.filter(menu_owner_id=(request.user.id), menu_is_active=True)
    paginator = Paginator(menu_data, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'menu_data': menu_data
    }
    return render(request, "canteen/canteen_products.html", context)


@login_required(login_url='index')
def canteen_history(request):
    return render(request, "canteen/canteen_history.html", {})




