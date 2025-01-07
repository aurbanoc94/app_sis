import os
from django.core.management.base import BaseCommand
from inventario.models import Producto

class Command(BaseCommand):
    help = 'Carga imágenes desde la carpeta media/productos y las asigna a los productos'

    def handle(self, *args, **kwargs):
        ruta_media = os.path.join('media', 'productos')
        if not os.path.exists(ruta_media):
            self.stdout.write(self.style.ERROR(f'La carpeta {ruta_media} no existe.'))
            return

        for archivo in os.listdir(ruta_media):
            if archivo.endswith(('.png', '.jpg', '.jpeg')):
                nombre_producto = os.path.splitext(archivo)[0]
                ruta_imagen = os.path.join('productos', archivo)
                
                # Busca el producto o lo crea
                producto, creado = Producto.objects.get_or_create(Nombre=nombre_producto)
                producto.imagen = ruta_imagen
                producto.save()
                self.stdout.write(self.style.SUCCESS(f'Imagen {archivo} asignada al producto {nombre_producto}'))
