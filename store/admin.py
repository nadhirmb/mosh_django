from django.db.models.aggregates import Count
from django.contrib import admin
from django.urls import reverse
from django.http import HttpRequest
from django.utils.html import format_html, urlencode
from . import models

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
  list_display = ['title' ,'unit_price', 'inventory_status', 'collection_title']
  list_editable = ['unit_price']
  list_per_page = 10
  list_select_related = ['collection']

  def collection_title(self, product):
    return product.collection.title

  @admin.display(ordering='inventory')
  def inventory_status(self, product):
    if product.inventory < 10:
      return 'Low'
    return 'OK'

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
  list_display = ['first_name' ,'last_name', 'membership']
  list_editable = ['membership']
  list_select_related = ['user']
  ordering = ['user__first_name','user__last_name']
  list_per_page = 10

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
  list_display = ['id', 'placed_at' ,'customer']
  list_per_page = 10


# Register your models here.
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin): 
  list_display = ['title', 'products_count']

  @admin.display(ordering = 'products_counts')
  def products_count(self, collection): 
    url =(
       reverse('admin:store_product_changelist') 
       + '?'
       + urlencode({
        'collection__id': str(collection.id)
       })) 
    return format_html('<a href="{}">{}</a>',url, collection.products_count)

  def get_queryset(self, request):
    return super().get_queryset(request).annotate(
      products_count = Count('products')
      )
