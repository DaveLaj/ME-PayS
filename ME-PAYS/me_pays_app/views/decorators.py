from django.shortcuts import redirect

def redirect_if_logged_in(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')  # replace 'home' with your desired URL
        return view_func(request, *args, **kwargs)
    return wrapper