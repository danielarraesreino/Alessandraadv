from django.contrib import admin
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'client_type', 'email', 'created_at')
    list_filter = ('client_type', 'created_at')
    search_fields = ('full_name', 'email')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Identificação', {
            'fields': ('full_name', 'client_type')
        }),
        ('Dados Criptografados (PII)', {
            'fields': ('cpf_cnpj', 'phone'),
            'description': 'Dados sensíveis armazenados com criptografia (LGPD)'
        }),
        ('Contato', {
            'fields': ('email',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
