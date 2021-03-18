from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=100)
    first_name = forms.CharField(label="Prenom", max_length=100, required=False)
    last_name = forms.CharField(label="Nom", max_length=100, required=False)
    email = forms.EmailField(label="Email", max_length=100)
    password = forms.CharField(label="Mot de passe", max_length=100, widget=forms.PasswordInput)
    repassword = forms.CharField(label=" Confirmation mot de passe", max_length=100, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        val_pwd = cleaned_data['password']
        repassword = cleaned_data['repassword']
        if val_pwd != repassword:
            raise forms.ValidationError("Les mots de passes ne correspondent pas")

    def clean_email(self):
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError("Email déjà utilisé.")
        return email

        # Add this to check if the username already exists in your database or not

    def clean_username(self):
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        if username and User.objects.filter(username=username).exclude(email=email).count():
            raise forms.ValidationError("Nom d'utilisateur déjà utilisé.")
        return username


class LoginForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=100)
    password = forms.CharField(label="Mot de passe", max_length=100, widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data["username"]
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("Le nom d'utilisateur %s n'existe pas" % username)
