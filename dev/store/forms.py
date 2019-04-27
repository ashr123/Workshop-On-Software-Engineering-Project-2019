from django import forms

class OpenStoreForm(forms.Form):
	name = forms.CharField()