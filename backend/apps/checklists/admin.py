from django.contrib import admin
from .models import UserChecklist, ChecklistItem

class ChecklistItemInline(admin.TabularInline):
    model = ChecklistItem
    extra = 0
    raw_id_fields = ['document']

@admin.register(UserChecklist)
class UserChecklistAdmin(admin.ModelAdmin):
    list_display = ['user', 'visa_type', 'status', 'completion_percentage', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__email', 'user__username', 'visa_type__name']
    inlines = [ChecklistItemInline]

@admin.register(ChecklistItem)
class ChecklistItemAdmin(admin.ModelAdmin):
    list_display = ['checklist', 'document', 'status', 'marked_done_at']
    list_filter = ['status']
    search_fields = ['checklist__user__email', 'document__name']
    raw_id_fields = ['checklist', 'document']
