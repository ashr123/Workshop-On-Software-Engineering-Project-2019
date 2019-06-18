from django.db.models import Q

from store.models import Item as m_Item
from trading_system.domain.bi_rules import BaseItemRule
from trading_system.domain.ci_rules import ComplexItemRule


class Item:
	def __init__(self, price=None, name=None, category=None, description=None, quantity=None, model=None):
		if model != None:
			self._model = model
			return
		self._model = m_Item.objects.create(price=price, name=name, category=category, description=description,
		                                    quantity=quantity)
		self._model.save()

	def to_dict(self):
		return self._model.__dict__

	@property
	def pk(self):
		return self._model.pk

	@property
	def quantity(self):
		return self._model.quantity

	@property
	def name(self):
		return self._model.name

	@quantity.setter
	def quantity(self, value):
		self._model.quantity = value

	def has_available_amount(self, amount):
		return amount <= self._model.quantity

	def calc_total(self, amount):
		return amount*self._model.price

	def check_rules(self, amount):
		base_arr = []
		complex_arr = []
		itemRules = ComplexItemRule.get_item_ci_rules(item_id=self.pk)
		for rule in reversed(itemRules):
			if rule.id in complex_arr:
				continue
			if not rule.check(amount, base_arr, complex_arr):
				return False
		itemBaseRules = BaseItemRule.get_item_bi_rules(item_id=self.pk)
		for rule in itemBaseRules:
			if rule.id in base_arr:
				continue
			if not rule.check(amount=amount):
				return False
		return True

	def get_details(self):
		return {"pk": self._model.pk,
		        "name": self._model.name,
		        "category": self._model.get_category_display,
		        "description": self._model.description,
		        "price": self._model.price,
		        "quantity": self._model.quantity}

	def update(self, item_dict):
		for field in self._model._meta.fields:
			if field.attname in item_dict.keys():
				setattr(self._model, field.attname, item_dict[field.attname])
		self._model.save()

	def delete(self):
		self._model.delete()

	def save(self):
		self._model.save()

	@staticmethod
	def get_item(item_id):
		return Item(model=m_Item.objects.get(pk=item_id))

	@staticmethod
	def search(txt):
		items_models = m_Item.objects.filter(Q(name__contains=txt) | Q(
			description__contains=txt) | Q(category__contains=txt))
		items = list(map(lambda im: Item(model=im), items_models))
		return list(map(lambda i: i.get_details(), items))
