from django.contrib import admin
from .models import Marca, Producto

# Register your models here.
class ProductoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "precio", "descripcion", "uso", "nuevo", "marca", "popular", "tendencia", "fecha_fabricacion"]
    list_editable = ["precio", "descripcion", "uso", "marca", "popular", "tendencia"]
    search_fields = ["nombre", "uso"]
    list_filter = ["marca", "nuevo"]
    list_display_links = ["nombre"]  

admin.site.register(Marca)
admin.site.register(Producto, ProductoAdmin)