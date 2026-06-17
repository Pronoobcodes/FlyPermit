from rest_framework import serializers
from .models import UserChecklist, ChecklistItem


class ChecklistItemSerializer(serializers.ModelSerializer):
    document_name = serializers.CharField(source='document.name', read_only=True)
    document_description = serializers.CharField(source='document.description', read_only=True)

    class Meta:
        model = ChecklistItem
        fields = ['id', 'document', 'document_name', 'document_description', 'status', 'user_note', 'marked_done_at']
        read_only_fields = [ 'id', 'document_name', 'document_description', 'marked_done_at']


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