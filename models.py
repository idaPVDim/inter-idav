from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('technician', 'Technicien'),
        ('client', 'Client'),
        ('merchant', 'Commerçant'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='client')
    is_blocked = models.BooleanField(default=False)
    status = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

class Installation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='installations')
    date = models.DateField()
    location = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"Installation {self.id} by {self.user.username}"

class Maintenance(models.Model):
    installation = models.ForeignKey(Installation, on_delete=models.CASCADE, related_name='maintenances')
    date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return f"Maintenance {self.id} for Installation {self.installation.id}"

class Stock(models.Model):
    item_name = models.CharField(max_length=255, unique=True)
    quantity = models.IntegerField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.item_name

class Equipment(models.Model):
    name = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=255)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
