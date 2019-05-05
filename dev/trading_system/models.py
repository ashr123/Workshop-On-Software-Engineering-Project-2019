from django.contrib.auth.models import User
from store.models import Store, Item
from django.db import models

# Create your models here.
# Create your models here.

class Cart(models.Model):
	customer = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
	store = models.ForeignKey(Store, on_delete=models.CASCADE, default=None)
	items = models.ManyToManyField(Item)

	class Meta:
		unique_together = (("customer", "store"),)