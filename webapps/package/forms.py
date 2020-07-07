from django import forms


class SearchForm(forms.Form):
    searchstring = forms.CharField(label='Search')
