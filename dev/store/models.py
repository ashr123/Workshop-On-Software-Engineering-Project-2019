from django.contrib.auth.models import User
from django.db import models

CategoryChoice = (
	("1", "ALL"),
	("2", "HOME"),
	("3", "WORK"),
)



# Create your models here.
class Item(models.Model):
	# itemId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
	name = models.CharField(max_length=30, default=None)
	description = models.CharField(max_length=64, default=None)
	category = models.CharField(max_length=30,choices=CategoryChoice,
	                            default=1)
	quantity = models.PositiveIntegerField(default=1)

	def __str__(self):
		return self.name


class Store(models.Model):
	name = models.CharField(max_length=30)
	owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
	items = models.ManyToManyField(Item)
	description = models.CharField(max_length=64)
