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


class VisaTypeDetailSerializer(serializers.ModelSerializer):
    country = serializers.StringRelatedField()
    document_requirements = DocumentRequirementSerializer(many=True, read_only=True)

    class Meta:
        model = VisaType
        fields = ["id", "name", "country", "category", "processing_time", "fee_usd", "vitality", "description", "is_active", "document_requirements"]


class CountryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ["id", "name", "code", "flag_emoji"]


class CountryDetailSerializer(serializers.ModelSerializer):

    visa_types = VisaTypeListSerializer(many=True, read_only=True)

    class Meta:
        model = Country
        fields = ["id", "name", "code", "flag_emoji", "visa_types"]


