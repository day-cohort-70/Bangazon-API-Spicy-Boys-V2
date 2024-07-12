import json
import datetime
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from bangazonapi.models import Product


class ProductTests(APITestCase):
    def setUp(self) -> None:
        """
        Create a new account and create sample category
        """
        url = "/register"
        data = {
            "username": "steve",
            "password": "Admin8*",
            "email": "steve@stevebrownlee.com",
            "address": "100 Infinity Way",
            "phone_number": "555-1212",
            "first_name": "Steve",
            "last_name": "Brownlee",
        }
        response = self.client.post(url, data, format="json")
        json_response = json.loads(response.content)
        self.token = json_response["token"]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = "/stores"
        data = {"name": "Test", "description": "Test2", "customer_id": 1}
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

        response = self.client.post(url, data, format="json")
        json_response = json.loads(response.content)
        print(json_response)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["name"], "Test")
        self.assertEqual(json_response["description"], "Test2")
        self.assertEqual(json_response["customer_id"], 1)

        url = "/productcategories"
        data = {"name": "Sporting Goods"}
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

        response = self.client.post(url, data, format="json")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["name"], "Sporting Goods")

    def test_create_product(self):
        """
        Ensure we can create a new product.
        """

        url = "/products"
        data = {
            "name": "Kite",
            "price": 14.99,
            "quantity": 60,
            "description": "It flies high",
            "category_id": 1,
            "location": "Pittsburgh",
            "store_id": 1,
        }
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.post(url, data, format="json")
        json_response = json.loads(response.content)
        print(json_response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["name"], "Kite")
        self.assertEqual(json_response["price"], 14.99)
        self.assertEqual(json_response["quantity"], 60)
        self.assertEqual(json_response["description"], "It flies high")
        self.assertEqual(json_response["location"], "Pittsburgh")
        # self.assertEqual(json_response["store_id"], 1)
        # self.assertEqual(json_response["category_id"], 1)

    def test_update_product(self):
        """
        Ensure we can update a product.
        """
        self.test_create_product()

        url = "/products/1"
        data = {
            "name": "Kite",
            "price": 24.99,
            "quantity": 40,
            "description": "It flies very high",
            "category_id": 1,
            "created_date": datetime.date.today(),
            "location": "Pittsburgh",
        }
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(url, data, format="json")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["name"], "Kite")
        self.assertEqual(json_response["price"], 24.99)
        self.assertEqual(json_response["quantity"], 40)
        self.assertEqual(json_response["description"], "It flies very high")
        self.assertEqual(json_response["location"], "Pittsburgh")

    def test_get_all_products(self):
        """
        Ensure we can get a collection of products.
        """
        self.test_create_product()
        self.test_create_product()
        self.test_create_product()

        url = "/products"

        response = self.client.get(url, None, format="json")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json_response), 3)

    def test_delete_product(self):
        self.test_create_product()

        url = "/products/1"
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # TODO: Delete product

    # TODO: Product can be rated. Assert average rating exists.
    def test_product_can_be_rated_and_average_rating_exists(self):
        url = "/products"
        data = {
            "name": "Kite",
            "price": 14.99,
            "quantity": 60,
            "description": "It flies high",
            "category_id": 1,
            "location": "Pittsburgh",
            "store_id": 1,
        }
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.post(url, data, format="json")
        json_response = json.loads(response.content)
        print("Printing product....")
        print(json_response)


        rating_url = f"/products/1/rate-product"
        rating_data = {
            "score": 5,  # Changed from 'rating' to 'score'
            "review": "Great product!",

        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token) # Ensure authentication
        response = self.client.post(rating_url, rating_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Add second rating
        rating_data["score"] = 3
        response = self.client.post(rating_url, rating_data, format='json')
        if response.status_code == 201:
            json_response = json.loads(response.content)
        else:
            print(f"Unexpected status code: {response.status_code}")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Fetch the product to check its average rating
        product_detail_url = f"/products/1"  # Adjust 'product_detail' to match your endpoint for fetching a single product
        print(f"Product detail URL: {product_detail_url}")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.get(product_detail_url)
        print("Product response------------")
        print(response)
        print("------------")

        json_response = json.loads(response.content)
        print("Product JSON response------------")
        print(json_response)
        print("------------")

        self.assertIn('average_rating', json_response)
        self.assertAlmostEqual(float(json_response['average_rating']), 4.0, places=1)
           
           
            