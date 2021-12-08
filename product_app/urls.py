from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'product_app'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('users/', GetUserView.as_view(), name='users'),
    path('countries/', GetCountriesList.as_view(), name='countries'),
    path('sales/', SalesView.as_view(), name='sales'),
    path('sale_statistics/', SaleStatistics.as_view(), name='sale_statistics'),
    path('upload_country_data/', UploadCountryData.as_view(), name='upload_country_data'),  # for adding country/city
    path('upload_sales/', UploadProductSaleData.as_view(), name='upload_sales'),
]
