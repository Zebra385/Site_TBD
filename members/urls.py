
from django.urls import path, reverse_lazy
from .views import AccueilMemberView, CallExchangeMetting
# from .views import LoginUser
# from .views import RegistrationView
# from django.contrib.auth import views as auth_views

app_name = "members"


urlpatterns = [
    path('PageMember/', AccueilMemberView.as_view(), name="pagemember"),
    path('RegisterCall/', CallExchangeMetting.as_view(), name="registercall"),
]