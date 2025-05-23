"""
URL configuration for hotel_lister_app_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns 
from home.views import * 

urlpatterns = [
    path('', home, name='home'),  # Home page
    path('profile/', profile, name='profile'),
    path('login/', login_view, name='login'),  # Login page
    path('bookmark/<uuid:hotel_id>/', bookmark_hotel, name='bookmark'),  # Add this URL for bookmarking
    path('unbookmark/<uuid:hotel_id>/', unbookmark_hotel, name='unbookmark'),
    path('hotel-detail/<uuid:hotel_id>/', hotel_detail, name='hotel_detail'),  # Hotel detail page
    path('register/', register_view, name='register'), 
    path('logout/', logout, name='logout'), 
    path('update-theme/', update_theme, name='update_theme'),
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns() 
