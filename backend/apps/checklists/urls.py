from rest_framework.routers import DefaultRouter
from .views import UserChecklistViewSet, ChecklistItemViewSet

checklist_router = DefaultRouter()

checklist_router.register("user-checklists", UserChecklistViewSet, basename="user-checklists")
checklist_router.register("checklist-items", ChecklistItemViewSet, basename="checklist-items")
urlpatterns = checklist_router.urls