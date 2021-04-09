import logging
from django.http import HttpResponseRedirect
from django.views import View
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .form import RegisterForm, LoginForm


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
        return render(request, "user/dashboard.html", {'username': user.username,
                                                       'email': user.email,
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
