from django.http import JsonResponse, HttpResponseRedirect
from django.views import View
from bangazonapi.models import Customer, Favorite, Product
from rest_framework import viewsets
from rest_framework.response import Response
import json
from django.shortcuts import render
from django.views.generic import TemplateView
import requests
from urllib.parse import urlencode


class FavoritesReportViewSet(viewsets.ViewSet):
    def list(self, request):
        customer_id = request.query_params.get('customer')
        if not customer_id:
            return Response({"error": "Customer ID is required"}, status=400)

        try:
            customer = Customer.objects.get(id=int(customer_id))
        except (ValueError, Customer.DoesNotExist):
            return Response({"error": "Invalid customer ID"}, status=400)

        favorites = Favorite.objects.filter(customer=customer)
        report_data = {
            "customer_name": f"{customer.user.first_name} {customer.user.last_name}",
            "favorites": [{"seller_name": f"{fav.seller.user.first_name} {fav.seller.user.last_name}"} for fav in favorites]
        }
        return Response(report_data)


class FavoritesReportTemplateView(TemplateView):
    template_name = '../templates/reports/favoritesellers.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer_id = self.request.GET.get('customer')
        if not customer_id:
            context['error'] = "Customer ID is required"
            return context

        api_url = f"http://localhost:8000/reports/favoritesellers?customer={customer_id}"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            context['customer_name'] = data.get('customer_name', '')
            context['favorites'] = data.get('favorites', [])
        else:
            context['error'] = "Failed to fetch report."
        return context
    

class InexpensiveProductsView(View):
    def get(self, request):
        products = Product.objects.filter(price__lt=999)
        return render(request, 'inexpensive_products.html', {'products': products})
    
class ExpensiveProductsView(View):
    def get(self, request):
        products = Product.objects.filter(price__gt=999)
        return render(request, 'expensive_products.html', {'products': products})