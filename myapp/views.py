from django.shortcuts import render, redirect
from django.contrib import messages
from myapp.models import Producto
from django.conf import settings
from django.db.models import Q
from fuzzywuzzy import fuzz
from django.db.models import Q, Value, FloatField
from django.db.models.functions import Greatest
import unicodedata
from django.http import JsonResponse

# Create your views here.

#vista de losproductos populares y en tendencia
def home(request):
    productos_tendencia = Producto.objects.filter(tendencia=True)
    productos_populares = Producto.objects.filter(popular=True)
    data = {
        'tendencia': productos_tendencia,
        'populares': productos_populares,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'home.html', data)



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

from .product_filter_bot import ProductFilterBot

def filter_products(request):
    category = request.GET.get('category', '')
    products = []
    if category:
        bot = ProductFilterBot()
        try:
            products = bot.filter_products(category)
        except Exception as e:
            # Log the error here if needed
            products = []
    
    context = {
        'category': category,
        'products': products
    }
    


import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from django.shortcuts import render
from django.conf import settings
from .models import Producto


@csrf_exempt  # Esto es necesario para que Django permita solicitudes POST sin un token CSRF.
def chat_with_rasa(request):
    if request.method == 'POST':
        # Obtener el mensaje del usuario desde el frontend
        data = json.loads(request.body)
        user_message = data.get('message')

        # Enviar el mensaje al API de Rasa
        response = requests.post(
            'http://localhost:5005/webhooks/rest/webhook',  # URL del API de Rasa
            json={"sender": "user", "message": user_message}
        )

        # Obtener la respuesta del bot
        bot_response = response.json()

        # Devolver la respuesta del bot al frontend
        return JsonResponse(bot_response, safe=False)

    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def intelligent_filter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '').lower()
        
        productos = Producto.objects.all()
        resultados = []
        
        # Función auxiliar para normalizar texto (quitar acentos)
        def normalize_text(text):
            return ''.join(c for c in unicodedata.normalize('NFD', text)
                if unicodedata.category(c) != 'Mn').lower()
        
        # Si no hay palabras clave específicas, hacer búsqueda difusa
        if not any(keyword in user_message for keyword in ['marca', 'descripción', 'precio', 'económica', 'barata']):
            user_message_norm = normalize_text(user_message)
            
            # Buscar en todos los productos
            for producto in productos:
                nombre_norm = normalize_text(producto.nombre)
                desc_norm = normalize_text(producto.descripcion)
                marca_norm = normalize_text(producto.marca.nombre)
                
                # Calcular similitud con diferentes campos
                nombre_ratio = fuzz.partial_ratio(user_message_norm, nombre_norm)
                desc_ratio = fuzz.partial_ratio(user_message_norm, desc_norm)
                marca_ratio = fuzz.partial_ratio(user_message_norm, marca_norm)
                
                # Si alguna similitud es mayor al 75%, incluir el producto
                if max(nombre_ratio, desc_ratio, marca_ratio) > 75:
                    resultados.append({
                        'producto': producto,
                        'relevancia': max(nombre_ratio, desc_ratio, marca_ratio)
                    })
            
            # Ordenar por relevancia
            resultados = sorted(resultados, key=lambda x: x['relevancia'], reverse=True)
            productos = [r['producto'] for r in resultados]
        
        else:
            # Mantener la lógica existente para búsquedas específicas
            if 'marca' in user_message:
                productos = productos.filter(marca__nombre__icontains=user_message.split('marca')[1].strip())
            elif 'descripción' in user_message:
                productos = productos.filter(descripcion__icontains=user_message.split('descripción')[1].strip())
            elif 'precio' in user_message:
                try:
                    precio = float(user_message.split('precio')[1].strip())
                    productos = productos.filter(precio__lte=precio)
                except ValueError:
                    pass
            elif 'económica' in user_message or 'barata' in user_message:
                productos = productos.order_by('precio')[:5]

        if productos:
            productos_data = [{
                'nombre': p.nombre,
                'precio': p.precio,
                'imagen': p.imagen.url if p.imagen else '/static/placeholder.png',
                'uso': p.uso or 'Uso no especificado'
            } for p in productos[:10]]  # Limitamos a 10 resultados
            
            response = {
                "text": f"Encontré estos productos relacionados con '{user_message}':",
                "productos": productos_data
            }
        else:
            response = {
                "text": f"Lo siento, no encontré productos que coincidan con '{user_message}'.",
                "productos": []
            }

        return JsonResponse(response)

    return JsonResponse({"error": "Invalid request"}, status=400)

def chat_page(request):
    data = {
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'chat.html', data)

def get_product_use(request):
    product_name = request.GET.get('name', '')
    try:
        producto = Producto.objects.get(nombre__iexact=product_name)
        return JsonResponse({'uso': producto.uso or 'Uso no especificado'})
    except Producto.DoesNotExist:
        return JsonResponse({'uso': 'Uso no especificado'})
