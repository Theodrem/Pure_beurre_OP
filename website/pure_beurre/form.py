from django import forms


class AskFoodform(forms.Form):
    food = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Rechercher'}), max_length=100)