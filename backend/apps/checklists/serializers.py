from rest_framework import serializers
from .models import UserChecklist, ChecklistItem


class ChecklistItemSerializer(serializers.ModelSerializer):
    document_name = serializers.CharField(source='document.name', read_only=True)
    document_description = serializers.CharField(source='document.description', read_only=True)
    document_sample = serializers.CharField(source='document.sample_description', read_only=True)
    document_importance = serializers.CharField(source='document.importance', read_only=True)
    document_condition_note = serializers.CharField(source='document.condition_note', read_only=True)
    document_source_url = serializers.CharField(source='document.official_source_url', read_only=True)
    is_completed = serializers.BooleanField(source='is_done', read_only=True)
    notes = serializers.CharField(source='user_note', allow_blank=True, required=False)
    completed_at = serializers.DateTimeField(source='marked_done_at', read_only=True)

    class Meta:
        model = ChecklistItem
        fields = [
            'id', 'document_name', 'is_completed', 'completed_at', 'notes', 'status',
            'document_description', 'document_sample',
            'document_importance', 'document_condition_note', 'document_source_url',
        ]


from apps.visas.serializers import VisaTypeNestedSerializer
from apps.visas.models import VisaType

class UserChecklistSerializer(serializers.ModelSerializer):
    visa_type = VisaTypeNestedSerializer(read_only=True)
    visa_type_id = serializers.PrimaryKeyRelatedField(
        queryset=VisaType.objects.all(), source='visa_type', write_only=True
    )
    completion_percentage = serializers.FloatField(source='completion_pct', read_only=True)
    items = ChecklistItemSerializer(many=True, read_only=True)
    target_date = serializers.DateField(required=False, allow_null=True)

    class Meta:
        model = UserChecklist
        fields = ['id', 'visa_type', 'visa_type_id', 'status', 'notes', 'items', 'completion_percentage', 'target_date', 'created_at', 'updated_at']
        read_only_fields = ['status', 'id', 'completion_percentage', 'created_at', 'updated_at', 'items']