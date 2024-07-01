from rest_framework.decorators import action
from bangazonapi.models.recommendation import Recommendation
import base64
from django.core.files.base import ContentFile
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import Store, Product
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
from .product import ProductSerializer


class StoreSerializer(serializers.ModelSerializer):
    """JSON serializer for stores"""
    products = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = ['id', 'name', 'description', 'customer_id', 'products']
    
    def get_products(self, obj):
        # Check for a query parameter like ?expand=products
        expand = self.context.get('request').query_params.get('expand')
        if expand == "products":
            products = Product.objects.filter(store=obj)
            return ProductSerializer(products, many=True).data
        return []
      

class StoresViewSet(ViewSet):
    """Request handlers for Stores in the Bangazon Platform"""
    permission_classes = (IsAuthenticatedOrReadOnly,)


    def list(self, request): 
        stores = Store.objects.all()
        serializer = StoreSerializer(
            stores, many=True, context={'request': request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        try:

            store = Store.objects.get(pk=pk)

            serializer = StoreSerializer(store, context={'request': request})
            return Response(serializer.data)

        except Store.DoesNotExist as ex:
            return Response(
                {'message': 'The requested store does not exist, or you do not have permission to access it.'},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as ex:
            return HttpResponseServerError(ex)