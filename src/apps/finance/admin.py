from django.contrib import admin
from .models import AccountPayable

@admin.register(AccountPayable)
class AccountPayableAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'due_date', 'status', 'category', 'is_late')
    list_filter = ('status', 'category', 'due_date')
    search_fields = ('description', 'supplier')
    date_hierarchy = 'due_date'
    
    def is_late(self, obj):
        return obj.is_late
    is_late.boolean = True
    is_late.short_description = "Atrasado?"
