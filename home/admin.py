from django.contrib import admin
from .models import * 
# Register your models here.
admin.site.register(Hotel)
admin.site.register(Amenity)
admin.site.register(HotelImage)
admin.site.register(HotelBookmark)