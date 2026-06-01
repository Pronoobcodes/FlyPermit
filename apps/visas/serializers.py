from rest_framework import serializers
from .models import Country, VisaType, DocumentRequirement


class DocumentRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentRequirement
        fields = ['id', 'name', 'description', 'importance', 'condition_note', 'order']


class VisaTypeListSerializer(serializers.ModelSerializer):
    country = serializers.CharField(source='country.name', read_only=True)

    class Meta:
        model = VisaType
        fields = ['id', 'name', 'country', 'category', 'processing_time', 'fee_usd', 'validity']