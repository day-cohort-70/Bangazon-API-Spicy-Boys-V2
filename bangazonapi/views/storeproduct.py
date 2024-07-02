
from rest_framework import serializers
from bangazonapi.models import OrderProduct, Product
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'number_sold', 'description',
                  'quantity', 'created_date', 'location', 'image_path',
                  'average_rating', 'can_be_rated', 'category_id', 'store_id')

class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderProduct
        fields = ['id', 'order_id', 'product']


class OrderProductViewSet(ViewSet):
    """
    Retrieve orders for a specific store.
    """

    def list(self, request):
        print(request.query_params)
        store_id = self.request.query_params.get('store')
        if store_id is not None:
            order_products = OrderProduct.objects.filter(product__store_id=store_id)
            serializer = OrderProductSerializer(order_products, many=True)
            return Response(serializer.data)
        else:
            # Handle the case where store_id is None
            return Response({"error": "No store ID provided"}, status=400)