from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from trading_system.models import Cart as m_Cart


class Cart:
	def __init__(self, store_pk=None, user_pk=None, model=None):
		if model != None:
			self._model = model
			return
		self._model = m_Cart.objects.create(customer_id=user_pk, store_id=store_pk)
		self._model.save()

	def add_item(self, item_id):
		self._model.items.add(item_id)

	def remove_item(self, item_id):
		self._model.items.remove(item_id)

	@property
	def pk(self):
		return self._model.pk

	@staticmethod
	def get_cart(cart_id=None, store_pk=None, user_id=None):
		if cart_id != None:
			model = m_Cart.objects.get(pk=cart_id)
		elif user_id!= None:
			try:
				model = m_Cart.objects.get(customer_id=user_id)
			except ObjectDoesNotExist:
				return None
			except MultipleObjectsReturned:
				pass
		else:
			try:
				model = m_Cart.objects.get(store_id=store_pk, customer_id=user_id)
			except ObjectDoesNotExist:
				return None

		return Cart(model=model)
