from django import forms


class SomeForm(forms.Form):
	CHOICES = (('a', 'add item'),
	           ('b', 'delete item'),
	           ('c', 'update item'),
	           ('d', 'add manager'),)
	picked = forms.MultipleChoiceField(choices=CHOICES, widget=forms.CheckboxSelectMultiple())


class SearchForm(forms.Form):
	search = forms.CharField()
