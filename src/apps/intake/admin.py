from django.contrib import admin
from django.contrib import messages
from .models import Lead, TriageSession

def resend_whatsapp_notification(modeladmin, request, queryset):
    """Ação para reenviar notificação WhatsApp."""
    from apps.whatsapp.services.notification import WhatsAppNotificationService
    
    service = WhatsAppNotificationService(provider='mock')
    sent_count = 0
    
    for lead in queryset:
        try:
            if service.send_lead_notification(lead):
                sent_count += 1
        except Exception as e:
            messages.error(request, f"Erro ao enviar para {lead.full_name}: {e}")
    
    messages.success(request, f"{sent_count} notificação(ões) enviada(s) com sucesso!")

resend_whatsapp_notification.short_description = "📱 Reenviar notificação WhatsApp"

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'case_type', 'score', 'is_qualified', 'created_at')
    list_filter = ('case_type', 'is_qualified', 'created_at')
    search_fields = ('full_name', 'contact_info')
    readonly_fields = ('created_at', 'score')
    actions = [resend_whatsapp_notification]
    
    fieldsets = (
        ('Informações do Lead', {
            'fields': ('full_name', 'contact_info', 'case_type')
        }),
        ('Triagem', {
            'fields': ('triage_data', 'score', 'is_qualified')
        }),
        ('Metadata', {
            'fields': ('created_at',)
        }),
    )

@admin.register(TriageSession)
class TriageSessionAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'current_step', 'updated_at')
    search_fields = ('session_id',)
    readonly_fields = ('updated_at',)
