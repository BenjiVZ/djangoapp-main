from django.http import HttpResponseForbidden

def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.profile.role == 'admin':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
    return wrapper_func
