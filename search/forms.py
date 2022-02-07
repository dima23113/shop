from django import forms


class SearchProductForm(forms.Form):
    search_field = forms.CharField(max_length=256, required=True, initial=False)
