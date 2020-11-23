
from django.urls import path
from .views import MyLogoutView
from .views import RegistrationView
from .views import LoginUser

app_name = "accounts"


urlpatterns = [
    path('login/', LoginUser.as_view(), name="login"),
    path('logout/', MyLogoutView.as_view(), name="logout"),
    path('register/', RegistrationView.as_view(), name="register"),
   
    
]