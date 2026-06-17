from rest_framework.permissions import BasePermission


class IsChecklistOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'checklist'):
            return obj.checklist.user == request.user
        return False