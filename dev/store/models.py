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
		return reverse('item-detail', kwargs={'id': self.pk})
	def __str__(self):
		return "Name: " + self.name + ", Category: " + self.get_category_display() + ", Description: " + self.description + ", Price: " + str(self.price) + ", Quantity: " + str(self.quantity)

	# def your_view(request, category_):
	#
	# 	if category_ == "all" or category_ == "ALL":
	# 		item = Item.objects.filter(category=1)
	# 	elif category_ == "all" or category_ == "HOME":
	# 		item = Item.objects.filter(category=2)
	# 	else:
	# 		item = Item.objects.filter(category=3)

class Store(models.Model):
	name = models.CharField(max_length=30)
	# owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
	owners = models.ManyToManyField(User)
	managers = models.ManyToManyField(User,related_name="store_managers")
	items = models.ManyToManyField(Item)
	description = models.CharField(max_length=64)
	discount = models.PositiveIntegerField(default=0)

	max_quantity = models.PositiveIntegerField(null=True, blank=True)
	max_op = models.CharField(max_length=3, null=True, blank=True)
	min_quantity = models.PositiveIntegerField(null=True, blank=True)
	min_op = models.CharField(max_length=3, null=True, blank=True)
	registered_only = models.BooleanField(default=False)
	registered_op = models.CharField(max_length=3, null=True, blank=True)

	class Meta:
		permissions = (
			('ADD_ITEM', 'add item'),
			('REMOVE_ITEM', 'delete item'),
			('EDIT_ITEM', 'update item'),
			('ADD_MANAGER', 'add manager'),
			('REMOVE_STORE', 'delete store'),
			('ADD_DISCOUNT', 'add discount'),
		)



class BaseRule(models.Model):
	MAX_QUANTITY = 'MXQ'
	MIN_QUANTITY = 'MNQ'
	REGISTERED_ONLY = 'RGO'
	FORBIDDEN_COUNTRIES = 'FBC'
	RULE_TYPES = (
		(MAX_QUANTITY, 'max_quantity'),
		(MIN_QUANTITY, 'min_quantity'),
		(REGISTERED_ONLY, 'registered_only'),
		(FORBIDDEN_COUNTRIES, 'forbidden_countries')
	)
	store = models.ForeignKey(Store, on_delete=models.CASCADE)
	type = models.CharField(max_length=3, choices=RULE_TYPES)
	parameter = models.CharField(max_length=120)


class ItemRule(models.Model):
	MAX_QUANTITY = 'MXQ'
	MIN_QUANTITY = 'MNQ'
	RULE_TYPES = (
		(MAX_QUANTITY, 'max_quantity'),
		(MIN_QUANTITY, 'min_quantity'),
	)
	item = models.ForeignKey(Item, on_delete=models.CASCADE)
	type = models.CharField(max_length=3, choices=RULE_TYPES)
	parameter = models.CharField(max_length=120)

