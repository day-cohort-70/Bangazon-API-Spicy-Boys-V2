from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .favorite import Favorite


class Customer(models.Model):

    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=55)
    #store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True, related_name='owner')

    @property
    def recommends(self):
        return self.__recommends

    @recommends.setter
    def recommends(self, value):
        self.__recommends = value

    @property
    def recommended(self):
        return self.__recommended

    @recommended.setter
    def recommended(self, value):
        self.__recommended = value


    def generate_favorites_report(self, customer_id):
        # Fetch the customer's details
        customer = get_object_or_404(Customer, pk=customer_id)
        
        # Fetch all sellers favorited by this customer
        favorites = Favorite.objects.filter(customer=customer)
        
        # Prepare the report data
        report_data = {
            "customer_name": customer.user.first_name + " " + customer.user.last_name,
            "favorites": []
        }
        
        for favorite in favorites:
            # Assuming the Favorite model has a foreign key to a Seller model
            seller = favorite.seller
            report_data["favorites"].append({
                "seller_name": seller.user.first_name + " " + seller.user.last_name,
                "seller_details": str(seller)  # Assuming __str__ method is implemented in the Seller model
            })
        
        return report_data