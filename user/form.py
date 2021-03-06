from django.contrib.auth.password_validation import validate_password
from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur  *", widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=100)
    first_name = forms.CharField(label="Prenom  ", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=100)
    last_name = forms.CharField(label="Nom", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=100)
    email = forms.EmailField(label="Email  *", widget=forms.EmailInput(attrs={'class': 'form-control'}), max_length=100)
    password = forms.CharField(label="Mot de passe(minimum 8 caractèes) *", widget=forms.PasswordInput(attrs={'class': 'form-control'}), validators=[validate_password], max_length=100)
    repassword = forms.CharField(label=" Confirmation mot de passe  *", widget=forms.PasswordInput(attrs={'class': 'form-control'}), max_length=100)

    def clean(self):
        """
        If password and repassword doesn't match.
        Displays the error message
        """
        cleaned_data = super(RegisterForm, self).clean()
        val_pwd = cleaned_data.get('password')
        repassword = cleaned_data.get('repassword')
        if val_pwd != repassword:
            raise forms.ValidationError("Les mots de passes ne correspondent pas")

    def clean_email(self):
        """
        If email already exists.
        Displays the error message.
        """
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email déjà utilisé.")
        return email

        # Add this to check if the username already exists in your database or not

    def clean_username(self):
        """
        If username already exists.
        Displays the error message.
        """
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError("Nom d'utilisateur déjà utilisé.")
        return username


class LoginForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=100)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={'class': 'form-control'}), max_length=100)

    def clean_username(self):
        """
        If username doesn't exists.
        Displays the error message.
        """
        username = self.cleaned_data["username"]
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("Le nom d'utilisateur %s n'existe pas" % username)


