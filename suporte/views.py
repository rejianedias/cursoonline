from django.shortcuts import render

# suporte/views.py
from django.http import HttpResponse

def suporte_home(request):
    return HttpResponse("Página de suporte")


# Create your views here.
