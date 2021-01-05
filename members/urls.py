from django.urls import path
from .views import AccueilMemberView, CalendarExchangeMeeting
from .views import CallExchangeMeeting, ConfirmCallExchangeMeeting
from .views import ConfirmAcceptExchangeMeeting
# from .views import LoginUser
# from .views import RegistrationView
# from django.contrib.auth import views as auth_views

app_name = "members"


urlpatterns = [
    path('PageMember/',
         AccueilMemberView.as_view(),
         name="pagemember"
         ),
    path('RegisterCall/',
         CallExchangeMeeting.as_view(),
         name="registercall"
         ),
    path('CalendarExchangeMeeting/',
         CalendarExchangeMeeting.as_view(),
         name="calendarexchangemeeting"
         ),
    path('ConfirmCallExchangeMeeting/',
         ConfirmCallExchangeMeeting.as_view(),
         name="confirmcallexchangemeeting"
         ),
    path('ConfirmAcceptExchangeMeeting/',
         ConfirmAcceptExchangeMeeting.as_view(),
         name="confirmacceptexchangemeeting"
         ),
]
