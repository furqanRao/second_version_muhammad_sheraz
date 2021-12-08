from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from django.db.models import Count
from django.db.models import Q
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .serializers import *
import traceback
import pandas as pd
from django.db.models import Avg, Max


class LoginView(APIView):

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not email or not password:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Username and Password are required!"
            })
        user = authenticate(username=email, password=password)
        if user:
            try:
                token, created = Token.objects.get_or_create(user=user)
                response = {
                    "status": status.HTTP_200_OK,
                    "token": token.key,
                    "user_id": token.user.id,
                }
            except:
                response = {
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": "Due to internal error we couldn't process your request, please try again later!"
                }
        else:
            response = {
                "status": status.HTTP_404_NOT_FOUND,
                "message": "User not found!"
            }
        return Response(response)


class Logout(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        try:
            Token.objects.filter(key=token).delete()
        except:
            print(traceback.print_exc())
        return Response({
            "status": status.HTTP_200_OK,
        })


class GetUserView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user_id = request.GET.get('id', None)
        if User.objects.filter(id=user_id):
            try:
                profile = UserProfile.objects.get(user_id=user_id)
            except:
                profile = UserProfile.objects.create(user_id=user_id)
            user = UserProfileSerializer(profile)
            return Response({
                "status": status.HTTP_200_OK,
                "response": user.data
            })
        else:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
            })

    def get_object(self, pk):
        return UserProfile.objects.get(user=User.objects.get(id=pk))

    def patch(self, request):
        model_object = self.get_object(request.data['id'])
        serializer = UserProfileSerializer(model_object, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": status.HTTP_200_OK,
                "response": serializer.data
            })
        return Response({
            "status": status.HTTP_404_NOT_FOUND,
        })


class GetCountriesList(ListCreateAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class SalesView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get_object(self, pk):
        return ProductData.objects.get(id=pk)

    def get(self, request):
        sale_id = request.GET.get('id', None)
        if ProductData.objects.filter(id=sale_id):
            product = ProductData.objects.get(id=sale_id)
            product_serializer = ProductDataSerializer(product)
            return Response({
                "status": status.HTTP_200_OK,
                "response": product_serializer.data
            })
        return Response({
            "status": status.HTTP_404_NOT_FOUND,
        })

    def post(self, request):
        try:
            serializer = ProductDataSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": status.HTTP_201_CREATED,
                    "response": serializer.data
                })
            else:
                return Response({
                    "status": status.HTTP_404_NOT_FOUND,
                })
        except:
            return Response({
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "response": "You need to pass these params [product, sales_number, revenue, date, user_id]"
            })

    def patch(self, request):
        sale_id = request.data.get('id', None)
        model_object = self.get_object(sale_id)
        serializer = ProductDataSerializer(model_object, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": status.HTTP_200_OK,
                "response": serializer.data
            })
        return Response({
            "status": status.HTTP_404_NOT_FOUND,
        })

    def put(self, request):
        sale_id = request.data.get('id', None)
        model_object = self.get_object(sale_id)
        serializer = ProductDataSerializer(model_object, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": status.HTTP_200_OK,
                "response": serializer.data
            })
        return Response({
            "status": status.HTTP_404_NOT_FOUND,
        })

    def delete(self, request):
        sale_id = request.data.get('id', None)
        model_object = self.get_object(sale_id)
        if model_object:
            model_object.delete()
            return Response({
                "status": status.HTTP_204_NO_CONTENT,
            })
        return Response({
            "status": status.HTTP_404_NOT_FOUND,
        })


class SaleStatistics(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        current_user = Token.objects.get(key=token).user
        products = ProductData.objects.all()
        current_user_products = products.filter(user=current_user)

        current_user_sales_average = current_user_products.aggregate(Avg('sales_number')).values()
        all_users_sales_average = products.aggregate(Avg('sales_number')).values()
        highest_revenue_sale_for_current_user = current_user_products.values('id', 'revenue').annotate(Max('revenue'))[0]
        product_highest_revenue_for_current_user = current_user_products.values('product', 'sales_number').annotate(Max('sales_number'))[0]
        product_highest_sales_number_for_current_user = current_user_products.values('product', 'sales_number').annotate(Max('sales_number'))[0]

        return Response({
            "status": status.HTTP_200_OK,
            "response": {
                "average_sales_for_current_user": current_user_sales_average,
                "average_sales_all_user": all_users_sales_average,
                "highest_revenue_sale_for_current_user": {"sale_id": highest_revenue_sale_for_current_user['id'],
                                                          "revenue": highest_revenue_sale_for_current_user['revenue']},
                "product_highest_revenue_for_current_user": {"product_name": product_highest_revenue_for_current_user['product'],
                                                             "price": product_highest_revenue_for_current_user['sales_number']},
                "product_highest_sales_number_for_current_user": {"product_name": product_highest_sales_number_for_current_user['product'],
                                                                  "price": product_highest_sales_number_for_current_user['sales_number']},
            }
        })


class UploadProductSaleData(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        file = request.data.get('file', None)
        user_id = request.data.get('user_id', None)
        if file and user_id:
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)
            file_columns = []
            required_columns = ['date', 'product', 'sales_number', 'revenue']
            for i in df:
                if "Unnamed:" not in i:
                    file_columns.append(i)
            objects = []
            for i in df.index:
                data_date = None
                product = None
                sales_number = None
                revenue = None
                for index in range(len(file_columns)):
                    if required_columns[index] == "date":
                        if str(df[file_columns[index]][i]) != "nan":
                            data_date = df[file_columns[index]][i]
                    if required_columns[index] == "product":
                        if str(df[file_columns[index]][i]) != "nan":
                            product = df[file_columns[index]][i]
                    if required_columns[index] == "sales_number":
                        if str(df[file_columns[index]][i]) != "nan":
                            sales_number = df[file_columns[index]][i]
                    if required_columns[index] == "revenue":
                        if str(df[file_columns[index]][i]) != "nan":
                            revenue = df[file_columns[index]][i]

                objects.append(ProductData(user_id=user_id, product=product, sales_number=sales_number,
                                           revenue=revenue, date=data_date))
            ProductData.objects.bulk_create(objects)

            return Response({
                "status": status.HTTP_200_OK,
            })
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
        })


# for creating country/city data one time
class UploadCountryData(APIView):
    # permission_classes = [IsAuthenticated, ]

    def post(self, request):
        file = request.data.get('file', None)
        df = pd.read_excel(file)
        ar = []
        x = ['fsdfsfsdw', 'City', 'Country', 'gsdfdsf']
        for i in df:
            if "Unnamed:" not in i:
                ar.append(i)
        for i in df.index:
            city = None
            country = None
            for index in range(len(ar)):
                if x[index] == "City":
                    if str(df[ar[index]][i]) != "nan":
                        city = df[ar[index]][i]
                if x[index] == "Country":
                    if str(df[ar[index]][i]) != "nan":
                        country = df[ar[index]][i]

            if city and country:
                if Country.objects.filter(name=country):
                    country_obj = Country.objects.get(name=country)
                    City.objects.create(country=country_obj, name=city)
                else:
                    country_obj = Country.objects.create(name=country)
                    City.objects.create(country=country_obj, name=city)

        return Response({
            "status": status.HTTP_200_OK,
        })
