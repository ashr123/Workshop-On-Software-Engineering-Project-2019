from multiprocessing.managers import State

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

# class AddRuleToStore(forms.Form):
# 	CHOICES = (('MAX_QUANTITY', 'Max quantity - restrict max amount of items per order'),
# 	           ('MIN_QUANTITY', 'Min quantity - restrict min amount of items per order'),
# 	           ('FORBIDDEN_COUNTRY', 'Forbidden Country - restrict orderes for specific country'),
# 	           ('REGISTERED_ONLY', 'Registered only - only members will be able to buy from your store'),)
# 	rules = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=False)
# 	#parameter_number = forms.IntegerField(min_value=0, required=False)
# 	parameter = forms.CharField(max_length=100, required=False)


class AddRuleToStore_base(forms.Form):
	CHOICES = (('MAX_QUANTITY', 'Max quantity - restrict max amount of items per order'),
	           ('MIN_QUANTITY', 'Min quantity - restrict min amount of items per order'),
	           ('FORBIDDEN_COUNTRY', 'Forbidden Country - restrict orderes for specific country'),
	           ('REGISTERED_ONLY', 'Registered only - only members will be able to buy from your store'),)
	rule = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=False)
	#parameter_number = forms.IntegerField(min_value=0, required=False)
	parameter = forms.CharField(max_length=100, required=False)

class AddRuleToStore_withop(forms.Form):
	CHOICES = (('MAX_QUANTITY', 'Max quantity - restrict max amount of items per order'),
	           ('MIN_QUANTITY', 'Min quantity - restrict min amount of items per order'),
	           ('FORBIDDEN_COUNTRY', 'Forbidden Country - restrict orderes for specific country'),
	           ('REGISTERED_ONLY', 'Registered only - only members will be able to buy from your store'),)
	LOGICS = (('OR', 'or'),
	          ('AND', 'and'),
	          ('XOR', 'xor'))
	operator = forms.ChoiceField(choices=LOGICS, widget=forms.RadioSelect)
	rule = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=False)
	# parameter_number = forms.IntegerField(min_value=0, required=False)
	parameter = forms.CharField(max_length=100, required=False)

class AddRuleToStore_two(forms.Form):
	CHOICES = (('MAX_QUANTITY', 'Max quantity - restrict max amount of items per order'),
	           ('MIN_QUANTITY', 'Min quantity - restrict min amount of items per order'),
	           ('FORBIDDEN_COUNTRY', 'Forbidden Country - restrict orderes for specific country'),
	           ('REGISTERED_ONLY', 'Registered only - only members will be able to buy from your store'),)
	LOGICS = (('OR', 'or'),
	          ('AND', 'and'),
	          ('XOR', 'xor'))
	operator2 = forms.ChoiceField(choices=LOGICS, widget=forms.RadioSelect)
	rule1 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=False)
	parameter1 = forms.CharField(max_length=100, required=False)
	operator1 = forms.ChoiceField(choices=LOGICS, widget=forms.RadioSelect)
	rule2 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=False)
	# parameter_number = forms.IntegerField(min_value=0, required=False)
	parameter2 = forms.CharField(max_length=100, required=False)




class AddRuleToItem(forms.Form):
	CHOICES = (('MAX_QUANTITY', 'Max quantity - restrict max amount of items per order'),
	           ('MIN_QUANTITY', 'Min quantity - restrict min amount of items per order'),)
	rule = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=False)
	#parameter_number = forms.IntegerField(min_value=0, required=False)
	parameter = forms.IntegerField(min_value=1)

class AddRuleToItem_withop(forms.Form):
	CHOICES = (('MAX_QUANTITY', 'Max quantity - restrict max amount of items per order'),
	           ('MIN_QUANTITY', 'Min quantity - restrict min amount of items per order'),)
	LOGICS = (('OR', 'or'),
	          ('AND', 'and'),
	          ('XOR', 'xor'))
	operator = forms.ChoiceField(choices=LOGICS, widget=forms.RadioSelect)
	rule = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=False)
	parameter = forms.IntegerField(min_value=0)


class AddRuleToItem_two(forms.Form):
	CHOICES = (('MAX_QUANTITY', 'Max quantity - restrict max amount of items per order'),
	           ('MIN_QUANTITY', 'Min quantity - restrict min amount of items per order'),)
	LOGICS = (('OR', 'or'),
	          ('AND', 'and'),
	          ('XOR', 'xor'))
	operator2 = forms.ChoiceField(choices=LOGICS, widget=forms.RadioSelect)
	rule1 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=False)
	parameter1 = forms.CharField(max_length=100, required=False)
	operator1 = forms.ChoiceField(choices=LOGICS, widget=forms.RadioSelect)
	rule2 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=False)
	parameter2 = forms.CharField(max_length=100, required=False)

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


from .fileds import CreditCardField, ExpiryDateField, VerificationValueField

class BuyForm(forms.Form):
	amount = forms.IntegerField()


class PayForm(forms.Form):
	holder = forms.CharField(max_length=50, required=True)
	id = forms.IntegerField()
	card_number = forms.IntegerField(required=True)
	month = forms.IntegerField(required=True)
	year = forms.IntegerField(required=True)
	cvc = forms.CharField(required=True, label='CVV / CVC',
	widget = forms.TextInput(attrs={'size': '3',
	'maxlength': '3',
	'placeholder':''}))





class ShippingForm(forms.Form):
	name = forms.CharField(label='Customer', max_length=25, required=True)
	street = forms.CharField(label='Street', max_length=30)
	city = forms.CharField(label='City', max_length=25)
	country = forms.CharField(max_length=25)
	zip = forms.IntegerField(label='Zip Code')

