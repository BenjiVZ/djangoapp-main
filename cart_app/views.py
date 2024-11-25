# cart/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Carrito, CarritoItem
from myapp.models import Producto  # Importa el modelo Producto desde la app myapp
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from datetime import datetime
from django.urls import reverse

@login_required
def agregar_al_carrito(request, producto_id):
    """
    Vista para agregar un producto al carrito del usuario.
    """
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        producto = get_object_or_404(Producto, id=producto_id)
        carrito, created = Carrito.objects.get_or_create(usuario=request.user)
        carrito_item, created = CarritoItem.objects.get_or_create(carrito=carrito, producto=producto)
        
        if not created:
            carrito_item.cantidad += 1
            carrito_item.save()
        
        # Calcular el número total de items en el carrito
        num_items = sum(item.cantidad for item in carrito.items.all())
        
        return JsonResponse({
            'status': 'success',
            'num_items': num_items
        })
    
    return redirect('cart')

@login_required
def actualizar_cantidad(request, item_id):
    """
    Vista para actualizar la cantidad de un producto en el carrito
    """
    item = get_object_or_404(CarritoItem, id=item_id, carrito__usuario=request.user)
    action = request.POST.get('action')
    
    if action == 'increase':
        item.cantidad += 1
    elif action == 'decrease':
        if item.cantidad > 1:
            item.cantidad -= 1
        else:
            item.delete()
            return redirect('cart')
    
    item.save()
    return redirect('cart')

@login_required
def eliminar_del_carrito(request, item_id):
    """
    Vista para eliminar un producto del carrito
    """
    item = get_object_or_404(CarritoItem, id=item_id, carrito__usuario=request.user)
    item.delete()
    messages.success(request, 'Producto eliminado del carrito.')
    return redirect('cart')

@login_required
def generar_factura(request):
    """
    Vista para generar una factura PDF y limpiar el carrito
    """
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    items = carrito.items.all()
    
    if not items:
        messages.warning(request, 'El carrito está vacío.')
        return redirect('cart')

    # Crear el PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Configuración inicial del PDF
    p.setFont('Helvetica-Bold', 16)
    p.drawString(50, 750, "Factura de Compra")
    
    # Información del cliente y fecha
    p.setFont('Helvetica', 12)
    p.drawString(50, 720, f"Cliente: {request.user.get_full_name() or request.user.username}")
    p.drawString(50, 700, f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    # Encabezados de la tabla
    y = 650
    p.drawString(50, y, "Producto")
    p.drawString(250, y, "Cantidad")
    p.drawString(350, y, "Precio Unit.")
    p.drawString(450, y, "Total")
    
    # Línea separadora
    y -= 20
    p.line(50, y, 550, y)
    
    # Contenido de la factura
    total = 0
    y -= 30
    
    for item in items:
        if y < 100:  # Nueva página si no hay espacio
            p.showPage()
            y = 750
        
        p.drawString(50, y, item.producto.nombre[:30])
        p.drawString(250, y, str(item.cantidad))
        p.drawString(350, y, f"${item.producto.precio}")
        subtotal = item.get_total_item_price()
        p.drawString(450, y, f"${subtotal}")
        
        total += subtotal
        y -= 20
    
    # Total final
    p.line(50, y, 550, y)
    y -= 20
    p.setFont('Helvetica-Bold', 12)
    p.drawString(350, y, "Total Final:")
    p.drawString(450, y, f"${total}")
    
    # Finalizar el PDF
    p.showPage()
    p.save()
    
    # Preparar la respuesta
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="factura.pdf"'
    
    # Limpiar el carrito
    carrito.items.all().delete()
    
    # Agregar mensaje de éxito
    messages.success(request, 'Compra realizada con éxito. La factura se está descargando.')
    
    return response

@login_required
def cart(request):
    """
    Vista para mostrar los productos en el carrito de compras del usuario.
    """
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    items = carrito.items.all()
    num_items = sum(item.cantidad for item in items)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'num_items': num_items})
    
    total = sum(item.get_total_item_price() for item in items)
    
    data = {
        'items': items,
        'total': total,
        'MEDIA_URL': settings.MEDIA_URL,
        'num_items': num_items
    }
    return render(request, 'cart.html', data)

@login_required
def procesar_pago(request):
    if request.method == 'POST':
        # Aquí podrías agregar la lógica real de procesamiento de pago
        # Por ahora solo simulamos que el pago fue exitoso
        messages.success(request, 'Pago procesado exitosamente')
        return JsonResponse({'status': 'success'})
    
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    items = carrito.items.all()
    total = sum(item.get_total_item_price() for item in items)
    
    data = {
        'items': items,
        'total': total,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'payment.html', data)
