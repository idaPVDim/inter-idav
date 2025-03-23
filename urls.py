from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, InstallationViewSet, MaintenanceViewSet, StockViewSet, EquipmentViewSet, LoginView

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'installations', InstallationViewSet)
router.register(r'maintenances', MaintenanceViewSet)
router.register(r'stocks', StockViewSet)
router.register(r'equipments', EquipmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', LoginView.as_view(), name='login'), # Ajout de l'authentification
]