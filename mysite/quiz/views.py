from django.shortcuts import render
# quiz/views.py
from django.http import HttpResponse

def index(request):
    return HttpResponse("Olá, esta é a página de quiz!")


# Create your views here.
