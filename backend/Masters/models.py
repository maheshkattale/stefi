from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class TravelCategory(models.Model):
    CATEGORY_TYPES = [
        ('bus', 'Bus'),
        ('train', 'Train'),
        ('car', 'Car'),
        ('flight', 'Flight'),
        ('cruise', 'Cruise'),
        ('bike', 'Bike'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    category_type = models.CharField(max_length=20, choices=CATEGORY_TYPES)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="FontAwesome icon class")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name_plural = "Travel Categories"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.get_category_type_display()})"

class State(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True, help_text="State code like MH, DL, etc.")
    country = models.CharField(max_length=100, default="India")
    capital = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='states/', null=True, blank=True)
    popular_destinations = models.TextField(blank=True, help_text="Comma separated popular destinations")
    best_time_to_visit = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name}, {self.country}"

class Destination(models.Model):
    DESTINATION_TYPES = [
        ('hill_station', 'Hill Station'),
        ('beach', 'Beach'),
        ('historical', 'Historical'),
        ('religious', 'Religious'),
        ('adventure', 'Adventure'),
        ('wildlife', 'Wildlife'),
        ('city', 'City'),
    ]
    
    name = models.CharField(max_length=200)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='destinations')
    destination_type = models.CharField(max_length=20, choices=DESTINATION_TYPES)
    description = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    best_time_to_visit = models.CharField(max_length=200, blank=True)
    average_temperature = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='destinations/', null=True, blank=True)
    is_popular = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['name']
        unique_together = ['name', 'state']
    
    def __str__(self):
        return f"{self.name}, {self.state.name}"

class TravelAgency(models.Model):
    AGENCY_TYPES = [
        ('local', 'Local Operator'),
        ('national', 'National Operator'),
        ('international', 'International Operator'),
    ]
    
    name = models.CharField(max_length=200)
    agency_type = models.CharField(max_length=20, choices=AGENCY_TYPES)
    description = models.TextField(blank=True)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    website = models.URLField(blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0, 
                               validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    license_number = models.CharField(max_length=100, blank=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name_plural = "Travel Agencies"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.get_agency_type_display()})"

class TravelClass(models.Model):
    CLASS_TYPES = [
        ('economy', 'Economy/Lower Class'),
        ('standard', 'Standard/Middle Class'),
        ('business', 'Business Class'),
        ('first', 'First Class'),
        ('luxury', 'Luxury/Upper Class'),
        ('premium', 'Premium Luxury'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    class_type = models.CharField(max_length=20, choices=CLASS_TYPES)
    description = models.TextField(blank=True)
    amenities = models.TextField(blank=True, help_text="Comma separated amenities")
    price_multiplier = models.DecimalField(max_digits=5, decimal_places=2, default=1.0,
                                         help_text="Multiplier for base price")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name_plural = "Travel Classes"
        ordering = ['price_multiplier']
    
    def __str__(self):
        return f"{self.name} ({self.get_class_type_display()})"

class Hotel(models.Model):
    HOTEL_TYPES = [
        ('hotel', 'Hotel'),
        ('resort', 'Resort'),
        ('villa', 'Villa'),
        ('hostel', 'Hostel'),
        ('homestay', 'Homestay'),
        ('apartment', 'Apartment'),
        ('camp', 'Camp'),
    ]
    
    STAR_RATINGS = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    name = models.CharField(max_length=200)
    hotel_type = models.CharField(max_length=20, choices=HOTEL_TYPES)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='hotels')
    address = models.TextField()
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)
    star_rating = models.IntegerField(choices=STAR_RATINGS, null=True, blank=True)
    description = models.TextField()
    amenities = models.TextField(blank=True, help_text="Comma separated amenities")
    check_in_time = models.TimeField(default='14:00:00')
    check_out_time = models.TimeField(default='12:00:00')
    has_swimming_pool = models.BooleanField(default=False)
    has_spa = models.BooleanField(default=False)
    has_gym = models.BooleanField(default=False)
    has_restaurant = models.BooleanField(default=True)
    wifi_available = models.BooleanField(default=True)
    parking_available = models.BooleanField(default=False)
    image = models.ImageField(upload_to='hotels/', null=True, blank=True)
    website = models.URLField(blank=True)
    average_price_per_night = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0,
                               validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['name']
        unique_together = ['name', 'destination']
    
    def __str__(self):
        return f"{self.name} - {self.destination.name}"

class RoomType(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='room_types')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    max_occupancy = models.IntegerField(default=2)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    amenities = models.TextField(blank=True)
    size = models.CharField(max_length=50, blank=True, help_text="Room size in sq ft")
    bed_type = models.CharField(max_length=100, blank=True)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='rooms/', null=True, blank=True)
    
    class Meta:
        ordering = ['base_price']
    
    def __str__(self):
        return f"{self.name} - {self.hotel.name}"