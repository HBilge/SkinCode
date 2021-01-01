from django.test import SimpleTestCase
from django.urls import reverse, resolve
from prediction.views import *


class TestUrls(SimpleTestCase):

    def test_cancertypes_url(self):
        url = reverse("cancertypes")
        self.assertEquals(resolve(url).func, cancertypes)

    def test_skincancer_url(self):
        url = reverse("skincancer")
        self.assertEquals(resolve(url).func, skincancer)

    def test_doctors_url(self):
        url = reverse("doctors")
        self.assertEquals(resolve(url).func, doctors)

    def test_system_url(self):
        url = reverse("system")
        self.assertEquals(resolve(url).func, system)

    def test_about_url(self):
        url = reverse("about")
        self.assertEquals(resolve(url).func, about)

    def test_view_profile_url(self):
        url = reverse("view_profile")
        self.assertEquals(resolve(url).func, view_profile)

    def test_predict_url(self):
        url = reverse("predict")
        self.assertEquals(resolve(url).func, predict)

    def test_image_upload_url(self):
        url = reverse("image_upload")
        self.assertEquals(resolve(url).func, image_upload)

    def test_home_url(self):
        url = reverse("home")
        self.assertEquals(resolve(url).func, home)

    def test_register_url(self):
        url = reverse("register")
        self.assertEquals(resolve(url).func, registerUser)

    def test_login_url(self):
        url = reverse("login")
        self.assertEquals(resolve(url).func, loginUser)

    def test_logout_url(self):
        url = reverse("logout")
        self.assertEquals(resolve(url).func, logoutUser)


