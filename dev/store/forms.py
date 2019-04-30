from django import forms


class OpenStoreForm(forms.Form):
	name = forms.CharField()


class ItemForm(forms.Form):
	name = forms.CharField()
