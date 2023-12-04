from django.shortcuts import render, redirect, get_object_or_404
from .models import Libro, Carrito, Perfil, Comentario
from .forms import LibroForm, UserRegistrationForm, LoginForm, EditarPerfilForm, ComentarioForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseServerError, HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

User = get_user_model()

def get_all_users():
    return User.objects.all()

def inicio(request):
    libros = Libro.objects.all()  # Asegúrate de reemplazar esto con tu propia lógica para obtener los libros
    return render(request, 'paginas/inicio.html', {'libros': libros})

def nosotros(request):
    return render(request, 'paginas/nosotros.html')

@login_required
def libros(request):
    if not request.user.is_staff:
        return redirect('inicio') 
    libros = Libro.objects.all()
    return render(request, 'libros/index.html', {'libros': libros})

@login_required
def crear(request):
    formulario = LibroForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('libros')
    return render(request, 'libros/crear.html', {'formulario': formulario})

@login_required
def editar(request, id):
    libro = Libro.objects.get(id=id)
    formulario = LibroForm(request.POST or None,
                           request.FILES or None, instance=libro)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('libros')
    return render(request, 'libros/editar.html', {'formulario': formulario})

@login_required
def eliminar(request, id):
    libros = Libro.objects.get(id=id)
    libros.delete()
    return redirect('libros')

def iniciarSesion(request):
    error = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('inicio')
            else:
                error = 'Nombre de usuario o contraseña incorrectos'
    else:
        form = LoginForm()
    return render(request, 'auth/iniciarSesion.html', {'form': form, 'error': error})

def registrarse(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Crea un nuevo perfil para el usuario
            perfil, created = Perfil.objects.get_or_create(usuario=user)
            if created:
                # Asigna la imagen de perfil predeterminada
                perfil.foto_de_perfil = 'perfiles/perfil.png'  # Asegúrate de reemplazar esto con la ruta a tu imagen de perfil predeterminada
                perfil.save()
            return redirect('iniciarSesion')
    else:
        form = UserRegistrationForm()
    return render(request, 'auth/registrarse.html', {'form': form})

@login_required
def cerrarSesion(request):
    logout(request)
    return redirect('inicio')

@login_required
def listado_productos(request):
    productos = Libro.objects.all()
    return render(request, 'productos/listado.html', {
        'libros': productos,
    })

@login_required
def ver_carrito(request):
    try:
        carrito = Carrito.objects.filter(usuario=request.user)
        total_carrito = sum(item.get_total_item_price() for item in carrito)
        cantidad_total = sum(item.cantidad for item in carrito)
        return render(request, 'productos/ver_carrito.html', {'carrito': carrito, 'total_carrito': total_carrito, 'cantidad_total': cantidad_total})
    except Exception as e:
        print(f"Error en la vista ver_carrito: {e}")
        return HttpResponseServerError("Ha ocurrido un error.")

@login_required
def agregar_producto(request, producto_id):
    producto = get_object_or_404(Libro, id=producto_id)
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user, libro=producto)
    if not creado:
        carrito.cantidad += 1
        carrito.save()
    return redirect('ver_carrito')

@login_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Libro, id=producto_id)
    carrito = get_object_or_404(Carrito, usuario=request.user, libro=producto)
    if carrito.cantidad > 1:
        carrito.cantidad -= 1
        carrito.save()
    else:
        carrito.delete()
    return redirect('ver_carrito')

@login_required
def perfil(request):
    if request.user.is_staff:  # asumiendo que 'is_staff' indica un administrador
        usuarios = User.objects.all()  # obtiene todos los usuarios
        return render(request, 'perfiles/perfil.html', {'usuarios': usuarios})
    else:
        return render(request, 'perfiles/perfil.html')  # muestra la página de perfil sin la lista de usuarios si el usuario no es un administrador

@login_required
def eliminar_usuario(request, pk):
    User = get_user_model()
    if request.user.is_staff:  # Comprueba si el usuario es un administrador
        try:
            user_to_delete = User.objects.get(pk=pk)
            user_to_delete.delete()
        except User.DoesNotExist:
            return HttpResponse('Usuario no encontrado', status=404)
        return redirect('perfil')
    else:
        return HttpResponse('No tienes permiso para realizar esta acción', status=403)

class CambiarContrasenaView(PasswordChangeView):
    template_name = 'perfiles/cambiar_contrasena.html' 
    success_url = reverse_lazy('perfil')

def editar_perfil(request):
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, request.FILES, instance=request.user.perfil)
        if form.is_valid():
            perfil = form.save(commit=False)
            if 'username' in form.changed_data:
                request.user.username = form.cleaned_data.get('username')
                request.user.save()
            if 'foto_de_perfil' in form.changed_data and form.cleaned_data.get('foto_de_perfil') is not None:
                perfil.foto_de_perfil = form.cleaned_data.get('foto_de_perfil')
            if 'descripcion' in form.changed_data:
                perfil.descripcion = form.cleaned_data.get('descripcion')
            perfil.save()
            return redirect('perfil')
    else:
        form = EditarPerfilForm(instance=request.user.perfil)
    return render(request, 'perfiles/editar_perfil.html', {'form': form})

from django.db.models import Avg

def detalle_libro(request, id):
    libro = get_object_or_404(Libro, id=id)
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.libro = libro
            comentario.usuario = request.user
            comentario.save()
            return redirect('detalle_libro', id=libro.id)
    else:
        form = ComentarioForm()
    comentarios = libro.comentarios.all()
    puntuacion_promedio = comentarios.aggregate(Avg('puntuacion'))['puntuacion__avg']
    if puntuacion_promedio is None:
        puntuacion_promedio = 0
    return render(request, 'libros/detalle_libro.html', {'libro': libro, 'form': form, 'comentarios': comentarios, 'puntuacion_promedio': puntuacion_promedio})

@login_required
def eliminar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    if request.user == comentario.usuario:
        comentario.delete()
    return redirect('detalle_libro', id=comentario.libro.id)