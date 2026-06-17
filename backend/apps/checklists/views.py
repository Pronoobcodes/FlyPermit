from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Count, Q, Case, When, Value, FloatField
from django.db.models.functions import Cast

from .models import UserChecklist, ChecklistItem
from .serializers import UserChecklistSerializer, ChecklistItemSerializer
from .permissions import IsChecklistOwner
from .services import create_checklist_items


class UserChecklistViewSet(viewsets.ModelViewSet):
    serializer_class = UserChecklistSerializer
    permission_classes = [IsAuthenticated, IsChecklistOwner]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_queryset(self):
        total_count = Count('items')
        completed_count = Count('items', filter=Q(items__status='have_it'))
        return UserChecklist.objects.filter(user=self.request.user).annotate(
            total_items=total_count,
            completed_items=completed_count
        ).annotate(
            completion_pct=Case(
                When(total_items=0, then=Value(0.0)),
                default=Cast('completed_items', FloatField()) / Cast('total_items', FloatField()) * 100,
                output_field=FloatField()
            )
        ).select_related('visa_type').prefetch_related('items', 'items__document').order_by('-created_at')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        visa_type_id = serializer.validated_data.get('visa_type').id
        checklist, created = UserChecklist.objects.get_or_create(
            user=request.user,
            visa_type_id=visa_type_id,
            defaults=serializer.validated_data
        )

        if created:
            create_checklist_items(checklist)
            message = 'Checklist created successfully.'
            status_code = status.HTTP_201_CREATED
        else:
            message = 'Checklist already exists. Resuming application.'
            status_code = status.HTTP_200_OK

        # Fetch the checklist with annotated completion percentage
        annotated_checklist = self.get_queryset().get(id=checklist.id)
        response_serializer = self.get_serializer(annotated_checklist)

        return Response({
            'success': True,
            'message': message,
            'data': response_serializer.data
        }, status=status_code)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'message': 'Checklist retrieved successfully.',
            'data': serializer.data
        })

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'message': 'Checklists retrieved successfully.',
            'data': serializer.data
        })

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'success': True,
            'message': 'Checklist updated successfully.',
            'data': serializer.data
        })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({
            'success': True,
            'message': 'Checklist deleted successfully.'
        }, status=status.HTTP_200_OK)


class ChecklistItemViewSet(mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           viewsets.GenericViewSet):
    serializer_class = ChecklistItemSerializer
    permission_classes = [IsAuthenticated, IsChecklistOwner]

    def get_queryset(self):
        return ChecklistItem.objects.filter(checklist__user=self.request.user).select_related('document', 'checklist')

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.status == 'have_it' and not instance.marked_done_at:
            instance.marked_done_at = timezone.now()
            instance.save()
        elif instance.status != 'have_it' and instance.marked_done_at:
            instance.marked_done_at = None
            instance.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # Refresh and sync checklist status AFTER the save completes fully
        instance.refresh_from_db()
        instance.checklist.sync_status()
        
        return Response({
            'success': True,
            'message': 'Checklist item updated successfully.',
            'data': serializer.data
        })

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'message': 'Checklist item retrieved successfully.',
            'data': serializer.data
        })

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'message': 'Checklist items retrieved successfully.',
            'data': serializer.data
        })
