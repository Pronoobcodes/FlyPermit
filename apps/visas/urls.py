from rest_framework.routers import DefaultRouter

from .views import CountryViewSet,VisaTypeViewSet,DocumentRequirementViewSet


visa_router = DefaultRouter()

visa_router.register("countries", CountryViewSet, basename="countries")
visa_router.register("visas", VisaTypeViewSet, basename="visas")
visa_router.register("documents", DocumentRequirementViewSet, basename="documents")

urlpatterns = visa_router.urls