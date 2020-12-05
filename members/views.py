from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import HttpResponse
# Create your views here.


class AccueilMemberView(TemplateView):
    """ That class to get the acceuil page"""
    template_name = "members/accueil_member.html"