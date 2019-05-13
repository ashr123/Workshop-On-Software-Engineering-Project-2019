from django.urls import reverse
from django.contrib.auth.models import User
from django.db import models

CategoryChoice = (
	("1", "ALL"),
	("2", "HOME"),
	("3", "WORK"),
)

class Item(models.Model):
	# itemId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
	name = models.CharField(max_length=30, default=None)
	description = models.CharField(max_length=64, default=None)
	category = models.CharField(max_length=30,choices=CategoryChoice,default=1)
	quantity = models.PositiveIntegerField(default=1)

	def get_absolute_url(self):
		return reverse('item-detail',kwargs={'id': self.pk})
	def __str__(self):
		return self.name


class Store(models.Model):
	name = models.CharField(max_length=30)
	# owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
	owners = models.ManyToManyField(User)
	items = models.ManyToManyField(Item)
	description = models.CharField(max_length=64)
	discount = models.PositiveIntegerField(default=0)

	class Meta:
		permissions = (
			('ADD_ITEM', 'add item'),
			('REMOVE_ITEM', 'delete item'),
			('EDIT_ITEM', 'update item'),
			('ADD_MANAGER', 'add manager'),
			('REMOVE_STORE', 'delete store'),
		)
