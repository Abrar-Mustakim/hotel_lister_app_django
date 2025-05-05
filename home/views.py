from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.db.models import Q

# Create your views here.

@login_required
def update_theme(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_theme = data.get('theme')

        profile = request.user.profile  # or request.user.userprofile if you didn’t set related_name
        profile.theme_preference = new_theme
        profile.save()
        return JsonResponse({'status': 'success', 'theme': new_theme})
    return JsonResponse({'status': 'failed'}, status=400)


def home(request):
    query = request.GET.get('q', '')
    star_rating = request.GET.get('star_rating')
    amenity = request.GET.get('amenity')

    hotels = Hotel.objects.all()

    if query:
        hotels = hotels.filter(Q(hotel_name__icontains=query) | Q(location__icontains=query))

    if star_rating:
        hotels = hotels.filter(star_rating=star_rating)

    if amenity:
        hotels = hotels.filter(amenities__name__icontains=amenity)

    # Optional: Get first image
    for hotel in hotels:
        hotel.image = hotel.images.first() if hotel.images.exists() else None

    amenities = Amenity.objects.all()

    return render(request, 'home.html', {
        'hotels': hotels,
        'query': query,
        'star_rating': star_rating,
        'amenity': amenity,
        'amenities': amenities,
    })



def login_view(request):
    return render(request, 'login.html')

def register_view(request):
    return render(request, 'register.html')


def profile(request):
    return render(request, 'profile.html')