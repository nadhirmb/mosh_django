from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
# request -> response 
# request handler
# action


# we can return http resonse as well as rednering a templates
def say_hello(request):
  return render(request, 'hello.html')