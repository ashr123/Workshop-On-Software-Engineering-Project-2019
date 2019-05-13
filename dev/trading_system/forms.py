from django import forms


class SearchForm(forms.Form):
	search = forms.CharField()

class BidForm(forms.Form):
	offer = forms.DecimalField(max_digits=6, decimal_places=2)
