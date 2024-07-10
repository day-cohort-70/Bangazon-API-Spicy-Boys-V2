from django.views.generic import ListView, TemplateView
from bangazonapi.models import Customer, Favorite, Product
from rest_framework import viewsets
from rest_framework.response import Response

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
    template_name = 'reports/favoritesellers.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer_id = self.request.GET.get('customer')
        
        if not customer_id:
            context['error'] = "Customer ID is required"
            return context

        try:
            customer = Customer.objects.get(id=int(customer_id))
            favorites = Favorite.objects.filter(customer=customer)
            context['customer_name'] = f"{customer.user.first_name} {customer.user.last_name}"
            context['favorites'] = [{"seller_name": f"{fav.seller.user.first_name} {fav.seller.user.last_name}"} for fav in favorites]
        except (ValueError, Customer.DoesNotExist):
            context['error'] = "Invalid customer ID"

        return context

class ProductListView(ListView):
    model = Product
    context_object_name = 'products'

    def get_queryset(self):
        price_threshold = 999
        if self.price_filter == 'expensive':
            return Product.objects.filter(price__gt=price_threshold)
        else:
            return Product.objects.filter(price__lte=price_threshold)

class InexpensiveProductsView(ProductListView):
    template_name = 'inexpensive_products.html'
    price_filter = 'inexpensive'

class ExpensiveProductsView(ProductListView):
    template_name = 'expensive_products.html'
    price_filter = 'expensive'