from django import forms
from .models import Store, Item


class OpenStoreForm(forms.Form):
	name = forms.CharField()


class ItemForm(forms.Form):
	name = forms.CharField()


