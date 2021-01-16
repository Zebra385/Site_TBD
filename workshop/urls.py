from .views import AccueilView, CoursView, StagesView, CopyrightView
from django.urls import path, include

app_name = "workshop"

urlpatterns = [
    path('accueil/', AccueilView.as_view(), name="accueil"),
    path('cours/', CoursView.as_view(), name="cours"),
    path('stages/', StagesView.as_view(), name="stages"),
    path('copyright/', CopyrightView.as_view(), name="copyright"),
]
