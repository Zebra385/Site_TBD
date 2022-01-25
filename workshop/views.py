from django.views.generic.base import TemplateView
from django.views.generic import ListView
from members.models import CalendarMeeting
from members.create_calendar import calendar


class AccueilView(ListView):
    """ That class to get the acceuil page"""
    template_name = "workshop/accueil.html"
    context_object_name = 'calendar_meeting_list'
    model = CalendarMeeting

    def get_queryset(self):
        self.day_list = list(CalendarMeeting.objects.all().order_by('date'))
        self.calendar = calendar(self.day_list)
        # test
        # for date in self.calendar:
        #     print('self.calendar.date vaut:', date)
            
        return self.calendar

    def get_context_data(self, **kwargs):
        kwargs['calendar'] = self.calendar
        kwargs['calendar_customuser'] = None
        return super(AccueilView, self).get_context_data(**kwargs)


class CoursView(TemplateView):
    """ That class to get the coursl page"""
    template_name = "workshop/cours.html"

class AnimateurView(TemplateView):
    """ That class to get the coursl page"""
    template_name = "workshop/animateur.html"


class StagesView(TemplateView):
    """ That class to get the stages page"""
    template_name = "workshop/stages.html"

class CopyrightView(TemplateView):
    """That class to give the url of all copyright use to build this site"""
    template_name = 'workshop/copyright.html'

class CookiesView(TemplateView):
    """That class to present the policiy of cookies"""
    template_name = 'workshop/cookie-policy.html'