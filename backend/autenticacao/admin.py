from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ('cpf', 'is_active', 'is_staff', 'criado_em')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('cpf',)
    ordering = ('cpf',)
    fieldsets = (
        (None, {'fields': ('cpf', 'password')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('cpf', 'password1', 'password2'),
        }),
    )
