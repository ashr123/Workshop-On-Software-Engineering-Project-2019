from django import forms

from .models import Item


class AddDiscountToStore(forms.Form):
	discount = forms.IntegerField(max_value=100)

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

class AddManagerForm(forms.Form):
	user_name = forms.CharField()
	is_owner = forms.BooleanField( required=False)
	CHOICES = (('ADD_ITEM', 'add item'),
	           ('REMOVE_ITEM', 'delete item'),
	           ('EDIT_ITEM', 'update item'),
	           ('ADD_MANAGER', 'add manager'),)
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

