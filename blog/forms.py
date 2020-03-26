from django import forms

from .models import Review


class EmailPostForm(forms.Form):
	name = forms.CharField(max_length=100)
	email = forms.EmailField()
	to = forms.EmailField()
	comment = forms.CharField(required=False, widget=forms.Textarea)


class ReviewForm(forms.ModelForm):
	class Meta:
		model = Review
		fields = ('name', 'email', 'body')
