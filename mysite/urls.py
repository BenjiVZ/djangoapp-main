"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from myapp.views import (
    home, 
    filter_products, 
    chat_with_rasa, 
    chat_page, 
    intelligent_filter,
    get_product_use  # Agregar esta importación
)
from user_app.views import log, reg
from django.contrib.auth.views import LoginView, LogoutView
from catalog_app.views import catalog, catalogue
from cart_app.views import (
    cart, 
    agregar_al_carrito, 
    actualizar_cantidad,
    eliminar_del_carrito,
    procesar_pago,
    generar_factura
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home, name='home'),
    
    # URLs del chat y filtrado
    path('chat_page/', chat_with_rasa, name='chat_with_rasa'),
    path('chat/', chat_page, name='chat_page'),
    path('filter/', filter_products, name='filter_products'),
    path('intelligent_filter/', intelligent_filter, name='intelligent_filter'),
    path('get_product_use/', get_product_use, name='get_product_use'),
    
    # URLs de autenticación
    path('register/', reg, name='regs'),
    path('login/', LoginView.as_view(template_name='login.html'), name='logs'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # URLs del catálogo
    path('catalog/', catalog, name='catalog'),
    path('catalogue/', catalogue, name='catalogue'),
    
    # URLs del carrito
    path('cart/', cart, name='cart'),
    path('cart/agregar/<int:producto_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('cart/actualizar/<int:item_id>/', actualizar_cantidad, name='actualizar_cantidad'),
    path('cart/eliminar/<int:item_id>/', eliminar_del_carrito, name='eliminar_del_carrito'),
    path('cart/pago/', procesar_pago, name='procesar_pago'),
    path('cart/factura/', generar_factura, name='generar_factura'),
]
#path('logout/', CustomLogoutView.as_view(), name='logout'),
#path('logout/', auth_views.LogoutView.as_view(), name='logout'),
#path('logout/', LogoutView.as_view(template_name='logout.html'), name='logst'),

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)