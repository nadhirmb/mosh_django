from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend


from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin,DestroyModelMixin
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import status

from .filters import ProductFilter
from .models import Cart, Collection, Product, OrderItem, Review, CartItem
from .serialisers import CartItemSerializer, CartSerializer, ProductSerialiser, CollectionSerializer, ReviewSerializer,AddCartItemSerializer, UpdateCartItemSerializer
# Create your views here.

class ProductViewSet(ModelViewSet):
  queryset = Product.objects.all()
  serializer_class = ProductSerialiser
  filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
 # filterset_fields=['collection_id']
  filterset_class = ProductFilter
  pagination_class = PageNumberPagination
  search_fields=['title', 'description']
  ordering_fields = ['unit_price', 'last_update']

  
  def get_serializer_context(self):
    return {'request', self.request}  
  
  def destroy(self, request, *args, **kwargs):
    if OrderItem.objects.filter(product_id=kwargs[pk]).count() >0:
      return Response({'error':'product cannot be deleted bye'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    return super().destroy(request, *args, **kwargs)

 
class CollectionViewSet(ModelViewSet):
  queryset = Collection.objects.annotate( 
    products_count = Count('products')).all()
  serializer_class = CollectionSerializer
  
  def delete(self, request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    if collection.products.count() > 0:
      return Response({'error': 'Collection cannot be deleted bi'})
    collection.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

  
class ReviewViewSet(ModelViewSet):
  serializer_class = ReviewSerializer

  def get_queryset(self):
    return Review.objects.filter(product_id = self.kwargs['product_pk'])

  def get_serializer_context(self):
    return {'product_id': self.kwargs['product_pk']}

class CartViewSet(CreateModelMixin, 
                  RetrieveModelMixin, 
                  DestroyModelMixin,
                  GenericViewSet):

  queryset= Cart.objects.prefetch_related('items__product').all()
  serializer_class = CartSerializer

class CartItemViewSet(ModelViewSet):
  http_method_names = ['get', 'post', 'patch', 'delete']
  def get_serializer_class(self): 
    if self.request.method == 'POST':
        return AddCartItemSerializer
    elif self.request.method == 'PATCH':
      return UpdateCartItemSerializer
    return CartItemSerializer
  
  def get_serializer_context(self):
    return {'cart_id':self.kwargs['cart_pk']}
  
  def get_queryset(self):
    return CartItem.objects\
          .filter(cart_id=self.kwargs['cart_pk'])\
          .select_related('product')

