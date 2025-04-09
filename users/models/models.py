from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UsuarioManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError("El nombre de usuario es obligatorio")
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class Usuario(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    objects = UsuarioManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

def visita_foto_path(instance, filename):
    """Función mejorada para el almacenamiento de imágenes"""
    ext = filename.split('.')[-1].lower()
    timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
    
    # Determina si es anverso o reverso basado en el nombre del campo
    if instance.foto_anverso and instance.foto_anverso.name in filename:
        tipo = 'anverso'
    elif instance.foto_reverso and instance.foto_reverso.name in filename:
        tipo = 'reverso'
    else:
        tipo = 'anverso' if 'anverso' in filename.lower() else 'reverso'
    
    # Crea directorios separados para anverso/reverso
    return f'visitas/{instance.cedula}/{tipo}/{tipo}_{timestamp}.{ext}'

class Visita(models.Model):
    nombre_completo = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, unique=True)
    foto_anverso = models.ImageField(
        upload_to=visita_foto_path,
        blank=True,
        null=True,
        verbose_name="Foto Anverso de Cédula"
    )
    foto_reverso = models.ImageField(
        upload_to=visita_foto_path,
        blank=True,
        null=True,
        verbose_name="Foto Reverso de Cédula"
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.nombre_completo} ({self.cedula})"

    def save(self, *args, **kwargs):
        # Actualiza el campo updated_at
        self.updated_at = timezone.now()
        
        # Elimina fotos antiguas si se actualizan
        if self.pk:
            old_visita = Visita.objects.get(pk=self.pk)
            if old_visita.foto_anverso and (not self.foto_anverso or old_visita.foto_anverso != self.foto_anverso):
                old_visita.foto_anverso.delete(save=False)
            if old_visita.foto_reverso and (not self.foto_reverso or old_visita.foto_reverso != self.foto_reverso):
                old_visita.foto_reverso.delete(save=False)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Elimina las fotos al borrar el registro
        self.foto_anverso.delete(save=False) if self.foto_anverso else None
        self.foto_reverso.delete(save=False) if self.foto_reverso else None
        super().delete(*args, **kwargs)

class Ingreso(models.Model):
    visita = models.ForeignKey(Visita, on_delete=models.CASCADE)
    fecha_entrada = models.DateTimeField(default=timezone.now)
    hora_entrada = models.TimeField(auto_now_add=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Ingreso de {self.visita.nombre_completo} - {self.fecha_entrada.date()}"