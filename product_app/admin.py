from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
admin.site.register(City)
admin.site.register(Country)
admin.site.register(ProductData)
