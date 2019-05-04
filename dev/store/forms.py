from enum import Enum

from django import forms

from .models import Item


class CategoryChoice(Enum):  # A subclass of Enum
	AL = 'ALL'
	HO = 'HOME'
	WO = 'WORK'


class OpenStoreForm(forms.Form):
	name = forms.CharField()
	description = forms.CharField(max_length=128)


class ItemForm(forms.Form):
	# name = forms.CharField()
	class Meta:
		model = Item
		fields = ['name', 'description', 'category', 'price', 'quantity']
