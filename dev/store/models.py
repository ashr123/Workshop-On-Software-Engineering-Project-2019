from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Store(models.Model):
    name = models.CharField(max_length=30)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

