from django.http import HttpResponse
from django.shortcuts import redirect
#if the user is logged in they will be directed to their home page
#a decorater to be used above the function if needed
def unauthenticated_user(view_func):
    def wrapper_func(request, *args,**kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args,**kwargs)
    return wrapper_func


# a decorator that will prevent users from viewing certain pages, depeneding
# on their groups
def allowed_users(allowed_roles=[]):
    def decorator (view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("not authorized")
        return wrapper_func
    return decorator