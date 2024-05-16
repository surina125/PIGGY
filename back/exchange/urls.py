from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('exchange_info/',views.exchange_info)


]
