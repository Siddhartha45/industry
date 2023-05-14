from django.shortcuts import redirect


def superadmin_required(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 1:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('home')
    return wrap


def admin_required(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 2:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('home')
    return wrap