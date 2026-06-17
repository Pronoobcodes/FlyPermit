from rest_framework import serializers
from .models import UserChecklist, ChecklistItem


class ChecklistItemSerializer(serializers.ModelSerializer):
    document_name = serializers.CharField(source='document.name', read_only=True)

    class Meta:
        model = ChecklistItem
        fields = ['id', 'document', 'document_name', 'status', 'user_note', 'marked_done_at']
        read_only_fields = [ 'id', 'document_name', 'marked_done_at']


class UserChecklistSerializer(serializers.ModelSerializer):
    visa_type_name = serializers.CharField(source='visa_type.name', read_only=True)
    completion_percentage = serializers.FloatField(read_only=True)
    items = ChecklistItemSerializer(many=True, read_only=True)

    class Meta:
        model = UserChecklist
        fields = ['id', 'visa_type', 'visa_type_name', 'status', 'notes', 'items', 'completion_percentage', 'created_at', 'updated_at']
        read_only_fields = [ 'status', 'id', 'completion_percentage', 'visa_type_name', 'created_at', 'updated_at', 'items']