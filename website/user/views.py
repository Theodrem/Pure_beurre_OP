from django.http import HttpResponseRedirect
from django.views import View
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .form import RegisterForm, LoginForm


@method_decorator(login_required, name='dispatch')
class Dashboard(View):
    def get(self, request, username):
        user = User.objects.get(username=username)
        email = user.email
        return render(request, "user/dashboard.html", {'username': username,
                                                       'email': email})


class Register(View):
    form = RegisterForm
    template_name = 'user/register.html'

    def get(self, request):
        form = self.form()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
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

                print("Utilisateur %s créé" % username)

                return HttpResponseRedirect('/dashboard/%s' % username)
        else:
            form = RegisterForm()
        return render(request, self.template_name, {'form': form})


class Login(View):
    form = LoginForm
    template_name = "user/login.html"

    def get(self, request):
        form = self.form()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.method == 'POST':
            form = self.form(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    print("Utilisateur %s connecté" % username)
                    return HttpResponseRedirect('/dashboard/%s' % username)

                else:
                    messages.add_message(request, messages.INFO, 'Le Mot de passe ne correspond pas.')

        else:
            form = self.form()

        return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
class Logout(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/login')
