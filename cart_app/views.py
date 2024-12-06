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
import json
from django.db import models

@login_required
def agregar_al_carrito(request, producto_id):
    """
    Vista para agregar un producto al carrito del usuario.
    """
    print("\n=== INICIO AGREGAR AL CARRITO ===")
    print(f"Usuario: {request.user.username}")
    print(f"Producto ID: {producto_id}")
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            # Verificar producto
            producto = get_object_or_404(Producto, id=producto_id)
            print(f"Producto encontrado: {producto.nombre}")

            # Verificar carrito
            carrito = Carrito.objects.filter(usuario=request.user).first()
            if not carrito:
                print("Creando nuevo carrito")
                carrito = Carrito.objects.create(usuario=request.user)
            else:
                print(f"Usando carrito existente ID: {carrito.id}")

            # Verificar item existente
            carrito_item = CarritoItem.objects.filter(carrito=carrito, producto=producto).first()
            if carrito_item:
                print(f"Actualizando item existente. Cantidad anterior: {carrito_item.cantidad}")
                carrito_item.cantidad += 1
                carrito_item.save()
                print(f"Nueva cantidad: {carrito_item.cantidad}")
            else:
                print("Creando nuevo item")
                carrito_item = CarritoItem.objects.create(
                    carrito=carrito,
                    producto=producto,
                    cantidad=1
                )

            # Verificar total de items
            num_items = CarritoItem.objects.filter(carrito=carrito).aggregate(
                total=models.Sum('cantidad'))['total'] or 0
            print(f"Total items en carrito: {num_items}")

            print("=== FIN AGREGAR AL CARRITO ===\n")
            return JsonResponse({
                'status': 'success',
                'message': 'Producto agregado al carrito',
                'num_items': num_items
            })
        except Exception as e:
            print(f"Error al agregar al carrito: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)

    return redirect('cart')

@login_required
def actualizar_cantidad(request, item_id):
    """
    Vista para actualizar la cantidad de un producto en el carrito
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get('action')
            
            item = get_object_or_404(CarritoItem, id=item_id, carrito__usuario=request.user)
            
            if action == 'increase':
                item.cantidad += 1
                item.save()
            elif action == 'decrease':
                if item.cantidad > 1:
                    item.cantidad -= 1
                    item.save()
                else:
                    item.delete()
            
            carrito = item.carrito
            num_items = CarritoItem.objects.filter(carrito=carrito).aggregate(
                total=models.Sum('cantidad'))['total'] or 0
            total = sum(item.get_total_item_price() for item in carrito.items.all())
            
            return JsonResponse({
                'success': True,
                'num_items': num_items,
                'total': total
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({
        'success': False,
        'error': 'Método no permitido'
    }, status=405)

@login_required
def eliminar_del_carrito(request, item_id):
    """
    Vista para eliminar un producto del carrito
    """
    if request.method == 'POST':
        try:
            item = get_object_or_404(CarritoItem, id=item_id, carrito__usuario=request.user)
            carrito = item.carrito
            item.delete()
            
            num_items = CarritoItem.objects.filter(carrito=carrito).aggregate(
                total=models.Sum('cantidad'))['total'] or 0
            
            return JsonResponse({
                'success': True,
                'message': 'Producto eliminado del carrito',
                'num_items': num_items
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({
        'success': False,
        'error': 'Método no permitido'
    }, status=405)

@login_required
def generar_factura(request):
    """
    Vista para generar una factura PDF y limpiar el carrito
    """
    if request.method != 'POST':
        return JsonResponse({
            'status': 'error',
            'message': 'Método no permitido'
        }, status=405)

    try:
        carrito = Carrito.objects.filter(usuario=request.user).first()
        if not carrito or not carrito.items.exists():
            return JsonResponse({
                'status': 'error',
                'message': 'El carrito está vacío'
            }, status=400)

        items = carrito.items.all()
        
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
        
        # Limpiar el carrito después de generar la factura
        carrito.items.all().delete()
        
        return response

    except Exception as e:
        print(f"Error al generar factura: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return JsonResponse({
            'status': 'error',
            'message': 'Error al generar la factura'
        }, status=500)

@login_required
def cart(request):
    """
    Vista para mostrar los productos en el carrito de compras del usuario.
    """
    try:
        print("\n=== INICIO VISTA CART ===")
        print(f"Usuario: {request.user.username}")
        
        carrito = Carrito.objects.filter(usuario=request.user).first()
        if not carrito:
            print("No existe carrito, creando uno nuevo")
            carrito = Carrito.objects.create(usuario=request.user)
        
        cart_items = CarritoItem.objects.filter(carrito=carrito)
        print(f"Número de items encontrados: {cart_items.count()}")
        
        for item in cart_items:
            print(f"Item: {item.producto.nombre} - Cantidad: {item.cantidad}")
        
        num_items = cart_items.aggregate(total=models.Sum('cantidad'))['total'] or 0
        total = sum(item.get_total_item_price() for item in cart_items)
        
        print(f"Total items: {num_items}")
        print(f"Total precio: ${total}")
        print("=== FIN VISTA CART ===\n")

        data = {
            'cart_items': cart_items,
            'total': total,
            'subtotal': total,
            'num_items': num_items
        }
        return render(request, 'cart.html', data)
    except Exception as e:
        print(f"Error en vista cart: {str(e)}")
        import traceback
        print(traceback.format_exc())
        messages.error(request, 'Error al cargar el carrito')
        return redirect('catalogue')

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
