from django.shortcuts import render

def home(request):
    return render(request, 'main/home.html')

def football(request):
    return render(request, 'main/football.html')

def hockey(request):
    return render(request, 'main/hockey.html')

def basketball(request):
    return render(request, 'main/basketball.html')