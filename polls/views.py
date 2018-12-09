from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone


from .models import Windforecast, WindMeasurement
from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))



from django.http import HttpResponse
import io
import matplotlib.pyplot as plt
import numpy as np
import random 
import sys

from common.utils.screen_scraping.screen_scraping import *
from common.utils.screen_scraping.windfinder import *
from common.utils.screen_scraping.station_lippesee import *


def setPlt():
    numPts = 50
    x = [random.random() for n in range(numPts)]
    y = [random.random() for n in range(numPts)]
    sz = 2 ** (10*np.random.rand(numPts))
    plt.scatter(x, y, s=sz, alpha=0.5)

def pltToSvg():
    buf = io.BytesIO()
    plt.savefig('polls/static/polls/images/test.svg', format='svg', bbox_inches='tight')

    plt.savefig(buf, format='svg', bbox_inches='tight')

    s = buf.getvalue()
    buf.close()
    return s

import csv
from django.http import HttpResponse

def some_view(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    writer = csv.writer(response)
    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])

    return response



def showimage(request):
    #setPlt() # create the plot
    #svg = pltToSvg() # convert plot to SVG
    #plt.cla() # clean up plt so it can be re-used
    #tree = getHtmlData('https://www.windfinder.com/weatherforecast/lippesee_paderborn')
    #print(tree)

   # day1 = tree.xpath('//*[@id="frame"]/div/div[1]/section[1]/section[1]/div/div[1]/h4/text()')[0]
    #day1 = day1[day1.find(",")+2:]
    day1 = "assdf"
    df = GetSuperForecast_Windfinder()

    for index, row in df.iterrows():
        try:
            Windforecast.objects.create(wind_average = row['average'], 
                                        wind_max = row['max'],
                                        runtime = row['runtime'],
                                        forecast_time = row['forecast_time'],
                                        wind_angle = row['angle']
                                        )
        except:
            day1 += str(row['runtime']) +"\n\n"

    df = GetActualWind()
    for index, row in df.iterrows():
        try:
            WindMeasurement.objects.create(wind_average = row['average'], wind_max = row['max'], runtime = row['runtime'])
        except:
            day1 += str(row['runtime']) +"\n\n"

    return render(request,'polls/showimage.html', {'out': day1})

import requests
from lxml import html


def trash():
    df = GetSuperForecast_Windfinder()

    for index, row in df.iterrows():
        try:
            Windforecast.objects.create(wind_average = row['average'], wind_max = row['max'], runtime = row['runtime'], forecast_time = row['forecast_time'])
        except:
            day1 += str(row['runtime']) +"\n\n"
    return render(request,'polls/showimage.html', {'out': day1})

