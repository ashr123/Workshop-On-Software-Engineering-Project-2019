from django import forms

from .models import Item


class OpenStoreForm(forms.Form):
	name = forms.CharField()
	description = forms.CharField(max_length=128)


class ItemForm(forms.ModelForm):
	class Meta:
		model = Item
		fields = ['name', 'description', 'category', 'price', 'quantity']


class BuyForm(forms.Form):
	amount = forms.IntegerField()
