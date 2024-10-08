from django.shortcuts import render, redirect
from django.contrib import messages
from myapp.models import Producto

# Create your views here.

#vista de losproductos populares y en tendencia
def home(request):
    productos_tendencia = Producto.objects.filter(tendencia=True)
    productos_populares = Producto.objects.filter(popular=True)
    data = {
        'tendencia': productos_tendencia,
        'populares': productos_populares
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

from django.shortcuts import render

def chat_page(request):
    return render(request, 'chat.html')
