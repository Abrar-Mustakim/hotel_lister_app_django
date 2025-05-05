from django.db import models
from django.contrib.auth.models import User
import uuid

# Base model with UUID and timestamps
class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# Amenity model (e.g., "Pool", "Free WiFi")
class Amenity(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Hotel model
class Hotel(BaseModel):
    hotel_name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    star_rating = models.IntegerField(choices=[(i, f"{i} Star") for i in range(1, 6)])
    location = models.CharField(max_length=100)
    amenities = models.ManyToManyField(Amenity, related_name="hotels")
    room_count = models.IntegerField(default=10)

    def __str__(self):
        return self.hotel_name

# Hotel Images
class HotelImage(BaseModel):
    hotel = models.ForeignKey(Hotel, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='hotels/')

# Hotel Booking
class HotelBooking(BaseModel):
    hotel = models.ForeignKey(Hotel, related_name="bookings", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="bookings", on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    booking_type = models.CharField(max_length=20, choices=[('Pre Paid', 'Pre Paid'), ('Post Paid', 'Post Paid')])

    def __str__(self):
        return f"{self.user.username} booked {self.hotel.hotel_name}"

# Hotel Bookmarking (Favorites)
class HotelBookmark(BaseModel):
    user = models.ForeignKey(User, related_name="bookmarks", on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, related_name="bookmarked_by", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'hotel')

    def __str__(self):
        return f"{self.user.username} bookmarked {self.hotel.hotel_name}"
