import django_filters
from .models import VisaType


class VisaTypeFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name="category")
    country = django_filters.NumberFilter(field_name="country_id")

    class Meta:
        model = VisaType
        fields = ["category", "country"]