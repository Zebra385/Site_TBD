from django.shortcuts import render
from django.views.generic.base import TemplateView
# Create your views here.


class AccueilView(TemplateView):
    """ That class to get the acceuil page"""
    template_name = "workshop/index.html"
    