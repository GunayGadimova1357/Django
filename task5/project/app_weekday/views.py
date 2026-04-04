from django.http import HttpResponse
import datetime

def weekday(request):
    today = datetime.datetime.now()
    day = today.strftime("%A")
    return HttpResponse(f"Today: {day}")
