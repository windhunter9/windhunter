from django.db import models
from django.utils import timezone
import datetime
# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
    	return self.question_text
    def was_published_recently(self):
    	now = timezone.now()
    	return now - datetime.timedelta(days = 1) <= self.pub_date <= now

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
    	return self.choice_text


class Windforecast(models.Model):
    id = models.AutoField(primary_key=True)
    forecast_time = models.DateTimeField()
    runtime = models.DateTimeField()
    wind_max = models.FloatField()
    wind_average = models.FloatField()
    wind_angle = models.FloatField()
    class Meta:
        unique_together = (("forecast_time", "runtime"),)



class WindMeasurement(models.Model):
    id = models.AutoField(primary_key=True)
    runtime = models.DateTimeField(unique = True)
    wind_max = models.FloatField()
    wind_average = models.FloatField()

