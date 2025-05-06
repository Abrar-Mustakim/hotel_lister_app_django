from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth import logout as auth_logout
from django.core.paginator import Paginator

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


@login_required
def bookmark_hotel(request, hotel_id):
    hotel = Hotel.objects.get(uid=hotel_id)
    if not HotelBookmark.objects.filter(user=request.user, hotel=hotel).exists():
        HotelBookmark.objects.create(user=request.user, hotel=hotel)
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def unbookmark_hotel(request, hotel_id):
    hotel = Hotel.objects.get(uid=hotel_id)
    bookmark = HotelBookmark.objects.filter(user=request.user, hotel=hotel).first()
    if bookmark:
        bookmark.delete()
    return redirect(request.META.get('HTTP_REFERER', 'home'))


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

    # Optional: Add first image
    for hotel in hotels:
        hotel.image = hotel.images.first() if hotel.images.exists() else None

    # Add pagination (3 hotels per page)
    paginator = Paginator(hotels, 3)
    page_number = request.GET.get('page')
    hotels_page = paginator.get_page(page_number)

    amenities = Amenity.objects.all()

    bookmarked_hotels = []
    if request.user.is_authenticated:
        bookmarked_hotels = HotelBookmark.objects.filter(user=request.user).values_list('hotel__uid', flat=True)

    return render(request, 'home.html', {
        'hotels': hotels_page,  # paginated hotels
        'query': query,
        'star_rating': star_rating,
        'amenity': amenity,
        'amenities': amenities,
        'bookmarked_hotels': bookmarked_hotels,
    })



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')

    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        #UserProfile.objects.create(user=user)  # Create profile with default theme
        login(request, user)
        messages.success(request, "Registration successful.")
        return redirect('home')

    return render(request, 'register.html')


def logout(request): 
    auth_logout(request)
    return redirect('login')

@login_required
def profile(request):
    # Get HotelBookmark instances for the logged-in user
    bookmarks = HotelBookmark.objects.filter(user=request.user).select_related('hotel')

    # Extract the actual Hotel objects for easier template usage
    bookmarked_hotels = [bookmark.hotel for bookmark in bookmarks]

    return render(request, 'profile.html', {
        'user': request.user,
        'bookmarked_hotels': bookmarked_hotels,
    })


@login_required
def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, uid=hotel_id)
    images = hotel.images.all()
    reviews = HotelReview.objects.filter(hotel=hotel).select_related('user')

    if request.method == 'POST':
        rating = int(request.POST.get('rating', 0))
        comment = request.POST.get('comment', '')
        if rating and comment:
            HotelReview.objects.create(
                user=request.user,
                hotel=hotel,
                rating=rating,
                comment=comment
            )
            return redirect('hotel_detail', hotel_id=hotel_id)

    return render(request, 'hotel_detail.html', {
        'hotel': hotel,
        'images': images,
        'reviews': reviews
    })