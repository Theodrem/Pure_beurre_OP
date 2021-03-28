from django import forms


class AskFoodform(forms.Form):
    food = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Rechercher', 'class': 'form-control mb-2 mr-sm-2'}), max_length=100)
