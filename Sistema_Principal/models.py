# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings
from django.contrib.auth.models import Group,Permission

# Create your models here.
class Empresa(models.Model):
    nombre = models.CharField(max_length=100,help_text=("Nombre de la Empresa"))
    nit = models.CharField(max_length=10,null=False,unique=True)
    ciudad = models.CharField(max_length=50,null=False)
    direccion = models.CharField(max_length=200,help_text=("Direccion de la Empresa"))
    telefono = models.CharField(max_length=10, help_text=("Telefono de la Empresa"))
    imagen = models.ImageField(upload_to="logos/")
    correo = models.EmailField(max_length=75)
    cuotas_no_aplic = models.IntegerField(max_length=1,null=False)
    def __unicode__(self):
        return self.nombre
    
class UsuarioManager(BaseUserManager):
    def create_user(self,username,email,nombre=None,apellidos=None,password=None):
        if not username:
            raise ValueError('El usuario debe tener un nombre')
        user = self.model(
            username=username,
            email=UsuarioManager.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self.db)
        user.user_permissions = []
        user.user_permissions.add('Sistema_Principal.add_cotizacion')
        user.user_permissions.add('Sistema_Principal.add_cliente')
        user.save()
        return user
    def create_superuser(self, email, username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email=email,
            password=password,
            username=username,
        )
        user.is_superuser = True
        user.es_admin = True
        sicobotero = Empresa.objects.create(nombre="SiCoBotero",nit="00000-0",ciudad="Cartagena",cuotas_no_aplic = 0)
        sicobotero.save()
        user.empresa.add(sicobotero)
        super_admins = Group.objects.create(name = "super_admins")
        super_admins.save()
        user.groups.add(super_admins,)
        user.save(using=self._db)
        return user
    def get_by_natural_key(self,username):
        return self.get(username=username)
    
class Usuario(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=40, unique=True, db_index=True, verbose_name='Usuario')
    email = models.EmailField(max_length=254, unique=True)
    telefono = models.CharField(max_length=25)
    nombre = models.CharField(max_length=20,help_text=("Nombre del vendedor"))
    apellidos = models.CharField(max_length=40,help_text=("Apellidos del vendedor"))
    empresa = models.ManyToManyField(Empresa,blank=True,null=True)
    esta_activo = models.BooleanField(default=True)
    es_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objets = UsuarioManager()
    class Meta:
        pass
    def get_full_name(self):
        # The user is identified by their email address
        return self.nombre+" "+self.apellidos

    def get_short_name(self):
        # The user is identified by their email address
        return self.nombre

    def __unicode__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Administracion de permisos"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Tiene permiso para entrar a la aplicacion?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Es administrador?"
        # Simplest possible answer: All admins are staff
        return self.es_admin
    def is_active(self):
        return self.esta_activo

class Cliente(models.Model):
    cedula = models.CharField(max_length=10,help_text=("Cedula del Cliente"),unique=True)
    nombre = models.CharField(max_length=20,help_text=("Nombre del Cliente"),null=False)
    apellidos = models.CharField(max_length=40,help_text=("Apellidos del Cliente"),null=False)
    direccion = models.CharField(max_length=200,help_text=("Direccion de Cliente"),null=False)
    telefono = models.CharField(max_length=10, help_text=("Telefono del Cliente"),null=False)
    email = models.CharField(max_length=60, help_text=("Correo del cliente"),null=False)
    not_por_email = models.BooleanField()
    empresa = models.ForeignKey(Empresa)
    def __unicode__(self):
        return self.nombre+" "+self.apellidos+" : "+self.cedula

class Moto(models.Model):
    nombre_fabr = models.CharField(max_length=15,help_text=("Fabricante de la moto"),null=False)
    referencia = models.CharField(max_length=30,null=False,help_text=("Referencia de la moto"))
    modelo = models.CharField(max_length=30,help_text=("Modelo de la moto"),null=False)
    precio_publico = models.IntegerField(max_length=14,null=False)
    cuota_minima = models.IntegerField(max_length=15,null=False)
    empresa = models.ForeignKey(Empresa,null=False)
    def __unicode__(self):
        return self.nombre_fabr+" "+self.referencia+" "+self.modelo
    def __srt__(self):
        return self.nombre_fabr+" "+self.referencia+" "+self.modelo 

class Kit(models.Model):
    soat = models.IntegerField(max_length=10, null=False)
    casco = models.IntegerField(max_length=10, null=False)
    chaleco = models.IntegerField(max_length=10, null=False)
    transporte = models.IntegerField(max_length=10, null=False)
    empresa = models.ForeignKey(Empresa,null=False)
    moto_asociada = models.ForeignKey(Moto,null=False,unique=True)
    def __unicode__(self):
        return self.moto_asociada.nombre_fabr+" "+self.moto_asociada.referencia+" "+self.moto_asociada.modelo

class Matricula(models.Model):
    nombre_ciudad = models.CharField(max_length=20,null=False)
    precio = models.IntegerField(max_length=20,null=False)
    empresa = models.ForeignKey(Empresa,null=False)
    kit_asociado = models.ForeignKey(Kit,null=False)
    def __unicode__(self):
        return self.nombre_ciudad

class Inventario_motos(models.Model):
    moto = models.ForeignKey(Moto,null=False)
    en_venta = models.BooleanField(null=False)
    empresa = models.ForeignKey('Empresa',null=False)
    
    def __unicode__(self):
        #return u'{0} {1}'.format(self.moto, self.en_venta)
        return self.moto.nombre_fabr+" "+self.moto.referencia
    class Meta:
        verbose_name = verbose_name_plural = "Inventario de Motos"

    
class T_financiacion(models.Model):
    num_meses = models.IntegerField(max_length=2,null=False,unique=True)
    valor_por = models.FloatField(null=False)
    empresa = models.ForeignKey(Empresa,null=False)
    def __unicode__(self):
        return str(self.num_meses)
    class Meta:
        verbose_name="Registro de Financiacion"
        verbose_name_plural = "Registros de Financiacion"


class Cotizacion(models.Model):
    fecha_cot = models.DateField(auto_now=True)
    moto = models.ForeignKey(Moto)
    vendedor = models.ForeignKey(settings.AUTH_USER_MODEL)
    cliente = models.ForeignKey(Cliente)
    n_cuotas = models.IntegerField()
    cuota_inicial = models.IntegerField()