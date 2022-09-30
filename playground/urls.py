from django.urls import path
from . import views


# URLConf , every app have one 
urlpatterns = [
  path('hello/', views.say_hello) ,
]