from django.contrib import admin

# Register your models here.
from .models import Question
class QuestionAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'question_text']


from .models import Windforecast
class WindforecastAdmin(admin.ModelAdmin):
    fields = ['runtime', 'forecast_time','wind_max', 'wind_average', 'wind_angle']

    actions = ['download_csv']
    def download_csv(self, request, queryset):
	    import csv
	    from django.http import HttpResponse
	    import io


	    f = io.StringIO()
	    writer = csv.writer(f)
	    writer.writerow(["runtime", "forecast_time", "wind_average", "wind_max", 'wind_angle'])

	    for s in queryset:
	        writer.writerow([s.runtime, s.forecast_time, s.wind_average, s.wind_max, s.wind_angle])

	    f.seek(0)
	    response = HttpResponse(f, content_type='text/csv')
	    response['Content-Disposition'] = 'attachment; filename=windforecast.csv'
	    return response
    download_csv.short_description = "Download CSV"



from .models import WindMeasurement
class WindMeasurementAdmin(admin.ModelAdmin):
	fields = ['runtime', 'wind_max', 'wind_average']
	actions = ['download_csv']
	def download_csv(self, request, queryset):
	    import csv
	    from django.http import HttpResponse
	    import io


	    f = io.StringIO()
	    writer = csv.writer(f)
	    writer.writerow(["runtime", "wind_average", "wind_max","wind_angle"])

	    for s in queryset:
	        writer.writerow([s.runtime, s.wind_average, s.wind_max])

	    f.seek(0)
	    response = HttpResponse(f, content_type='text/csv')
	    response['Content-Disposition'] = 'attachment; filename=windmeasurement.csv'
	    return response
	download_csv.short_description = "Download CSV file for selected stats."






admin.site.register(WindMeasurement, WindMeasurementAdmin)
admin.site.register(Windforecast, WindforecastAdmin)
admin.site.register(Question, QuestionAdmin)