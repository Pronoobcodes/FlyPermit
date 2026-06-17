from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response

from .filter import VisaTypeFilter
from .models import Country, VisaType, DocumentRequirement
from .serializers import CountryListSerializer, CountryDetailSerializer, VisaTypeListSerializer, VisaTypeDetailSerializer, DocumentRequirementSerializer
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.


class CountryViewSet(ReadOnlyModelViewSet):
    def get_queryset(self):
        if self.action == "retrieve":
            return Country.objects.prefetch_related('visa_types')
        return Country.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CountryDetailSerializer
        return CountryListSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'message': 'Country retrieved successfully.',
            'data': serializer.data
        })
    

class VisaTypeViewSet(ReadOnlyModelViewSet):
    queryset = VisaType.objects.select_related("country").prefetch_related("document_requirements").filter(is_active=True)
    filter_backends = [DjangoFilterBackend]
    filterset_class = VisaTypeFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return VisaTypeDetailSerializer
        return VisaTypeListSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'message': 'Visa type retrieved successfully.',
            'data': serializer.data
        })
    

class DocumentRequirementViewSet(ReadOnlyModelViewSet):
    queryset = DocumentRequirement.objects.select_related("visa_type","visa_type__country")
    serializer_class = DocumentRequirementSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'message': 'Document requirement retrieved successfully.',
            'data': serializer.data
        })