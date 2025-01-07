from .models import Producto
from django.shortcuts import get_object_or_404

class Carrito:
    def __init__(self, request):
        self.session = request.session
        carrito = self.session.get('carrito', {})
        self.carrito = carrito

    def agregar(self, producto_id, cantidad):
        producto = get_object_or_404(Producto, ProductoID=producto_id)
        if str(producto_id) not in self.carrito:
            self.carrito[str(producto_id)] = {
                'producto_id': producto.ProductoID,
                'nombre': producto.Nombre,
                'precio': str(producto.Precio),
                'imagen': producto.imagen.url if producto.imagen else '',
                'cantidad': cantidad,
                'stock': producto.Stock,
            }
        else:
            self.carrito[str(producto_id)]['cantidad'] += cantidad
        self.guardar_carrito()

def guardar_carrito(self):
    self.session['carrito'] = self.carrito
    # Actualizar el total de productos en la sesión
    self.session['total_productos'] = sum(item['cantidad'] for item in self.carrito.values())
    self.session.modified = True