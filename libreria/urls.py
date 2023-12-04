from django.urls import path
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('nosotros', views.nosotros, name='nosotros'),
    path('libros', views.libros, name='libros'),
    path('libros/crear', views.crear, name='crear'),
    path('libros/editar', views.editar, name='editar'),
    path('eliminar/<int:id>', views.eliminar, name='eliminar'),
    path('editar/<int:id>', views.editar, name='editar'),
    path('iniciarSesion/', views.iniciarSesion, name='iniciarSesion'),
    path('registrarse/', views.registrarse, name='registrarse'),
    path('cerrarSesion/', views.cerrarSesion, name='cerrarSesion'),
    path('listadoProductos', views.listado_productos, name='listadoProductos'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('agregar_producto/<int:producto_id>/', views.agregar_producto, name='agregar_producto'),
    path('eliminar_producto/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('perfil/', views.perfil, name='perfil'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('cambiar_contrasena/', views.CambiarContrasenaView.as_view(), name='cambiar_contrasena'),
    path('eliminar_usuario/<int:pk>/', views.eliminar_usuario, name='eliminar_usuario'),

    path('libro/detalle/<int:id>', views.detalle_libro, name='detalle_libro'),
    path('eliminar_comentario/<int:comentario_id>/', views.eliminar_comentario, name='eliminar_comentario'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)