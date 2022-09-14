from django.db import models
from django.conf import settings

DICTIONNARY_MEETING = (
    ["Mardi", "14h00-17h00", 3],
    ["Mardi", "19h30-22h00", 3.5],
    ["Mercredi", "19h30-22h00", 2.5],
    ["Jeudi", "09h30-12h30", 3],
    ["Jeudi", "13h30-16h30", 3],
)


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
        return self.date.isoformat()

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
    date_meeting = models.ForeignKey(CalendarMeeting,
                                     on_delete=models.CASCADE
                                     )

    def __str__(self):
        return u'{0}'.format(self.date_meeting.date)

    class Meta:
        """
        That class to can choice a name of our database in  mode admin
        """
        verbose_name = "Calendrier Utilisateur"


class ExchangeMeeting(models.Model):
    """
    This class to load the  meetings of a customuser
    """
    caller = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='caller2',
                               null=True,
                               on_delete=models.CASCADE
                               )
    caller_meeting = models.ForeignKey(CalendarMeeting,
                                       related_name='caller2_meeting',
                                       null=True,
                                       on_delete=models.CASCADE
                                       )
    acceptor = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 related_name='acceptor2',
                                 null=True,
                                 on_delete=models.CASCADE
                                 )
    acceptor_meeting = models.ForeignKey(CalendarMeeting,
                                         related_name='acceptor2_meeting',
                                         null=True,
                                         on_delete=models.CASCADE
                                         )
    exchange_operational = models.BooleanField()

    def __str__(self):
        return u'{0}'.format(self.caller_meeting.date)

    class Meta:
        """
        That class to can choice a name of our database in  mode admin
        """
        verbose_name = "Echange séance"


class ListExchangeMeeting(models.Model):
    """
    This class to load the  meetings of a customuser
    we want to exchange a meeting
    """
    exchange_meeting = models.ForeignKey(ExchangeMeeting,
                                         on_delete=models.CASCADE
                                         )
    groupe_caller = models.ForeignKey(Meeting,
                               related_name='groupe1_caller', 
                               on_delete=models.CASCADE,
                               null=True
                               )                                                
    date_meeting1 = models.ForeignKey(CalendarMeeting,
                                      related_name='date2_meeting1',
                                      blank=True,
                                      on_delete=models.CASCADE
                                      )
    date_meeting2 = models.ForeignKey(CalendarMeeting,
                                      related_name='date2_meeting2',
                                      blank=True, null=True,
                                      on_delete=models.CASCADE
                                      )
    date_meeting3 = models.ForeignKey(CalendarMeeting,
                                      related_name='date2_meeting3',
                                      blank=True,
                                      null=True,
                                      on_delete=models.CASCADE
                                      )
    groupe = models.ForeignKey(Meeting,
                               related_name='groupe2_accepter', 
                               on_delete=models.CASCADE,
                               null=True
                               )

    class Meta:
        """
        That class to can choice a name of our database in  mode admin
        """
        verbose_name = "List Echange séance"
