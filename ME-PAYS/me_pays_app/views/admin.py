from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from me_pays_app.forms import *
from me_pays_app.models.users import *
from django.core.paginator import Paginator
import logging
from django.http import HttpResponseRedirect
from django.db.models import Q

def user_has_admin_group(user):
    return user.groups.filter(name='admin').exists()


# joint function of showing list and adding POS account
@user_passes_test(user_has_admin_group)
@login_required(login_url='index')
def pos_list(request):
    CustomUser = get_user_model()
    template = 'admin/admin_listOfPOS.html'
    pos_group = Group.objects.get(name='pos')

    # Get the search query from the request
    search_query = request.GET.get('query')

    if search_query:
        # Apply search filter to the queryset
        pos_data = CustomUser.objects.filter(
            Q(groups=pos_group),
            Q(is_active=1),
            Q(email__icontains=search_query) | Q(pos__store_name__icontains=search_query) | Q(pos__contact_number__icontains=search_query)
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
        'pos_data': pos_data
    }
    if 'account_id' in request.POST:
        account_id = request.POST['account_id']
        return updatepos(request, account_id, template='admin/admin_listOfPOS.html')
    
    # No updatepos form submission, render the pos_list template
    else:
        form = POS_UpdateForm()
    
    context['update_form'] = form

    # if this is a POST request we need to process the form data for insert
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = POS_CreationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            if CustomUser.objects.filter(email = form.cleaned_data['email']).exists():
                messages.error(request, "Account already exists!")
            elif form.cleaned_data['password1'] != form.cleaned_data['password2']:
                messages.error(request, "Password do not match!")
            elif POS.objects.filter(contact_number = form.cleaned_data['contact_number']).exists():
                messages.error(request, "Contact Number already in use!")
            elif POS.objects.filter(store_name = form.cleaned_data['store_name']).exists():
                messages.error(request, "Store Name already in use!")
            else:
                # Create the user:

                user = CustomUser.objects.create_pos(
                    form.cleaned_data['email'],
                    form.cleaned_data['password1']
                )
                
                profile = POS.objects.create(
                user=user,
                store_name=form.cleaned_data['store_name'],
                contact_number=form.cleaned_data['contact_number'],
                location=form.cleaned_data['location'],
                description=form.cleaned_data['description'],
                )

                
                user.save()   
                profile.save()

                # Login the user
                messages.success(request, "POS Successfully Registered")
                return redirect(request.META['HTTP_REFERER'])   
        else:
            context['form']=form
            context['errors']=form.errors
            return render(request, template, context)
   # No post data availabe, let's just show the page.
    else:

        form = POS_CreationForm()
        context['form']=form
        
    return render(request, template, context)


@user_passes_test(user_has_admin_group)
@login_required(login_url='index')  
def updatepos(request, account_id, template='admin/admin_listOfPOS.html'):
    user = get_object_or_404(CustomUser, id=account_id)
    pos = user.pos  # Assuming the POS instance is associated with the user

    if request.method == 'POST':
        form = POS_UpdateForm(request.POST, instance=pos)
        if form.is_valid():
            form.save()
            messages.success(request, "Account Updated Successfully!")
            return redirect('admin_listOfPOS')  # Replace 'pos_list' with your actual URL name for the POS list view
    else:
        form = POS_UpdateForm(instance=pos)
    
    context = {
        'update': form,
    }
    return render(request, template, context)

@user_passes_test(user_has_admin_group)
@login_required(login_url='index')  
def deletepos(request, account_id):
    pos_data = CustomUser.objects.get(id=account_id)

    if request.method == 'POST':
        pos_data.is_active = 0
        pos_data.save()
        messages.success(request, "Account Deleted Successfully!")
    return redirect(request.META['HTTP_REFERER'])


@user_passes_test(user_has_admin_group)
@login_required(login_url='index')  
def change_password(request, user_id, template='admin/admin_listOfPOS.html'):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        form = POS_ChangePassword(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Password changed successfully!")
            return redirect('pos_list')  # Replace 'pos_list' with your actual URL name for the POS list view
    else:
        form = POS_ChangePassword(instance=user)

    context = {
        'changepass': form,
    }
    return render(request, template, context)


@user_passes_test(user_has_admin_group)
@login_required(login_url='index')  
def searchPOS(request):
    search_string = request.GET.get('query')
    if search_string:
        pos_data = CustomUser.objects.filter(
            menu_name__icontains=search_string, 
            menu_owner_id=request.user.id, 
            menu_is_active=True
        )
        return pos_list(request, pos_data)
    else:
        menu_data = CustomUser.objects.filter(menu_owner_id=request.user.id, menu_is_active=True)
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










