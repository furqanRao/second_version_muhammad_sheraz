from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import *
from rest_framework.test import APITestCase


class LoginTestCase(APITestCase):

    def setUp(self):
        self.data = {
            "email": "employee",
            "password": "very-strong-pass"
        }
        self.new_user_data = {
            "username": "new_employee",
            "password": "very-strong-pass"
        }
        self.wrong_data = {
            "email": "employee",
            "password": "weak-pass"
        }
        # create user
        self.employee = User.objects.create_user(username="employee", password="very-strong-pass")
        self.token = Token.objects.create(user=self.employee)

    # in case of successful login
    def test_login_view(self):
        response = self.client.post("/api/v1/login/", self.data)
        self.assertEqual(response.data['status'], 200)

    # in case of login fail because credentials are incorrect
    def test_can_not_login_view(self):
        response = self.client.post("/api/v1/login/", self.wrong_data)
        self.assertEqual(response.data['status'], 404)

    # in case of valid logout
    def test_logout_view(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get("/api/v1/logout/", {})
        self.assertEqual(response.data['status'], 200)

    # in case of invalid logout
    def test_can_not_logout_view(self):
        response = self.client.post("/api/v1/logout/", self.data)
        self.assertEqual(response.status_code, 401)


class SalesDataTestCase(APITestCase):

    def setUp(self):
        # create user and token
        self.user = User.objects.create_user(username="employee", password="very-strong-pass")
        self.user_profile = UserProfile.objects.create(user=self.user, )
        self.token = Token.objects.create(user=self.user)
        self.user_id = {"id": 1}
        self.update_user_data = {
            "id": self.user_profile.id,
            "email": "changed_emp@gmail.com",
            "first_name": "Administrator",
            "last_name": "User",
            "gender": "Female",
            "age": 30,
            "country": "UK",
            "city": "LONDON"
        }
        self.sales = ProductData.objects.create(user_id=1, product="test product", sales_number=45,
                                                revenue=5.23, date=str(date.today()))
        self.get_sale = {"id": 1}
        self.create_sale_data = {
            "product": "Bulldog clip",
            "revenue": "0.10",
            "sales_number": 5,
            "date": "2010-02-02",
            "user": 1
        }
        self.update_sale_data = {
            "id": 1,
            "product": "Bulldog clip",
            "revenue": "0.10",
            "sales_number": 5,
            "date": "2010-02-02",
            "user_id": 1
        }

    # get user
    def test_get_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get("/api/v1/users/", self.user_id)
        self.assertEqual(response.status_code, 200)

    # get user
    def test_patch_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.patch("/api/v1/users/", self.update_user_data)
        self.assertEqual(response.status_code, 200)

    # get countries
    def test_get_countries(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get("/api/v1/countries/", )
        self.assertEqual(response.status_code, 200)

    # get countries fail
    def test_get_countries_fail(self):
        response = self.client.get("/api/v1/countries/", )
        self.assertEqual(response.status_code, 401)

    # get sale data
    def test_get_sales(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get("/api/v1/sales/", self.get_sale)
        self.assertEqual(response.status_code, 200)

    # create sale data
    def test_create_sales(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.post("/api/v1/sales/", self.create_sale_data)
        self.assertEqual(response.status_code, 200)

    # update sale data
    def test_patch_sales(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.patch("/api/v1/sales/", self.update_sale_data)
        self.assertEqual(response.status_code, 200)

    # put sale data
    def test_put_sales(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.put("/api/v1/sales/", self.update_sale_data)
        self.assertEqual(response.status_code, 200)

    # delete sale data
    def test_delete_sales(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.delete("/api/v1/sales/", self.get_sale)
        self.assertEqual(response.status_code, 200)

    # get sale_statistics
    def test_sale_statistics(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get("/api/v1/sale_statistics/", )
        self.assertEqual(response.status_code, 200)

    # get fail sale_statistics
    def test_sale_statistics_fail(self):
        response = self.client.get("/api/v1/sale_statistics/", )
        self.assertEqual(response.status_code, 401)
