from django import forms

from .models import Item


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
