# suporte/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.suporte_home, name='suporte_home'),  # ou outra view
]
