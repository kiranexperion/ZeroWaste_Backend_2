# from django.test import TestCase

# from rest_framework.test import APITestCase
# from rest_framework import status

# class TestWastes(APITestCase):
    
#     def test_waste_create(self):
#         waste_data = {
#             "waste_type":"paper",
#             "charge":25
#         }
#         response = self.client.post("corporation/addwaste/",waste_data)
#         print("response", response.status_code)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)