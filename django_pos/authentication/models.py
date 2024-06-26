from django.contrib.auth.models import AbstractUser, Group
from django.db import models
import django.utils.timezone

class CustomUser(AbstractUser):
    ADMIN = 'admin'
    EMPLOYEE = 'employee'
    NONE = 'none'

    ROLE_CHOICES = [
        (EMPLOYEE, 'employee'),
        (ADMIN, 'admin'),
        (NONE, 'none'),
    ]

    role = models.CharField(max_length=255, choices=ROLE_CHOICES, default=NONE)  
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30 , blank=True, null=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)  # Added max_length
    address = models.CharField(max_length=100, null=True, blank=True)  # New field for address
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    # Specify unique related_name for groups and user_permissions fields
    groups = models.ManyToManyField(Group, related_name='custom_users')
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_users',
        blank=True,
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Employee(models.Model):
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)

    def __str__(self):
        return f'{self.employee.first_name} {self.employee.last_name}'