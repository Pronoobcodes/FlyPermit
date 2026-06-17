from rest_framework.routers import DefaultRouter

from .views import CountryViewSet,VisaTypeViewSet,DocumentRequirementViewSet


visa_router = DefaultRouter()

visa_router.register("countries", CountryViewSet, basename="countries")
visa_router.register("documents", DocumentRequirementViewSet, basename="documents")
visa_router.register("", VisaTypeViewSet, basename="visas")

# Register the catch-all empty-prefix VisaTypeViewSet last so its detail route
# does not shadow the /documents/ endpoint.

urlpatterns = visa_router.urls