from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Modelo para o usuário"""
    gitlab = models.CharField(max_length=255, null=True, blank=True)
    gitbucket = models.CharField(max_length=255, null=True, blank=True)
    linkedin = models.CharField(max_length=255, null=True, blank=True)
    twitter = models.CharField(max_length=255, null=True, blank=True)
    website = models.URLField(max_length=255, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)