from django import forms
from django.utils.safestring import mark_safe

from .models import Cart



class SomeForm(forms.Form):
	CHOICES = (('a', 'add item'),
	           ('b', 'delete item'),
	           ('c', 'update item'),
	           ('d', 'add manager'),)
	picked = forms.MultipleChoiceField(choices=CHOICES, widget=forms.CheckboxSelectMultiple())


class SearchForm(forms.Form):
	search = forms.CharField()


class CartForm(forms.Form):
	def __init__(self, user, *args, **kwargs):
		super(CartForm, self).__init__(*args, **kwargs)
		carts = Cart.objects.filter(customer=user)
		list_ = []
		for cart in carts:
			list_ += list(cart.items.all())
		self.fields['items'] = forms.MultipleChoiceField(
			choices=[(o.id,
			          mark_safe(' <a href=' + '/' + 'store/view_item/' + str(
				          o.id) + '>' + o.name + '  :  ' + o.description + '</a>')) for o in
			         list_]
			, widget=forms.CheckboxSelectMultiple(),

		)

class BidForm(forms.Form):
	offer = forms.DecimalField(max_digits=6, decimal_places=2)

