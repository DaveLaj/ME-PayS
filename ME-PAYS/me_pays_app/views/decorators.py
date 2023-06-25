from django.shortcuts import redirect
from django.http import HttpResponse


def redirect_if_logged_in(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.groups.all()[0].name=='admin':
                return redirect('admin_enable')
            elif request.user.groups.all()[0].name=='enduser':
                return redirect('home')
            elif request.user.groups.all()[0].name=='cashier':
                return redirect('cashdiv_home')
            elif request.user.groups.all()[0].name=='pos':
                return redirect('canteen_home')
            else:
                return HttpResponse('NotFound.')
        return view_func(request, *args, **kwargs)

    return wrapper


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            groups = request.user.groups.values_list('name', flat=True)  # Get a list of group names
            if any(group in allowed_roles for group in groups):
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page.')
        return wrapper_func
    return decorator
    

                














# def redirect_if_enduser(view_func):
#     def wrapper(request, *args, **kwargs):
#         if request.user.role == Role.ENDUSER:
#             return redirect('cashierhome')
#         return view_func(request, *args, **kwargs)
#     return wrapper



# def redirect_if_cashier(view_func):
#     def wrapper(request, *args, **kwargs):
#         if request.user.role == Role.CASHIER:
#             return redirect('cashierhome')
#         return view_func(request, *args, **kwargs)
#     return wrapper


# def redirect_if_admin(view_func):
#     def wrapper(request, *args, **kwargs):
#         if request.user.role == Role.ADMIN:
#             return redirect('cashierhome')
#         return view_func(request, *args, **kwargs)
#     return wrapper

