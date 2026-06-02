from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.visas.filter import VisaTypeFilter
from .models import Country, VisaType, DocumentRequirement
from .serializers import CountryListSerializer, CountryDetailSerializer, VisaTypeListSerializer, VisaTypeDetailSerializer, DocumentRequirementSerializer
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.


class CountryViewSet(ReadOnlyModelViewSet):
    queryset = Country.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CountryDetailSerializer
        return CountryListSerializer
    

class VisaTypeViewSet(ReadOnlyModelViewSet):
    queryset = VisaType.objects.select_related("country").prefetch_related("document_requirements").filter(is_active=True)
    filter_backends = [DjangoFilterBackend]
    filterset_class = VisaTypeFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return VisaTypeDetailSerializer
        return VisaTypeListSerializer
    

class DocumentRequirementViewSet(ReadOnlyModelViewSet):
    queryset = DocumentRequirement.objects.select_related("visa_type","visa_type__country")
    serializer_class = DocumentRequirementSerializer