import logging
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseRedirect
from django.views import View
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .form import RegisterForm, LoginForm, ForgotForm, ResetPasswordForm


class Dashboard(View):
    """
    Page Dashboard
    """
    @method_decorator(login_required, name='dispatch')
    def get(self, request):
        current_user = request.user
        """
        The logged in user can access their account
        """
        user = User.objects.get(username=current_user.username)
        return render(request, "user/dashboard.html", {'user': user,
                                                       'title': "Mon compte"})


class Register(View):
    """
    Register page
    """
    form = RegisterForm
    template_name = 'user/register.html'

    def get(self, request):
        """
        Displays the register form
        """
        form = self.form()
        return render(request, self.template_name, {'form': form, 'title': "Inscription"})

    def post(self, request):
        """
        If the form is correct and the user does not exist. The user is created and then logged in automatically.
        The user is redirect on dashboard page.
        Otherwise an error message is displayed.
        """
        if request.method == 'POST':
            form = self.form(request.POST)
            if form.is_valid():
                User.objects.create_user(form.cleaned_data['username'],
                                         form.cleaned_data['email'],
                                         form.cleaned_data['password'],
                                         first_name=form.cleaned_data['first_name'],
                                         last_name=form.cleaned_data['last_name'])

                username = User.objects.get(username=form.cleaned_data['username'])

                user = authenticate(request, username=username, password=form.cleaned_data['password'])
                if user is not None:
                    login(request, user)

                logging.info("Utilisateur %s créé" % username)

                return HttpResponseRedirect('/dashboard/')
        else:
            form = RegisterForm()
        return render(request, self.template_name, {'form': form})


class Login(View):
    """
    Login page
    """
    form = LoginForm
    template_name = "user/login.html"

    def get(self, request):
        """
        Displays the login form
        """
        form = self.form()
        return render(request, self.template_name, {'form': form, 'title': "Connexion"})

    def post(self, request):
        """
        If the form is correct and the user does not exist. The user is logged.
        The user is redirect on dashboard page.
        Otherwise an error message is displayed.
        """
        if request.method == 'POST':
            form = self.form(request.POST)
            if form.is_valid():
                username = form.data.get('username')
                password = form.data.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    logging.info("Utilisateur %s connecté" % username)
                    return HttpResponseRedirect('/dashboard/')

                else:
                    messages.add_message(request, messages.INFO, 'Le Mot de passe ne correspond pas.')

        else:
            form = self.form()

        return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
class Logout(View):
    """
    If the user is logged in, he can log out.
    The user is redirect on login page.
    """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/login')


class ForgotPassword(View):
    form = ForgotForm
    template_name = "user/forgot_password.html"

    def get(self, request):
        form = self.form
        return render(request, self.template_name, {'form': form, 'Title': 'Récuperation mot de passe'})

    def post(self, request):
        if request.method == 'POST':

            form = self.form(request.POST)
            if form.is_valid():
                email_user = form.data.get('email')
                user = User.objects.get(email=email_user)
                subject = 'Récupération de votre mot de passe'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email_user, ]
                html_message = render_to_string('user/email_content.html', {'user': user})
                plain_message = strip_tags(html_message)
                send_mail(subject, plain_message, email_from, recipient_list, html_message=html_message)

                messages.add_message(request, messages.INFO, "L'email de récupération à été envoyée")
                return render(request, self.template_name, {'form': form})
        else:
            form = self.form()
        return render(request, self.template_name, {'form': form})


class ResetPassword(View):
    template_name = "user/reset_password.html"
    form = ResetPasswordForm

    def get(self, request):
        form = self.form
        return render(request, self.template_name, {'form': form, 'title': 'Récuperation mot de passe'})

    def post(self, request):
        if request.method == 'POST':
            form = self.form(request.POST)
            if form.is_valid():
                messages.add_message(request, messages.INFO, "L'email de récupération à été envoyée")
        else:
            form = self.form()

        return render(request, self.template_name, {'form': form})



