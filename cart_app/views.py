# cart/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Carrito, CarritoItem
from myapp.models import Producto  # Importa el modelo Producto desde la app myapp
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

@login_required
def agregar_al_carrito(request, producto_id):
    """
    Vista para agregar un producto al carrito del usuario.
    """
    producto = get_object_or_404(Producto, id=producto_id)
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    carrito_item, created = CarritoItem.objects.get_or_create(carrito=carrito, producto=producto)
    
    if not created:
        carrito_item.cantidad += 1
        carrito_item.save()
    
    messages.success(request, f'{producto.nombre} ha sido agregado al carrito.')
    return redirect('cart')  # Redirige a la vista del carrito

@login_required
def cart(request):
    """
    Vista para mostrar los productos en el carrito de compras del usuario.
    """
    data = {
        'MEDIA_URL': settings.MEDIA_URL,
    }
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    items = carrito.items.all()
    total = sum(item.get_total_item_price() for item in items)
    return render(request, 'cart.html', {'items': items, 'total': total})

@login_required
def generar_factura(request):
    """
    Vista para generar una factura a partir de los productos en el carrito.
    """
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    carrito.items.all().delete()  # Limpia el carrito
    messages.success(request, 'La factura ha sido generada exitosamente.')
    return redirect('catalogue')  # Redirige al catálogo de productos
