# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from bangazonapi.models import ProductRating
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.parsers import JSONParser
# from bangazonapi.models import Product
# from rest_framework import status

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def rate_product(request, product_id):
#     """
#     Rate a product.
#     """
#     # Ensure 'product_id' is part of the URL.

#     try:
#         data = JSONParser().parse(request)
#         score = data['score']
#         review = data['review']
#         product_id = int(product_id)  # Extracted from URL
        
#         customer_id = request.user.id  # Assuming the user model is related to Customer model
#         product = Product.objects.get(pk=product_id)
        
#         ProductRating.objects.create(score=score, review=review, customer_id=customer_id, product_id=product_id)
#         return Response({"message": "Rating successfully added."}, status.HTTP_201_CREATED)
#     except Exception as e:
#         return Response({"error": str(e)}, status.HTTP_400_BAD_REQUEST)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from bangazonapi.models import ProductRating, Product
from rest_framework.parsers import JSONParser
from rest_framework.authentication import TokenAuthentication

class RateProduct(APIView):
    """
    Rate a product.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id, format=None):
        try:
            data = JSONParser().parse(request)
            score = data['score']
            review = data['review']
            
            product = Product.objects.get(pk=product_id)
            
            ProductRating.objects.create(score=score, review=review, customer_id=request.user.id, product_id=product_id)
            return Response({"message": "Rating successfully added."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)