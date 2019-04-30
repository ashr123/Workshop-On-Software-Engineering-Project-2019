import uuid
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Item(models.Model):
	itemId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=30)


class Store(models.Model):
	name = models.CharField(max_length=30)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	items = models.ManyToManyField(Item)
