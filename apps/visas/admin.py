from django.contrib import admin
from .models import Country, VisaType, DocumentRequirement


class VisaTypeInline(admin.TabularInline):
    model = VisaType
    extra = 1
    fields = ['name', 'category', 'processing_time', 'fee_usd', 'validity', 'is_active']


class DocumentRequirementInline(admin.TabularInline):
    model = DocumentRequirement
    extra = 1
    fields = ['name', 'importance', 'icon_category', 'sample_description', 'official_source_url', 'last_verified', 'order']


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'flag_emoji']
    search_fields = ['name', 'code']
    inlines = [VisaTypeInline]


@admin.register(VisaType)
class VisaTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'category', 'fee_usd', 'is_active']
    list_filter = ['country', 'category', 'is_active']
    search_fields = ['name', 'country__name']
    fields = ['country', 'name', 'category', 'processing_time', 'fee_usd', 'validity', 'description', 'is_active']
    inlines = [DocumentRequirementInline]


@admin.register(DocumentRequirement)
class DocumentRequirementAdmin(admin.ModelAdmin):
    list_display = ['name', 'visa_type', 'importance', 'icon_category', 'last_verified', 'order']
    list_filter = ['importance', 'icon_category', 'visa_type__country']
    search_fields = ['name', 'visa_type__name']
    fields = ['visa_type', 'name', 'description', 'icon_category', 'importance', 'condition_note', 'sample_description', 'official_source_url', 'last_verified', 'order']
    ordering = ['order', 'name']
