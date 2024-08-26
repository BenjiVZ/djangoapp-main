from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from user_app.models import Profile

# Create your views here.
def log(request):
    return render(request, 'login.html')

def reg(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Aquí no es necesario crear el perfil manualmente
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

""" class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')  # Redirige a la página 'home' después del logout

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
"""