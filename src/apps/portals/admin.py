"""
Django Admin configuration for Client Portal.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import CaseTimeline, CaseDocument, ClientPortalAccess


@admin.register(CaseTimeline)
class CaseTimelineAdmin(admin.ModelAdmin):
    list_display = ('legal_case', 'current_stage', 'progress_bar', 'last_update')
    list_filter = ('current_stage', 'last_update')
    search_fields = ('legal_case__case_number', 'legal_case__client__full_name')
    readonly_fields = ('progress_percentage', 'last_update')
    
    fieldsets = (
        ('Caso', {
            'fields': ('legal_case', 'current_stage')
        }),
        ('Progresso', {
            'fields': ('progress_percentage', 'milestones')
        }),
        ('Metadata', {
            'fields': ('last_update',),
            'classes': ('collapse',)
        }),
    )
    
    def progress_bar(self, obj):
        """Display visual progress bar."""
        percentage = obj.progress_percentage()
        color = '#4CAF50' if percentage > 75 else '#DFAE9A'
        return format_html(
            '<div style="width:100px; background:#E5E5E5; border-radius:4px;">'
            '<div style="width:{}%; background:{}; height:20px; border-radius:4px; text-align:center; color:white; font-size:11px; line-height:20px;">'
            '{}%'
            '</div></div>',
            percentage, color, percentage
        )
    progress_bar.short_description = 'Progresso'


@admin.register(CaseDocument)
class CaseDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'legal_case', 'document_type', 'uploaded_by', 'uploaded_at', 'is_visible_to_client')
    list_filter = ('document_type', 'is_visible_to_client', 'uploaded_at')
    search_fields = ('title', 'description', 'legal_case__case_number')
    readonly_fields = ('uploaded_at',)
    
    fieldsets = (
        ('Documento', {
            'fields': ('legal_case', 'document_type', 'title', 'description', 'file')
        }),
        ('Visibilidade', {
            'fields': ('is_visible_to_client',)
        }),
        ('Metadata', {
            'fields': ('uploaded_by', 'uploaded_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ClientPortalAccess)
class ClientPortalAccessAdmin(admin.ModelAdmin):
    list_display = ('client', 'legal_case', 'is_active', 'last_accessed', 'created_at')
    list_filter = ('is_active', 'created_at', 'last_accessed')
    search_fields = ('client__full_name', 'legal_case__case_number', 'access_token')
    readonly_fields = ('access_token', 'created_at', 'last_accessed')
    
    fieldsets = (
        ('Acesso', {
            'fields': ('client', 'legal_case', 'is_active')
        }),
        ('Token', {
            'fields': ('access_token',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'last_accessed'),
            'classes': ('collapse',)
        }),
    )
