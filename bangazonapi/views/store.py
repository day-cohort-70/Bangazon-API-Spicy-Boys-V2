from rest_framework.decorators import action
from bangazonapi.models.recommendation import Recommendation
import base64
from django.core.files.base import ContentFile
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import Store
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser


class StoreSerializer(serializers.ModelSerializer):
    """JSON serializer for stores"""
    class Meta:
        model = Store
        fields = ['id', 'name', 'description', 'customer_id']
      

class StoresViewSet(ViewSet):
    """Request handlers for Stores in the Bangazon Platform"""
    permission_classes = (IsAuthenticatedOrReadOnly,)


    def list(self, request): 
        stores = Store.objects.all()
        serializer = StoreSerializer(
            stores, many=True, context={'request': request})
        return Response(serializer.data)