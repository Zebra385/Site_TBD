
from django.urls import path, reverse_lazy
from .views import MyLogoutView
from .views import LoginUser
from .views import RegistrationView
from django.contrib.auth import views as auth_views

app_name = "accounts"


urlpatterns = [
    path('login/', LoginUser.as_view(), name="login"),
    path('logout/', MyLogoutView.as_view(), name="logout"),
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name='accounts/reset_password.html',
        success_url=reverse_lazy('accounts:password_reset_done')),
        name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_sent.html',
        ),
        name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/password_reset_form.html',
            success_url=reverse_lazy('accounts:password_reset_complete')
         ),
         name="password_reset_confirm"
         ),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(
            template_name='accounts/password_reset_done.html'
         ),
         name="password_reset_complete"
         ),
    path('register/', RegistrationView.as_view(), name="register"),
]
