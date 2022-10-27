from itertools import product
from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F
from store.models import Product
# Create your views here.
# request -> response 
# request handler
# action


# we can return http resonse as well as rednering a templates
def say_hello(request):
 # try :
  # query_set = Product.objects.all() 
  # for product in query_set:
  #   print(product) 
  # product = Product.objects.get(pk=1) 
  # get return an object , not a queryset
  #complexe queyr , query_set.filter().filter.order_by()
  # the query set are lazy becaus they are evaleted later on,

  # count reutn number not query set , managers = poduct.object
 # "except ObjectDoesNotExist:
  #  pass
  product = Product.objects.filter(pk=0).exists()
  return render(request, 'hello.html')