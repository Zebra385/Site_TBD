from django import forms
from django.forms import ModelForm
from .models import ExchangeMeeting
from members.models import CalendarCustomuser, CalendarMeeting, Gang, Meeting, ListExchangeMeeting, ExchangeMeeting
from accounts.models import CustomUser
from django.forms import ModelChoiceField
from datetime import date

# exchangemeeting=ExchangeMeeting1.objects.filter(exchange_operational=False)
# meeting=ListExchangeMeeting1.objects.get(exchange_meeting_id=exchangemeeting)
class DateSelectorWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        days = [(day, day) for day in range(1, 32)]
        months = [(month, month) for month in range(1, 13)]
        years = [(year, year) for year in [2020, 2021]]
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
    
    auth_user = forms.CharField(max_length=20)
    call_meeting = forms.DateField(widget=DateSelectorWidget)
    groupe = forms.ModelChoiceField(Meeting.objects.all(),to_field_name="day",empty_label="---  Choisir un jour  ---")
    free_date1 = forms.DateField(widget=DateSelectorWidget)
    free_date2 = forms.DateField(widget=DateSelectorWidget, required=False)
    free_date3 = forms.DateField(widget=DateSelectorWidget, required=False)
    
# class ListExchangeMeetingForm1(forms.Form,choice):
#     """
#     That form class to show and accept a exchange of meeting
#     """
#     days = forms.ChoiceField(Choices=choices)
#     # list_day = forms.ModelMultipleChoiceField(queryset=ListExchangeMeeting().objects.all(), to_field_name="date_meeting1", required=False, widget=forms.CheckboxSelectMultiple
#     # )