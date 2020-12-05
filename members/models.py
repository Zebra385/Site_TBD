from django.db import models
from django.conf import settings

DICTIONNARY_MEETING = (
    ["Mardi","13h30-16h30",3],
    ["Mardi","19h30-22h00",3.5],
    ["Mercredi","19h30-22h00",2.5],
    ["Jeudi","09h00-12h00",3],
    ["Jeudi","13h30-16h30",3],
)


# Create your models here.
class Meeting(models.Model):
    """
    This class to load different meetings per week
    """
    day = models.CharField(max_length=15)
    time_slot = models.CharField(max_length=15)
    time = models.FloatField(max_length=2)

    def __str__(self):
        return self.day + "-" + self.time_slot

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

    def __str__(self):
            return self.meeting_id

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


    def __str__(self):
            return self.date

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

    def __str__(self):
            return self.date_meeting

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

    def __str__(self):
            return self.caller_id

    class Meta:
        """
        That class to can choice a name of our database in  mode admin
        """
        verbose_name = "Echange séance"