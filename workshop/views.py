from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.http import HttpResponse
from members.models import CalendarMeeting
from members.create_calendar import calendar
from datetime import date

# Create your views here.




class AccueilView(ListView):
    """ That class to get the acceuil page"""
    template_name = "workshop/accueil.html"
    context_object_name = 'calendar_meeting_list'   # your own name for the list as a template variable
    model = CalendarMeeting
   
   

    def get_queryset(self):
        self.day_list = list(CalendarMeeting.objects.all().order_by('date'))
        self.calendar=calendar(self.day_list)
        # for date in self.calendar:
        #     print('self.calendar.date vaut:', date)
        #     print('self.calendar.date.day vaut:', date[0].month)
        return self.calendar
        # self.day_list = CalendarMeeting.objects.all().order_by('date')
        # for day in self.day_list:
        #     print(day.date)
        # # make a list by day of week with function day_list
        # # and make good list , it add a day 2021-09-09 to have five day by day of week    
        # self.tuesday_list = good_list(day_list(self.day_list,1))
        # self.wenesday_list = good_list(day_list(self.day_list,2))
        # self.thursday_list = good_list(day_list(self.day_list,3))
        # # make a new list to have all in the year by order tuesday, wenesdaay and thursday
        # self.regroup_list= regroup_list(self.tuesday_list, self.wenesday_list,self.thursday_list)
        # # separate list  by month to have  15 days per month
        # self.janary_list = month_list(self.regroup_list,0)
        # self.february_list = month_list(self.regroup_list,1)
        # self.mars_list = month_list(self.regroup_list,2)
        # self.april_list = month_list(self.regroup_list,3)
        # self.may_list = month_list(self.regroup_list,4)
        # self.jun_list = month_list(self.regroup_list,5)

       
        # return self.janary_list, self.february_list, self.mars_list, self.april_list, self.may_list , self.jun_list

    def get_context_data(self, **kwargs):
        kwargs['calendar'] = self.calendar
        kwargs['calendar_customuser'] = None
       
       

        return super(AccueilView, self).get_context_data(**kwargs)
    
    
class CoursView(TemplateView):
    """ That class to get the coursl page"""
    template_name = "workshop/cours.html"

    # def generate_PDF(request):
    #     file = open('reglement.pdf', "w+b")
    #     file.seek(0) 
    #     pdf = file.read()
    #     file.close() 
    #     return HttpResponse(pdf, 'worshop/pdf')

class StagesView(TemplateView):
    """ That class to get the stages page"""
    template_name = "workshop/stages.html"