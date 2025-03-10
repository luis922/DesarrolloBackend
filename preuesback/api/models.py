from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,BaseUserManager
from django.utils import timezone
from django.db import models



class AtributosBase(models.Model):
    fueBorrado = models.BooleanField(default=False)
    creado = models.DateTimeField(default=timezone.now)
    modificado = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

class CustomUserManager(BaseUserManager):
    def create_user(self,name,email,password):
        if not name:
            raise ValueError('Debe ingresar un nombre de usuario')
        if not email:
            raise ValueError('Debe ingresar un email')
        if not password:
            raise ValueError('Debe ingresar una contraseña')
        user = self.model(
            email = self.normalize_email(email=email),
            username = name
        )
        user.set_password(raw_password=password)
        user.save(using=self.db)

        return user


    def create_superuser(self,username, email, password):
        if not email:
            raise ValueError('Debe ingresar un email')

        user = self.create_user(
            name = username,
            email = email,
            password = password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)

        return user

class Avatar(AtributosBase):
    nombre = models.CharField(max_length = 50, unique = True)
    dirAvatar = models.CharField(max_length = 100, unique = True)

    class Meta:
        db_table = "avatar"

class Usuario(AbstractBaseUser,AtributosBase,PermissionsMixin):
    username = models.CharField(max_length = 50, unique = True)
    email = models.CharField(max_length = 100, unique = True)
    password = models.CharField(max_length = 130)
    avatarActual = models.CharField(max_length = 50)
    monedas = models.IntegerField(default = 0)
    ultimaConexion = models.DateTimeField(auto_now_add = True)
    is_admin = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = False)

    objects = CustomUserManager()

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    class Meta:
        db_table = "usuario"

    # ManytoMany Relations
    avatars = models.ManyToManyField(Avatar)

    def __str__(self):
        return  self.email

class Contenido(AtributosBase):
    contenido = models.CharField(unique = True,max_length=50)

    class Meta:
        db_table = "contenido"

class Subcontenido(AtributosBase):
    subcontenido = models.CharField(unique=True,max_length=50)

    class Meta:
        db_table = "subcontenido"

    # OnetoMany Relations
    contenido = models.ForeignKey(Contenido, on_delete=models.CASCADE)

class Pregunta(AtributosBase):
    pregunta = models.TextField(max_length = 7000)
    videoLink = models.URLField()
    imgDir = models.CharField(max_length=255)

    class Meta:
        db_table = "pregunta"

    # OnetoMany Relations
    subcontenido = models.ForeignKey(Subcontenido, on_delete=models.CASCADE)

class Respuesta(AtributosBase):
    respuesta = models.CharField(max_length=200)
    esCorrecta = models.BooleanField()

    class Meta:
        db_table = "respuesta"

    # OnetoMany Relations
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)

class Ensayo(AtributosBase):
    nombre = models.CharField(max_length=50)
    esPersonalizado = models.BooleanField(default=False)
    numeroPreguntas = models.IntegerField()
    duracionSeleccionada = models.IntegerField()
    duracionOcupada = models.IntegerField()
    puntajeEnsayo = models.IntegerField(default=0)
    ensayoPadre = models.BigIntegerField(null=True)
    ultimoNombreRegistrado = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = "ensayo"

    # OnetoMany Relations
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    contenido = models.ForeignKey(Contenido, on_delete=models.CASCADE)
    # ManytoMany Relations
    subcontenidos = models.ManyToManyField(Subcontenido,related_name = "subcontneido_de_ensayo")
    preguntas = models.ManyToManyField(Pregunta, related_name = "preguntas_de_ensayo")

class RespuestaSeleccionada(AtributosBase):
    fueCorrecta = models.BooleanField()

    class Meta:
        db_table = "respuesta_seleccionada"

    # OnetoMany Relations
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    ensayo = models.ForeignKey(Ensayo, on_delete=models.CASCADE)
    respuesta = models.ForeignKey(Respuesta, on_delete=models.CASCADE)