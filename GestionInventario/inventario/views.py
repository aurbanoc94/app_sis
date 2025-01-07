from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .carrito import Carrito
from django.views.generic import ListView,DeleteView,CreateView,UpdateView,DetailView
from .models import Producto


def home(request):
    # Inicializar total_productos en caso de que no exista en la sesión
    total_productos = request.session.get('total_productos', 0)
    return render(request, 'inventario/home.html', {'total_productos': total_productos})

def agregar_al_carrito(request, producto_id):
    if request.method == 'GET':
        cantidad = int(request.GET.get('cantidad', 1))
        try:
            producto = Producto.objects.get(ProductoID=producto_id)
            
            # Verificar que la cantidad no exceda el stock
            if cantidad > producto.Stock:
                return JsonResponse({'error': 'No hay suficiente stock disponible'}, status=400)
            
            # Inicializar el carrito si no existe
            carrito = request.session.get('carrito', {})
            
            # Si el producto ya está en el carrito, sumamos las cantidades
            if str(producto_id) in carrito:
                carrito[str(producto_id)]['cantidad'] += cantidad
                # Verificar que no exceda el stock disponible
                if carrito[str(producto_id)]['cantidad'] > producto.Stock:
                    return JsonResponse({'error': 'No hay suficiente stock disponible'}, status=400)
            else:
                carrito[str(producto_id)] = {
                    'producto_id': producto_id,
                    'nombre': producto.Nombre,
                    'precio': str(producto.Precio),  # Convertir a string para evitar problemas de serialización
                    'cantidad': cantidad,
                    'imagen': producto.imagen.url if producto.imagen else None,
                    'stock': producto.Stock,
                }
            
            # Guardar el carrito actualizado en la sesión
            request.session['carrito'] = carrito
            
            # Calcular y guardar el total de productos en la sesión
            total_productos = sum(item['cantidad'] for item in carrito.values())
            request.session['total_productos'] = total_productos
            request.session.modified = True  # Indica que la sesión ha sido modificada
            
            # Depuración
            print(f"Carrito actualizado: {request.session['carrito']}")
            print(f"Total de productos: {request.session['total_productos']}")
            
            return JsonResponse({
                'message': 'Producto agregado al carrito con éxito',
                'total_productos': total_productos,
            })
        except Producto.DoesNotExist:
            return JsonResponse({'error': 'Producto no encontrado'}, status=404)


        

def carrito(request):
    carrito_obj = Carrito(request) 
    carrito = carrito_obj.carrito  
    total_productos = sum(item['cantidad'] for item in carrito.values()) if carrito else 0
    return render(request, 'inventario/carrito.html', {'carrito': carrito, 'total_productos': total_productos})

def inicializar_carrito(request):
    if 'carrito' not in request.session:
        request.session['carrito'] = {}
    if 'total_productos' not in request.session:
        request.session['total_productos'] = 0

def limpiar_carrito(request):
    """Limpia el carrito en la sesión."""
    request.session['carrito'] = {}
    request.session.modified = True
    return redirect('inventario:carrito')  

def seguir_comprando(request):
    carrito = request.session.get('carrito', {})
    total_productos = sum(item['cantidad'] for item in carrito.values())
    request.session['total_productos'] = total_productos
    request.session.modified = True  
    return redirect('inventario:producto-list')


def producto_list(request):
    carrito = request.session.get('carrito', {})
    total_productos = request.session.get('total_productos', 0)
    productos = Producto.objects.all()
    return render(request, 'inventario/producto_list.html', {
        'object_list': productos,
        'carrito': carrito,
        'total_productos': total_productos,
    })





class ProductoListView(ListView):
    model = Producto
    template_name='inventario/producto_list.html'

class ProductoDetailView(DetailView):
    model = Producto
    template_name='equipos/equipo_detail.html'

class ProductoCreateView(CreateView):
    model = Producto
    fields = ['Nombre','Precio','Stock','Imagen']
    template_name='inventario/producto_form.html'
    success_url = reverse_lazy('producto-list')

class ProductoUpdateView(UpdateView):
    model = Producto
    fields = ['nombre','cantidad','imagen']
    template_name='equipos/equipo_form.html'
    success_url = reverse_lazy('equipo-list')

class ProductoDeleteView(DeleteView):
    model = Producto
    template_name='equipos/equipo_confirm_delete.html'
    success_url = reverse_lazy('equipo-list')









