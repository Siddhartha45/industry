from django.shortcuts import redirect


def superadmin_required(view_func):
    """Decorators which lets users access views if their role is superaadmin or 1"""
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 1:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('home')
    return wrap


def admin_required(view_func):
    """Decorators which lets users access views if their role is admin or 2"""
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 2:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('home')
    return wrap
