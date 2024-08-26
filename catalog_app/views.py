from django.shortcuts import render
from django.http import HttpResponse
from myapp.models import Producto

# Create your views here.

def catalog(request):
    productos = Producto.objects.all()
    data = {
        'productos': productos
    }
    return render(request, "catalogue.html", data)