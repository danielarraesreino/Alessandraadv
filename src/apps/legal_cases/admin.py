from django.contrib import admin
from .models import LegalCase

@admin.register(LegalCase)
class LegalCaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'area', 'status', 'entry_date')
    list_filter = ('status', 'area', 'entry_date')
    search_fields = ('title', 'client__full_name')
    autocomplete_fields = ['client']
