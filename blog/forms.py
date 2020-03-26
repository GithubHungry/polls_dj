from django import forms


class EmailPostForm(forms.Form):
	name = forms.CharField(max_length=100)
	email = forms.EmailField()
	to = forms.EmailField()
	comment = forms.CharField(required=False, widget=forms.Textarea)
