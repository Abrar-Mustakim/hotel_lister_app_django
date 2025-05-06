import json
import os
from django.core.management.base import BaseCommand
from home.models import Hotel, Amenity, HotelImage
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

class Command(BaseCommand):
    help = "Load hotel data from JSON file"

    def handle(self, *args, **kwargs):
        # Define the path to the JSON file
        json_file_path = os.path.join(settings.BASE_DIR, 'home', 'data', 'hotels_data.json')

        try:
            with open(json_file_path, 'r') as file:
                data = json.load(file)

            # Load amenities
            for amenity_data in data['amenities']:
                amenity, created = Amenity.objects.get_or_create(name=amenity_data['name'])
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created amenity: {amenity.name}"))
                else:
                    self.stdout.write(f"Amenity already exists: {amenity.name}")

            # Load hotels
            for hotel_data in data['hotels']:
                hotel_name = hotel_data['hotel_name']

                # Skip if hotel already exists
                if Hotel.objects.filter(hotel_name=hotel_name).exists():
                    self.stdout.write(f"Hotel already exists: {hotel_name}")
                    continue

                # Prepare amenity list
                amenities = []
                for amenity_name in hotel_data['amenities']:
                    try:
                        amenity = Amenity.objects.get(name=amenity_name)
                        amenities.append(amenity)
                    except ObjectDoesNotExist:
                        self.stdout.write(self.style.ERROR(f"Amenity '{amenity_name}' not found"))
                        continue

                # Create hotel
                hotel = Hotel.objects.create(
                    hotel_name=hotel_name,
                    description=hotel_data['description'],
                    price=hotel_data['price'],
                    star_rating=hotel_data['star_rating'],
                    location=hotel_data['location'],
                    room_count=hotel_data['room_count']
                )
                hotel.amenities.set(amenities)

                # Add images
                for image_filename in hotel_data['images']:
                    image_path = f'hotels/{image_filename}'

                    # Check if image already exists for this hotel
                    if HotelImage.objects.filter(hotel=hotel, image=image_path).exists():
                        self.stdout.write(f"Image already exists for hotel: {hotel_name}")
                        continue

                    image = HotelImage(hotel=hotel, image=image_path)
                    image.save()
                    self.stdout.write(self.style.SUCCESS(f"Added image for hotel: {hotel_name}"))
                
                self.stdout.write(self.style.SUCCESS(f"Created hotel: {hotel_name}"))
        
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("The hotels_data.json file was not found."))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR("Error decoding the JSON file."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))
