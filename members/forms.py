from django import forms
from .models import ExchangeMeeting


class EchangeMeetingForm(forms.Form):
    """
    That form class to call a demand of change meeting
    """
    call_meeting = forms.DateField(label='call_metting')
    groupe = forms.CharField(max_length=20)
    free_date1 = forms.DateField()
    free_date2 = forms.DateField()
    free_date3 = forms.DateField()
    # class Meta:
    #     model = ExchangeMeeting
    #     fields = ['caller_id','caller_mmeting']

  

    # def save(self, commit=True):
        
    #     # make_password to hashe the password
    #     user.password = make_password(self.cleaned_data['password1'])
    #     if commit:
    #         user.save()
    #     return user
