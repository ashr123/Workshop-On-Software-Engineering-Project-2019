from django import forms


class InitiateForm(forms.Form):
	user_name = forms.CharField(label='name', max_length=100)
	password = forms.CharField(label='password', max_length=100)
