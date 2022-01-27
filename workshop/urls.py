from .views import AccueilView, CoursView, StagesView, CopyrightView, CookiesView, AnimateurView
from django.urls import path
app_name = "workshop"

urlpatterns = [
    path('accueil/', AccueilView.as_view(), name="accueil"),
    path('cours/', CoursView.as_view(), name="cours"),
    path('animateur/', AnimateurView.as_view(), name="animateur"),
    path('stages/', StagesView.as_view(), name="stages"),
    path('copyright/', CopyrightView.as_view(), name="copyright"),
    path('cookie_policy/', CookiesView.as_view(), name="cookie_policy"),
]
