from django.http import JsonResponse
from django.views import View
from bangazonapi.models import Customer, Favorite
from rest_framework import viewsets
from rest_framework.response import Response
import json

class FavoritesReportViewSet(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        # Assuming you want to filter by a customer ID passed in the query params
        customer_id = self.request.query_params.get('customer', None)
        if not customer_id:
            return Response({"error": "Customer ID is required"}, status=400)

        try:
            customer = Customer.objects.get(id=int(customer_id))
        except (ValueError, Customer.DoesNotExist):
            return Response({"error": "Invalid customer ID"}, status=400)

        # Fetch and prepare the report data
        favorites = Favorite.objects.filter(customer=customer)
        report_data = {
            "customer_name": f"{customer.user.first_name} {customer.user.last_name}",
            "favorites": [{"seller_name": f"{fav.seller.user.first_name} {fav.seller.user.last_name}"} for fav in favorites]
        }

        return Response(report_data)