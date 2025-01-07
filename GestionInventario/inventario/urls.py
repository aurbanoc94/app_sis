from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('', views.home, name='home'),
    path('limpiar/', views.limpiar_carrito, name='limpiar_carrito'),
    path('carrito/', views.carrito, name='carrito'),
    path('productos/',views.ProductoListView.as_view(),name="producto-list"),
    path('seguir-comprando/', views.seguir_comprando, name='seguir_comprando'),
    path('agregar-al-carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('registro/',views.ProductoCreateView.as_view(),name="producto-create"),
    path('editar/<int:pk>/',views.ProductoUpdateView.as_view(),name="producto-edit"),
    path('eliminar/<int:pk>/',views.ProductoDeleteView.as_view(),name="producto-delete"),
    path('<int:pk>/',views.ProductoDetailView.as_view(),name="producto-detail"),
]
