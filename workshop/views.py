from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import HttpResponse
# Create your views here.


class AccueilView(TemplateView):
    """ That class to get the acceuil page"""
    template_name = "workshop/accueil.html"
    
class CoursView(TemplateView):
    """ That class to get the coursl page"""
    template_name = "workshop/cours.html"

    # def generate_PDF(request):
    #     file = open('reglement.pdf', "w+b")
    #     file.seek(0) 
    #     pdf = file.read()
    #     file.close() 
    #     return HttpResponse(pdf, 'worshop/pdf')

class StagesView(TemplateView):
    """ That class to get the stages page"""
    template_name = "workshop/stages.html"