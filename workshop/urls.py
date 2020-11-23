from .views import AccueilView
from django.urls import path, include

app_name = "workshop"

urlpatterns = [
    path('accueil/', AccueilView.as_view(), name="accueil"),
   
    
]