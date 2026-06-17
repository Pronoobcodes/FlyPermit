from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.utils import timezone

from .models import UserChecklist, ChecklistItem
from .serializers import UserChecklistSerializer, ChecklistItemSerializer
from .permissions import IsChecklistOwner
from .services import create_checklist_items


class UserChecklistViewSet(viewsets.ModelViewSet):
    serializer_class = UserChecklistSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsChecklistOwner]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return UserChecklist.objects.none()
        return UserChecklist.objects.filter(user=self.request.user).select_related('visa_type').prefetch_related('items', 'items__document')

    def perform_create(self, serializer):
        checklist = serializer.save(user=self.request.user)
        create_checklist_items(checklist)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ChecklistItemViewSet(viewsets.ModelViewSet):
    serializer_class = ChecklistItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsChecklistOwner]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return ChecklistItem.objects.none()
        return ChecklistItem.objects.filter(checklist__user=self.request.user).select_related('document', 'checklist')

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.status == 'have_it' and not instance.marked_done_at:
            instance.marked_done_at = timezone.now()
            instance.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
