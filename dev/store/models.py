import uuid
from django.db import models
from django.contrib.auth.models import User
from enum import Enum


class CategoryChoice(Enum):  # A subclass of Enum
	AL = 'ALL'
	HO = 'HOME'
	WO = 'WORK'


# Create your models here.
class Item(models.Model):
	itemId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
	name = models.CharField(max_length=30, default=None)
	description = models.CharField(max_length=64, default=None)
	category = models.CharField(
		max_length=5,
		choices=[(tag, tag.value) for tag in CategoryChoice], default='ALL')

	quantity = models.PositiveIntegerField(default=1)
	# store_id = models.IntegerField(default=404)

	def __str__(self):
		return str(self.item) + ": $" + str(self.price)


class Store(models.Model):
	name = models.CharField(max_length=30)
	owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
	items = models.ManyToManyField(Item)
