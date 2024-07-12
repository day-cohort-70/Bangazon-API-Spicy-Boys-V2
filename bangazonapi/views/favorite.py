from rest_framework import viewsets, status
from rest_framework.response import Response
from bangazonapi.models import Favorite, Store, Customer  # Ensure this import matches your project structure
from .profile import FavoriteSerializer  # Ensure this import matches your project structure


class FavoritesViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing favorites.
    """

    serializer_class = FavoriteSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned favorites to a given user,
        by filtering against a `customer` query parameter in the URL.
        """
        queryset = Favorite.objects.all()
        customer = self.request.query_params.get('customer', None)
        if customer is not None:
            queryset = queryset.filter(customer__user__id=customer)
        return queryset

    def list(self, request, *args, **kwargs):
        """
        Handle GET requests for retrieving favorite entries.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        """
        Handle GET requests for retrieving a specific favorite entry.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        store_id = request.data.get('store_id')
        if store_id:
            try:
                store = Store.objects.get(pk=store_id)
                customer = Customer.objects.get(user=request.user)
                
                # Check if the favorite already exists
                existing_favorite = Favorite.objects.filter(customer=customer, store=store).first()
                if existing_favorite:
                    return Response({"detail": "This store is already in your favorites."}, status=status.HTTP_400_BAD_REQUEST)
                
                # Create new favorite
                favorite = Favorite.objects.create(customer=customer, store=store)
                serializer = self.get_serializer(favorite)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Store.DoesNotExist:
                return Response({"store_id": ["Store with this ID does not exist."]}, status=status.HTTP_400_BAD_REQUEST)
            except Customer.DoesNotExist:
                return Response({"detail": "Customer profile not found."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"store_id": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        """
        Handle PUT requests for updating a favorite entry.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, pk=None, *args, **kwargs):
        """
        Handle PATCH requests for partially updating a favorite entry.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        """
        Handle DELETE requests for removing a favorite entry.
        """
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)