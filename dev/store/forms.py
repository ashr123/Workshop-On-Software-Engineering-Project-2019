from django import forms
from django.utils.safestring import mark_safe

from .models import Item, Store


class StoreForm(forms.ModelForm):
	class Meta:
		model = Store
		fields = ['name', 'owners', 'description', 'discount']
		widgets = {
			'owners': forms.CheckboxSelectMultiple,
			# 'items': forms.CheckboxSelectMultiple,
		}


# 		def __init__(self, user, list_for_guest, *args, **kwargs):
# 			super(StoreForm, self).__init__(*args, **kwargs)
# 			self.fields['items'] = forms.MultipleChoiceField(
# 				choices=[(o.id,
# 				          mark_safe(' <a id="buy_href" href=' + '/' + 'store/view_item/' + str(
# 					          o.id) + '>' + o.name + '  :  ' + o.description + '</a>')) for o in
# 				         ]
#

class UpdateItems(forms.Form):

	def __init__(self, items, *args, **kwargs):
		super(UpdateItems, self).__init__(*args, **kwargs)
		print('\n kkkk ', items)
		list_ = items
		self.fields['items'] = forms.MultipleChoiceField(
			choices=[(o.id,
			          mark_safe(' <a id="update_href" href=' + '/' + 'store/update_item/' + str(
				          o.id) + '>' + o.name + '  :  ' + o.description + '</a>')) for o in
			         list_]
			, widget=forms.CheckboxSelectMultiple(),

		)


class AddRuleToStore(forms.Form):
	CHOICES = (('MAX_QUANTITY', 'Max_quantity - restrict max amount of items per order'),
	           ('MIN_QUANTITY', 'Min_quantity - restrict min amount of items per order'),
	           ('REGISTERED_ONLY', 'Registered_only - only members will be able to buy from your store'),)
	LOGICS = (('OR', 'or - OR to existing rules of this store'),
	          ('AND', 'and - AND to existing rules of this store'),
	          ('XOR', 'xor - XOR to existing rules of this store'))
	operator = forms.ChoiceField(choices=LOGICS, widget=forms.RadioSelect)
	rules = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
	parameter = forms.IntegerField(min_value=0)


class AddDiscountToStore(forms.Form):
	discount = forms.IntegerField(max_value=100)


class AddManagerForm(forms.Form):
	user_name = forms.CharField()
	is_owner = forms.BooleanField(required=False)
	CHOICES = (('ADD_ITEM', 'add item'),
	           ('REMOVE_ITEM', 'delete item'),
	           ('EDIT_ITEM', 'update item'),
	           ('ADD_MANAGER', 'add manager'),
	           ('REMOVE_STORE', 'delete store'),
	           ('ADD_DISCOUNT', 'add discount'),
	           )

	permissions = forms.MultipleChoiceField(choices=CHOICES, widget=forms.CheckboxSelectMultiple())


class OpenStoreForm(forms.Form):
	name = forms.CharField()
	description = forms.CharField(max_length=128)


class ItemForm(forms.ModelForm):
	class Meta:
		model = Item
		fields = ['name', 'description', 'category', 'price', 'quantity']


class BuyForm(forms.Form):
	amount = forms.IntegerField()
