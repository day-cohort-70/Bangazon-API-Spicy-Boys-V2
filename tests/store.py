import json
import datetime
from rest_framework import status
from rest_framework.test import APITestCase


class StoreTests(APITestCase):

    def setUp(self) -> None:

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
