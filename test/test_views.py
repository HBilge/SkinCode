from django.test import Client
from django.urls import reverse
import unittest


from pymongo import MongoClient
cluster = MongoClient("mongodb+srv://skincodeuser:skincodepassword@cluster0.0lzc9.mongodb.net/skincodedb?retryWrites=true&w=majority")
db = cluster["skincode"]
collection = db["auth_user"]




class TestMethods(unittest.TestCase):

    def setUp(self):
        self.client = Client()
        self.username="BilgeHicyilmam"
        self.password = "bilge123456"
        login = self.client.login(username=self.username, password=self.password)
        self.assertEqual(login, True)

    def test_about_GET(self):
        response = self.client.get(reverse("about"))
        self.assertEquals(response.status_code, 200)

    def test_cancertypes_GET(self):
        response = self.client.get(reverse("cancertypes"))
        self.assertEquals(response.status_code, 200)

    def test_skincancer_GET(self):
        response = self.client.get(reverse("skincancer"))
        self.assertEquals(response.status_code, 200)

    def test_system_GET(self):
        response = self.client.get(reverse("system"))
        self.assertEquals(response.status_code, 200)

    def test_image_upload_GET(self):
        response = self.client.get(reverse("image_upload"))
        self.assertEquals(response.status_code, 200)

    def test_doctors_GET(self):
        response = self.client.get(reverse("doctors"))
        self.assertEquals(response.status_code, 200)

    def test_image_upload_url(self):
        response = self.client.get(reverse("image_upload"))
        self.assertEquals(response.status_code, 200)

    def test_home_GET(self):
        response = self.client.get(reverse("home"))
        self.assertEquals(response.status_code, 200)

    def test_view_profile_GET(self):
        response = self.client.get(reverse("view_profile"))
        self.assertEquals(response.status_code, 200)


# python manage.py test test.test_views