from accounts.forms import CreatUserForm
from django.contrib.auth import logout, login
from django.views.generic.base import View
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView


class LoginUser(LoginView):
    """
    That class to login a user of the site
    who are in the data base user admin
    """
    template_name = 'accounts/login.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = ''
        return context


class MyLogoutView(LogoutView):
    """ That class to login out a user of site"""

    def post(self, request):
        logout(request)
        # Redirect to a accueil page.
        return HttpResponseRedirect('/')
