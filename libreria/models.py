from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView

class Libro(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=50, verbose_name="Titulo")
    imagen = models.ImageField(upload_to='imagenes/', verbose_name="Imagen", null=True)
    descripcion = models.TextField(verbose_name="Descripcion", null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio", default=0.00)

    def __str__(self):
        return f"{self.titulo} - {self.precio} - {self.descripcion}"

    def delete(self, using=None, keep_parents=False):
        self.imagen.storage.delete(self.imagen.name)
        super().delete()

class Carrito(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.cantidad} de {self.libro.titulo}'

    def get_total_item_price(self):
        return self.cantidad * self.libro.precio

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El campo Email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    is_admin = models.BooleanField(default=False)
    username = models.CharField(max_length=255, unique=True, default='valor_predeterminado')
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
    
class Perfil(models.Model):
    usuario = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    descripcion = models.TextField(blank=True)
    foto_de_perfil = models.ImageField(upload_to='perfiles/', default='perfiles/perfil.png')

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def crear_perfil_usuario(sender, instance, created, **kwargs):
        if created:
            Perfil.objects.create(usuario=instance)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def guardar_perfil_usuario(sender, instance, **kwargs):
        instance.perfil.save()

class PerfilUpdateView(UpdateView):
    model = Perfil
    fields = ['foto_de_perfil']
    template_name = 'perfil_editar.html'
    success_url = reverse_lazy('perfil')

    def get_object(self):
        return self.request.user.perfil

class Comentario(models.Model):
    texto = models.TextField()
    puntuacion = models.IntegerField()
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()