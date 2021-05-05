from django.contrib.auth.password_validation import validate_password
from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur *", widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=100)
    first_name = forms.CharField(label="Prenom", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=100)
    last_name = forms.CharField(label="Nom", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=100)
    email = forms.EmailField(label="Email *", widget=forms.EmailInput(attrs={'class': 'form-control'}), max_length=100)
    password = forms.CharField(label="Mot de passe(minimum 8 caractères) *", widget=forms.PasswordInput(attrs={'class': 'form-control'}), validators=[validate_password], max_length=100)
    repassword = forms.CharField(label=" Confirmation mot de passe *", widget=forms.PasswordInput(attrs={'class': 'form-control'}), max_length=100)

    def check_password_matches(self):
        """
        If password and repassword doesn't match.
        Displays the error message
        """
        cleaned_data = super(RegisterForm, self).clean()
        val_pwd = cleaned_data['password']
        repassword = cleaned_data['repassword']
        if val_pwd != repassword:
            raise forms.ValidationError("Les mots de passes ne correspondent pas")

    def check_email_already_exist(self):
        """
        If email already exists.
        Displays the error message.
        """
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email déjà utilisé.")
        return email

        # Add this to check if the username already exists in your database or not

    def check_username_already_exist(self):
        """
        If username already exists.
        Displays the error message.
        """
        username = self.cleaned_data.get("username")
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError("Nom d'utilisateur déjà utilisé.")
        return username


class LoginForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur *", widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=100)
    password = forms.CharField(label="Mot de passe *", widget=forms.PasswordInput(attrs={'class': 'form-control'}), max_length=100)

    def check_username_exist(self):
        """
        If username doesn't exists.
        Displays the error message.
        """
        username = self.cleaned_data["username"]
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("Le nom d'utilisateur %s n'existe pas" % username)


class ForgotForm(forms.Form):
    email = forms.EmailField(label="", widget=forms.EmailInput(attrs={'placeholder': 'Entre ton email', 'class': 'form-control'}), max_length=100)

    def check_email_exist(self):
        """
        If email already exists.
        Displays the error message.
        """
        email = self.cleaned_data.get("email")
        if not email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("Aucun utilisateur ne possède cet email.")

