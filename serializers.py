from rest_framework import serializers
from .models import CustomUser, Installation, Maintenance, Stock, Equipment

class CustomUserSerializer(serializers.ModelSerializer):
    installations_count = serializers.IntegerField(source="installations.count", read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'user_type', 'is_blocked', 'status', 'installations_count', 'created_at', 'updated_at']

class InstallationSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)  # Affiche les détails du user

    class Meta:
        model = Installation
        fields = '_all_'

class MaintenanceSerializer(serializers.ModelSerializer):
    installation = InstallationSerializer(read_only=True)

    class Meta:
        model = Maintenance
        fields = '_all_'

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '_all_'

class EquipmentSerializer(serializers.ModelSerializer):
    stock = StockSerializer(read_only=True)

    class Meta:
        model = Equipment
        fields = '_all_'