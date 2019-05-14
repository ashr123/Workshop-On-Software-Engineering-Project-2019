from django.contrib.auth.models import User
from django.db import models

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


class Auction(models.Model):
	item = models.ForeignKey(Item, on_delete=models.CASCADE, default=None)
	customers = models.ManyToManyField(User, through='AuctionParticipant')


class AuctionParticipant(models.Model):
	auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
	customer = models.ForeignKey(User, on_delete=models.CASCADE)
	offer = models.DecimalField(max_digits=6, decimal_places=2)
	address = models.URLField(max_length=250)

	class Meta:
		unique_together = (("auction", "customer"),)

