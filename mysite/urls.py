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
from myapp.views import home
from user_app.views import log, reg
from django.contrib.auth.views import LoginView, LogoutView
from catalog_app.views import catalog, catalogue
from cart_app.views import cart, agregar_al_carrito, generar_factura

from django.contrib.auth.views import LogoutView
""" from django.contrib.auth import views as auth_views
from user_app.views import CustomLogoutView """

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home, name='home'),
    path('register/', reg, name='regs'),
    path('login/', LoginView.as_view(template_name='login.html'), name='logs'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('catalog/', catalog, name='catalog'),
    path('catalogue/', catalogue, name='catalogue'),  # Vista para el catálogo
    path('cart/', cart, name='cart'),  # Vista para ver el carrito
    path('agregar/<int:producto_id>/', agregar_al_carrito, name='agregar_al_carrito'),  # Vista para agregar al carrito
    path('factura/', generar_factura, name='generar_factura'),  # Vista para generar factura
]
#path('logout/', CustomLogoutView.as_view(), name='logout'),
#path('logout/', auth_views.LogoutView.as_view(), name='logout'),
#path('logout/', LogoutView.as_view(template_name='logout.html'), name='logst'),

from django.conf import settings
from django.conf.urls.static import static


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)