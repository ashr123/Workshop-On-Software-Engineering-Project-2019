from django import forms
from django.utils.safestring import mark_safe

from .models import Item, Store, Discount, MaxMinCondition


class StoreForm(forms.ModelForm):
	class Meta:
		model = Store
		fields = ['name', 'owners', 'description', 'discounts']
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
		# print('\n kkkk ', items)
		list_ = items
		self.fields['items'] = forms.MultipleChoiceField(
			choices=[(o.id,
			          mark_safe(' <a id="update_href" href=' + '/' + 'store/update_item/' + str(
				          o.id) + '>' + o.name + '  :  ' + o.description + '</a>')) for o in
			         list_]
			, widget=forms.CheckboxSelectMultiple(),

		)


class AddRuleToStore(forms.Form):
	CHOICES = (('MAX_QUANTITY', 'Max quantity - restrict max amount of items per order'),
	           ('MIN_QUANTITY', 'Min quantity - restrict min amount of items per order'),
	           ('FORBIDDEN_COUNTRY', 'Forbidden Country - restrict orderes for specific country'),
	           ('REGISTERED_ONLY', 'Registered only - only members will be able to buy from your store'),)
	# LOGICS = (('OR', 'or - OR to existing rules of this store'),
	#           ('AND', 'and - AND to existing rules of this store'),
	#           ('XOR', 'xor - XOR to existing rules of this store'))
	# operator = forms.ChoiceField(choices=LOGICS, widget=forms.RadioSelect)
	rules = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=False)
	# parameter_number = forms.IntegerField(min_value=0, required=False)
	parameter = forms.CharField(max_length=100, required=False)


class MaxMinConditionForm(forms.ModelForm):
	cond_min_max = forms.BooleanField(required=False)
	class Meta:
		model = MaxMinCondition
		fields = ['min_amount', 'max_amount']


class AddDiscountForm(forms.ModelForm):
	class Meta:
		model = Discount
		fields = ['end_date', 'percentage', ]


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


class PayForm(forms.Form):
	holder = forms.CharField(max_length=50, required=True)
	id = forms.IntegerField()
	card_number = forms.IntegerField(required=True)
	month = forms.IntegerField(required=True)
	year = forms.IntegerField(required=True)
	cvc = forms.CharField(required=True, label='CVV / CVC',
	                      widget=forms.TextInput(attrs={'size': '3',
	                                                    'maxlength': '3',
	                                                    'placeholder': ''}))


class ShippingForm(forms.Form):
	name = forms.CharField(label='Customer', max_length=25, required=True)
	street = forms.CharField(label='Street', max_length=30)
	city = forms.CharField(label='City', max_length=25)
	country = forms.CharField(max_length=25)
	zip = forms.IntegerField(label='Zip Code')
