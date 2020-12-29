from django.contrib import admin
from .models import Meeting, Gang, CalendarMeeting, CalendarCustomuser,  ExchangeMeeting, ListExchangeMeeting

# Register your models here.


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    pass


@admin.register(Gang)
class GangAdmin(admin.ModelAdmin):
    pass


@admin.register(CalendarMeeting)
class CalendarMeetingAdmin(admin.ModelAdmin):
    pass


@admin.register(CalendarCustomuser)
class CalendarCustomuserAdmin(admin.ModelAdmin):
    pass


@admin.register(ExchangeMeeting)
class ExchangeMeetingAdmin(admin.ModelAdmin):
    pass


@admin.register(ListExchangeMeeting)
class ListExchangeMeetingAdmin(admin.ModelAdmin):
    pass