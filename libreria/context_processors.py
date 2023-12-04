from .models import Carrito

def carrito(request):
    """
    Devuelve un diccionario con el carrito de compras del usuario y la cantidad total de artículos en el carrito.
    Si el usuario no está autenticado, devuelve un carrito vacío y una cantidad total de 0.

    Args:
        request (HttpRequest): La solicitud HTTP actual.

    Returns:
        dict: Un diccionario con las claves 'carrito' y 'cantidad_total'.
    """
    if request.user.is_authenticated:
        carrito = Carrito.objects.filter(usuario=request.user)
        cantidad_total = sum(item.cantidad for item in carrito)
    else:
        carrito = []
        cantidad_total = 0

    return {'carrito': carrito, 'cantidad_total': cantidad_total}