# -*- encoding: utf-8 -*-
'''
Created on May 3, 2013

@author: minrock
'''


from django import forms
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from Sistema_Principal.models import *
from django.contrib.sites.models import Site
from Sistema_Principal.forms import Add_t_financiacion_form
from django.forms import ModelForm
from datetime import datetime

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Contraseña",widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar Contraseña",widget = forms.PasswordInput)
    
    class Meta:
        model = Usuario
        fields = ('username','email','nombre','apellidos')
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no son iguales")
        return password2
    
    def save(self,commit=True):
        user = super(UserCreationForm,self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password= ReadOnlyPasswordHashField()
    class Meta:
        model = Usuario
    def clean_password(self):
        return self.initial["password"]

fieldsets_admin = (
                  ("Info. General",{'fields':('username','email','password','empresa')}),
                  ("Info. Personal",{'fields':('nombre','apellidos','ciudad')}),
                  ("¿Administrador?",{'fields':('es_admin','is_superuser')}),
                  ("Ultima entrada",{'fields':('last_login',)}),
                  )
fieldsets_no_admin = (
                  ("Info. General",{'fields':('username','email','password',)}),
                  ("Info. Personal",{'fields':('nombre','apellidos','ciudad')}),
                  ("¿Administrador?",{'fields':('es_admin',)}),
                  ("Ultima entrada",{'fields':('last_login',)}),
                  )

class UsuarioAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username','email','nombre','apellidos','es_admin',)
    list_filter = ('es_admin',)
    fieldsets = (
                  ("Info. General",{'fields':('username','email','password',)}),
                  ("Info. Personal",{'fields':('nombre','apellidos','ciudad')}),
                  ("¿Administrador?",{'fields':('es_admin',)}),
                  ("Ultima entrada",{'fields':('last_login',)}),
                  )
    search_fields=('username','email','nombre','apellidos')
    ordering = ('username',)

    def get_fieldsets(self, request, obj=None):

        if request.user.is_superuser:
            self.fieldsets = fieldsets_admin
            form = self.get_form(request, obj)
        else:
            self.fieldsets = fieldsets_no_admin
            form = self.get_form(request, obj)


        fields = form.base_fields.keys() + list(self.get_readonly_fields(request, obj))

        return [(None, {'fields': fields})]

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            obj.save()
        else:
            obj.save()
            obj.empresa.add(Empresa.objects.get(pk = request.session.get('user_enterprise')))
            obj.save()
    #def formfield_for_manytomany(self, db_field, request=None, **kwargs):
    #    if db_field == "empresa":
    #        kwargs['queryset'] = Empresa.objects.filter(pk = request.session.get('user_enterprise'))

class InventarioMotosAdmin(admin.ModelAdmin):
    list_display = ('moto', 'en_venta')
    list_filter = ('en_venta',)
    exclude = ['empresa']
    def queryset(self, request):
        empresas = request.session.get('enterprise')
        return super(InventarioMotosAdmin, self).queryset(request).filter(empresa=empresas)
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        empresas = request.session['enterprise']
        if db_field.name == 'empresa':
            kwargs['queryset'] = empresas
        elif db_field.name == 'moto':
            kwargs['queryset'] = Moto.objects.filter(empresa=empresas)
        return super(InventarioMotosAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs) 
    def save_model(self, request, obj, form, change):
        obj.empresa = Empresa.objects.get(pk = request.session.get('user_enterprise'))
        obj.save()

class KitAdmin(admin.ModelAdmin):
    exclude = ['empresa']
    def save_model(self, request, obj, form, change):
        obj.empresa = Empresa.objects.get(pk = request.session.get('user_enterprise'))
        obj.save()
    def queryset(self, request):
        empresa = Empresa.objects.get(pk = request.session.get('user_enterprise'))
        return super(KitAdmin,self).queryset(request).filter(empresa=empresa)
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        empresas = Empresa.objects.get(pk = request.session.get('user_enterprise'))
        if db_field.name == 'moto_asociada':
            kwargs['queryset'] = Moto.objects.filter(empresa=empresas)
        return super(KitAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

class KitInLine(admin.TabularInline):
    model = Kit
    extra = 1
    max_num = 1
    exclude = ['empresa']


class MotoAdmin(admin.ModelAdmin):
    list_display = ('nombre_fabr','referencia','modelo','precio_publico')
    list_filter = ('nombre_fabr',)
    actions = ['really_delete_selected']
    exclude = ['empresa']
    inlines = [KitInLine,]
    def save_model(self, request, obj, form, change):
        obj.empresa = Empresa.objects.get(pk = request.session.get('user_enterprise'))
        obj.save()
        invt = Inventario_motos.objects.filter(empresa=obj.empresa,moto=obj)
        if(invt.count() == 0):
            inv = Inventario_motos()
            inv.en_venta=True
            inv.moto = obj
            inv.empresa = request.session.get('enterprise')
            inv.save()
    def queryset(self, request):
        empresa = Empresa.objects.get(pk = request.session.get('user_enterprise'))
        return super(MotoAdmin,self).queryset(request).filter(empresa=empresa)
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.empresa = request.session['enterprise']
            instance.save()
        formset.save()
    def get_actions(self, request):
        actions = super(MotoAdmin,self).get_actions(request)
        del actions['delete_selected']
        return actions
    def really_delete_selected(self,request,queryset):
        for obj in queryset:
            moto = Inventario_motos.objects.get(moto = obj)
            moto.en_venta = False
            moto.save()
        self.message_user(request,"%s Motos fueron deshabilitadas del inventario"%queryset.count())
    really_delete_selected.short_description = "Deshabilitar Motos del inventario"

class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre","apellidos","cedula","telefono","direccion","email")
    search_fields = ("nombre","cedula","email")
    exclude = ['empresa']
    actions = ['delete_cliente_unused']
    def save_model(self, request, obj, form, change):
        obj.empresa = Empresa.objects.get(pk = request.session.get('user_enterprise'))
        obj.save()
    def queryset(self, request):
        empresa = Empresa.objects.get(pk = request.session.get('user_enterprise'))
        return super(ClienteAdmin,self).queryset(request).filter(empresa=empresa)
    def get_actions(self, request):
        actions = super(ClienteAdmin,self).get_actions(request)
        del actions['delete_selected']
        return actions
    def delete_cliente_unused(self,request,queryset):
        i = 0
        j = 0
        for obj in queryset:
            c = Cotizacion.objects.filter(cliente=obj)
            if c.count() == 0:
                obj.delete()
                j= j+1
            else:
                i = i+1
        if i==1:
            self.message_user(request,"% s Cliente(s) afectado(s), %s registro no fue borrado por tener movimiento"%(str(j),str(i)))
        else:
            self.message_user(request,"%s Cliente(s) afectado(s), %s registros no fue borrados por tener movimiento"%(str(j),str(i)))
    delete_cliente_unused.short_description = "Eliminar Usuarios sin Movimiento"

class MatriculaAdmin(admin.ModelAdmin):
    list_display = ("nombre_ciudad",)
    exclude = ['empresa']
    def save_model(self, request, obj, form, change):
        obj.empresa = Empresa.objects.get(pk = request.session.get('user_enterprise'))
        obj.save()
    def formfield_for_choice_field(self, db_field, request=None, **kwargs):
        empresa = Empresa.objects.get(pk = request.session['user_enterprise'])
        if db_field.name == 'empresa':
            kwargs['queryset'] = Matricula.objects.filter(empresa = empresa)
        return super(MatriculaAdmin,self).formfield_for_foreignkey(db_field,request,**kwargs)
    def queryset(self, request):
        empresas = request.session.get('enterprise')
        return super(MatriculaAdmin, self).queryset(request).filter(empresa=empresas)

class T_financiacionAdmin(admin.ModelAdmin):
    form = Add_t_financiacion_form
    list_display = ("num_meses",)

    def save_model(self, request, obj, form, change):
        obj.empresa = Empresa.objects.get(pk = request.session.get('user_enterprise'))
        obj.save()
    def get_form(self, request, obj=None, **kwargs):
        AdminForm = super(T_financiacionAdmin,self).get_form(request,obj,**kwargs)
        AdminForm.request = request
        return AdminForm
    def queryset(self, request):
        empresas = request.session.get('enterprise')
        return super(T_financiacionAdmin, self).queryset(request).filter(empresa=empresas)

class EmpresaAdmin(admin.ModelAdmin):
    list_display = ("nombre","nit","ciudad","correo")
    def has_add_permission(self, request):
        perms = request.user.es_admin and request.user.is_superuser
        return perms
    def has_change_permission(self, request, obj=None):
        perms = request.user.es_admin and request.user.is_superuser
        return perms
    def has_delete_permission(self, request, obj=None):
        perms = request.user.es_admin and request.user.is_superuser
        return perms

class CotizacionAdmin(admin.ModelAdmin):
    list_display = ("fecha_cot","cliente")
    #readonly_fields = ('fecha_cot','moto','vendedor','no_aplicables','cliente','n_cuotas','cuota_inicial',
    #'n_no_aplicables','medio')
    exclude = ['empresa','matricula_asociada']
    def save_model(self, request, obj, form, change):
        obj.empresa = Empresa.objects.get(pk = request.session.get('user_enterprise'))
        obj.fecha_cot = datetime.today()
        obj.matricula_asociada = Matricula.objects.filter(empresa = obj.empresa).get(nombre_ciudad=request.user.ciudad)
        obj.save()
    def queryset(self, request):
        empresas = request.session.get('enterprise')
        return super(CotizacionAdmin, self).queryset(request).filter(empresa=empresas)

class MediosAdmin(admin.ModelAdmin):
    exclude = ['empresa']
    list_display = ['identificador','medio']
    def save_model(self, request, obj, form, change):
        obj.empresa = Empresa.objects.get(id=request.session.get('user_enterprise'))
        obj.save()
    def queryset(self, request):
        empresas = request.session.get('enterprise')
        return super(MediosAdmin, self).queryset(request).filter(empresa=empresas)

class RegistroRequisito(admin.TabularInline):
    model = registroRequisito
    extra = 1

class TablaRequisitoAdmin(admin.ModelAdmin):
    inlines = [RegistroRequisito]
    exclude = ['empresa']
    def save_model(self, request, obj, form, change):
        obj.empresa = request.session.get('enterprise')
        obj.save()


admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Empresa,EmpresaAdmin)
admin.site.register(Cliente,ClienteAdmin)
admin.site.register(Moto, MotoAdmin)
admin.site.register(Medio_Publicitario,MediosAdmin)
admin.site.unregister(Site)
admin.site.register(Kit,KitAdmin)
admin.site.register(Inventario_motos, InventarioMotosAdmin)
admin.site.register(T_financiacion,T_financiacionAdmin)
admin.site.register(Matricula,MatriculaAdmin)
admin.site.register(RequisitoTabla,TablaRequisitoAdmin)
#admin.site.register(Cotizacion, CotizacionAdmin)
