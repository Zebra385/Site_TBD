from django import forms
from members.models import CalendarMeeting, Meeting, CalendarCustomuser, ExchangeMeeting
import datetime
from datetime import date
from accounts.models import CustomUser


class DateSelectorWidget(forms.MultiWidget):
    """
    def a widget to choice a date par day month and year
    """
    def __init__(self, attrs=None):
        days = [(day, day) for day in range(1, 32)]
        months = [(month, month) for month in range(1, 13)]
        years = [(year, year) for year in [2022, 2023]]
        widgets = [
            forms.Select(attrs=attrs, choices=days),
            forms.Select(attrs=attrs, choices=months),
            forms.Select(attrs=attrs, choices=years),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if isinstance(value, date):
            return [value.day, value.month, value.year]
        elif isinstance(value, str):
            year, month, day = value.split('-')
            return [day, month, year]
        return [None, None, None]

    def value_from_datadict(self, data, files, name):
        day, month, year = super().value_from_datadict(data, files, name)
        # DateField expects a single string that it can parse into a date.
        return '{}-{}-{}'.format(year, month, day)


class ExchangeMeetingForm(forms.Form):
    """
    That form class to call a demand of change meeting
    """
    auth_user = forms.CharField(max_length=12,
                                widget=forms.TextInput(
                                    attrs={'size': '10'}
                                    )
                                )
    call_meeting = forms.DateField(label='Séance du demandeur',
                                   widget=DateSelectorWidget
                                   )
    groupe = forms.ModelChoiceField(Meeting.objects.all(),
                                    empty_label="---  Choisir un jour  ---"
                                    )
    free_date1 = forms.DateField(label='Première date de libre',
                                 widget=DateSelectorWidget
                                 )
    free_date2 = forms.DateField(label='Deuxième date de libre',
                                 widget=DateSelectorWidget,
                                 required=False
                                 )
    free_date3 = forms.DateField(label='Troisième date de libre',
                                 widget=DateSelectorWidget,
                                 required=False
                                 )

    def clean(self):
        cleaned_data = super().clean()
        auth_user = cleaned_data.get("auth_user")
        auth_user = CustomUser.objects.get(username=auth_user)
        call_meeting = cleaned_data.get("call_meeting")
        print('l utilisateur est ', auth_user)
        # créer le calendrier
        calendar = []
        calendar_all = CalendarMeeting.objects.all().order_by('date')
        for day in calendar_all:
            calendar.append(day.date)
        calendar_user = list(
            CalendarCustomuser.objects.filter(
                auth_user_id=auth_user
                ).order_by('date_meeting')
                )
        good_date = False
        call_meeting_str = call_meeting.strftime('%Y-%m-%d')
        for date in calendar_user:
            if call_meeting_str == str(date):
                good_date = True
        calendar_exchange_user = list(ExchangeMeeting.objects.filter(
                caller=auth_user, exchange_operational=False
                ).order_by('caller_meeting')
            )
        exist_date = False
        for date in calendar_exchange_user:
            if call_meeting_str == str(date):
                exist_date = True
        free_date1 = cleaned_data.get("free_date1")
        free_date2 = cleaned_data.get("free_date2")
        free_date3 = cleaned_data.get("free_date3")
        if call_meeting not in calendar:
            msg = "Votre date de séance n\'existe pas! dans le calendrier"
            self.add_error('call_meeting', msg)
        elif good_date is False:
            msg = "cette date n\'existe pas dans votre calendrier des séances"
            self.add_error('call_meeting', msg)
        elif exist_date is True:
            msg = "Vous avez dèjà fait une demande d'échange pour cette date,"
            msg += "si vous voulait changer votre demande il faut d\'abord annuler la précédente"
            self.add_error('call_meeting', msg)
        elif free_date1 not in calendar:
            msg = "Cette date de séance n\'existe pas!"
            self.add_error('free_date1', msg)
        elif free_date2 not in calendar:
            msg = "Cette date de séance n\'existe pas!"
            self.add_error('free_date2', msg)
        elif free_date3 not in calendar:
            msg = "Cette date de séance n\'existe pas!"
            self.add_error('free_date3', msg)
        elif free_date1 == datetime.date(2022, 1, 1):
            msg = "Vous devez entrer au moins la première date"
            self.add_error('free_date1', msg)
