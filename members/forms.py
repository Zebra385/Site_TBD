from django import forms
from members.models import CalendarMeeting, Meeting
import datetime
from datetime import date


class DateSelectorWidget(forms.MultiWidget):
    """
    def a widget to choice a date par day month and year
    """
    def __init__(self, attrs=None):
        days = [(day, day) for day in range(1, 32)]
        months = [(month, month) for month in range(1, 13)]
        years = [(year, year) for year in [2021, 2022]]
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
        # créer le calendrier
        calendar = []
        calendar_all = CalendarMeeting.objects.all().order_by('date')
        for day in calendar_all:
            calendar.append(day.date)
        # calendar = list(calendar.date)
        # print('le calendar est : ', calendar)
        call_meeting = cleaned_data.get("call_meeting")

        free_date1 = cleaned_data.get("free_date1")
        free_date2 = cleaned_data.get("free_date2")
        free_date3 = cleaned_data.get("free_date3")

        if call_meeting not in calendar:
            msg = "Votre date de séance n\'existe pas!"
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
        elif free_date1 == datetime.date(2021, 1, 1):
            msg = "Vous devez entrer au moins la première date"
            self.add_error('free_date1', msg)
