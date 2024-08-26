from django.shortcuts import render, redirect
from django.contrib import messages
from myapp.models import Producto

# Create your views here.

def home(request):
    productos_tendencia = Producto.objects.filter(tendencia=True)
    productos_populares = Producto.objects.filter(popular=True)
    data = {
        'tendencia': productos_tendencia,
        'populares': productos_populares
    }
    return render(request, 'home.html')

from django.contrib.auth.decorators import login_required

@login_required
def home_view(request):
    if request.user.profile.role == 'admin':
        return render(request, 'admin_dashboard.html')
    else:
        return render(request, 'user_dashboard.html')

def home_view(request):
    if not request.user.is_authenticated:
        return render(request, 'home.html')
    elif request.user.profile.role == 'admin':
        return redirect('admin:index')
    else:
        return render(request, 'home.html')

