from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from cart_app.models import Producto, Carrito, CarritoItem
from django.conf import settings
from django.contrib.auth.decorators import login_required

# Create your views here.

def catalog(request):
    productos = Producto.objects.all()
    data = {
        'productos': productos,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, "catalog.html", data)

@login_required
def catalogue(request):
    productos = Producto.objects.all()
    # Obtener el carrito actual del usuario
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    num_items = sum(item.cantidad for item in carrito.items.all())
    
    data = {
        'productos': productos,
        'MEDIA_URL': settings.MEDIA_URL,
        'num_items': num_items,
    }
    return render(request, 'catalogue.html', data)

@login_required
def agregar_al_carrito(request, producto_id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        producto = get_object_or_404(Producto, id=producto_id)
        carrito, created = Carrito.objects.get_or_create(usuario=request.user)
        carrito_item, created = CarritoItem.objects.get_or_create(carrito=carrito, producto=producto)
        
        if not created:
            carrito_item.cantidad += 1
            carrito_item.save()
        
        # Obtener el número total de items en el carrito
        num_items = sum(item.cantidad for item in carrito.items.all())
        
        return JsonResponse({
            'status': 'success',
            'num_items': num_items
        })
    
    return redirect('cart')