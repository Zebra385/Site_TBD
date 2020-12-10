from django.db import models
from django.conf import settings
from datetime import date
import datetime

DICTIONNARY_MEETING = (
    ["Mardi","13h30-16h30",3],
    ["Mardi","19h30-22h00",3.5],
    ["Mercredi","19h30-22h00",2.5],
    ["Jeudi","09h00-12h00",3],
    ["Jeudi","13h30-16h30",3],
)
def day_list(list,number_day_week):
    """function to load the date per day of week and and by month"""
    day_list= []
    for day in list:
        day_week = date(int(day.date_meeting.date.year),int(day.date_meeting.date.month),int(day.date_meeting.date.day)).weekday()
        
        if day_week == number_day_week:
            day_list.append(day.date_meeting.date)
    return day_list

# Create your models here.
class Meeting(models.Model):
    """
    This class to load different meetings per week
    """
    day = models.CharField(max_length=15)
    time_slot = models.CharField(max_length=15)
    time = models.FloatField(max_length=2)

   

    class Meta:
        """
        That class to can choice a name of our database in  mode admin
        """
        verbose_name = "séance"


class Gang(models.Model):
    """
    This class to load the five gangs of association
    """
    auth_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        )
    meeting_id = models.ForeignKey(Meeting, on_delete=models.CASCADE)

   

    class Meta:
        """
        That class to can choice a name of our database in  mode admin
        """
        verbose_name = "groupe"


class CalendarMeeting(models.Model):
    """
    This class to load the calendar of all meetings in the year
    """
    date = models.DateField()


  

    class Meta:
        """
        That class to can choice a name of our database in  mode admin
        """
        verbose_name = "Calendrier Séances"

class CalendarCustomuser(models.Model):
    """
    This class to load the  meetings of a customuser
    """
    auth_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        )
    date_meeting = models.ForeignKey(CalendarMeeting, on_delete=models.CASCADE)

    

    class Meta:
        """
        That class to can choice a name of our database in  mode admin
        """
        verbose_name = "Calendrier Utilisateur"


class ExchangeMeeting(models.Model):
    """
    This class to load the  meetings of a customuser
    """
    caller_id = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='caller', blank=True)
    caller_meeting = models.ManyToManyField(CalendarMeeting, related_name='caller_meeting', blank=True)
    acceptor_id = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='acceptor', blank=True)
    acceptor_meeting = models.ManyToManyField(CalendarMeeting, related_name='acceptor_meeting', blank=True)
    exchange_operational = models.BooleanField()

    

    class Meta:
        """
        That class to can choice a name of our database in  mode admin
        """
        verbose_name = "Echange séance"

        