from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)  # Asegurarse de que sean números flotantes
    except (TypeError, ValueError):
        return 0  # Si ocurre algún error, devolver 0

@register.filter   
def sum_items(carrito):
    total = 0
    for item in carrito.values():
        try:
            # Asegúrate de que 'precio' y 'cantidad' sean números (float o int)
            precio = float(item['precio'])  # Convertir a float
            cantidad = int(item['cantidad'])  # Convertir a int
            total += precio * cantidad
        except (ValueError, TypeError):
            # En caso de que haya un error de conversión, asignamos 0
            total += 0
    return total
