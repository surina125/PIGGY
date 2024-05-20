from django.urls import path
from . import views

app_name = 'profile'

urlpatterns = [
    path('user/<str:username>/', views.user_info, name='user-info'),
    path('recommend/<str:username>/', views.recommend, name='recommend'),
]
