from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import CustomUser, Installation, Maintenance, Stock, Equipment
from .serializers import CustomUserSerializer, InstallationSerializer, MaintenanceSerializer, StockSerializer, EquipmentSerializer
from rest_framework.pagination import PageNumberPagination

#For login
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny




# Pagination
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

# Notifications WebSocket
def send_ws_update(channel, data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        channel, {"type": "send_update", "message": data}
    )

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by('-created_at')
    serializer_class = CustomUserSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['user_type', 'is_blocked']
    search_fields = ['username', 'email']

    @action(detail=True, methods=['post'])
    def block(self, request, pk=None):
        user = self.get_object()
        user.is_blocked = True
        user.save()
        send_ws_update("users", {"id": user.id, "is_blocked": True})
        return Response({'status': 'user blocked'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def unblock(self, request, pk=None):
        user = self.get_object()
        user.is_blocked = False
        user.save()
        send_ws_update("users", {"id": user.id, "is_blocked": False})
        return Response({'status': 'user unblocked'}, status=status.HTTP_200_OK)

class InstallationViewSet(viewsets.ModelViewSet):
    queryset = Installation.objects.all()
    serializer_class = InstallationSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]

class MaintenanceViewSet(viewsets.ModelViewSet):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAdminUser]

class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]




class LoginView(APIView):
    permission_classes = [AllowAny] # Pour permettre l'accès aux non authentifié (à tout le monde de se connecter)

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")


        #try:
        #    user = User.objects.get(email=email) # On récupère l'utilisateur par son email(s'il existe)
        #except User.DoesNotExist:
        #    return Response({"error": "Identifiants invalides ou accès refusé"}, status=status.HTTP_401_UNAUTHORIZED)
        
        user = authenticate(request, username=email, password=password) # On authentifie l'utilisateur(utiliser email comme identifiant)

        if user and user.is_staff:  # Seuls les admins peuvent se connecter (Verifie que l'utilisateur est un admin)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)

        return Response({"error": "Identifiants invalides ou accès refusé"}, status=status.HTTP_401_UNAUTHORIZED)