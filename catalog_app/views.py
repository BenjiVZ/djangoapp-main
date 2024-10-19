from django.shortcuts import render
from django.http import HttpResponse
from myapp.models import Producto
from django.conf import settings

# Create your views here.

def catalog(request):
    productos = Producto.objects.all()
    data = {
        'productos': productos,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, "catalog.html", data)

def catalogue(request):
    productos = Producto.objects.all()
    data = {
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'catalogue.html', {'productos': productos})