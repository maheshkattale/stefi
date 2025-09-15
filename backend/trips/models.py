from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import uuid
from Masters.models import Destination, TravelClass  # explicit import

class TripPlan(models.Model):
    TRAVEL_METHODS = [
        ("air", "Air"),
        ("road", "Road"),
        ("train", "Train"),
        ("sea", "Sea"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="trips")
    title = models.CharField(max_length=255, default="My Trip")
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='trips')
    currency = models.CharField(max_length=10, null=True, blank=True)

    persons = models.PositiveIntegerField(default=1)
    travel_method = models.CharField(max_length=20, choices=TRAVEL_METHODS, default="road")
    budget = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    start_date = models.DateField()
    end_date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default="draft", choices=[
        ("draft", "Draft"),
        ("planned", "Planned"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['destination']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.title} to {self.destination.name} ({self.user.username})"

    def duration(self):
        return (self.end_date - self.start_date).days

    def calculate_total_cost(self):
        return sum(item.total_cost for item in self.itinerary.all())

    def save(self, *args, **kwargs):
        if self.budget == 0:
            self.budget = self.calculate_total_cost()
        super().save(*args, **kwargs)


class ItineraryItem(models.Model):
    TIME_CHOICES = [
        ("morning", "Morning"),
        ("afternoon", "Afternoon"),
        ("evening", "Evening"),
        ("night", "Night"),
    ]

    TYPE_CHOICES = [
        ("travel", "Travel"),
        ("hotel", "Hotel Stay"),
        ("activity", "Activity"),
        ("meal", "Meal"),
        ("sightseeing", "Sightseeing"),
        ("shopping", "Shopping"),
        ("other", "Other"),
    ]

    trip = models.ForeignKey(TripPlan, on_delete=models.CASCADE, related_name="itinerary")
    date = models.DateField()
    time_of_day = models.CharField(max_length=20, choices=TIME_CHOICES)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField()
    location = models.CharField(max_length=200, blank=True, null=True)
    cost_per_person = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    persons = models.PositiveIntegerField(default=1)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    duration_hours = models.DecimalField(max_digits=4, decimal_places=1, default=2.0)
    notes = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_ai_suggested = models.BooleanField(default=False)
    ai_confidence_score = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ['date', 'order', 'time_of_day']
        indexes = [
            models.Index(fields=['trip']),
            models.Index(fields=['date']),
            models.Index(fields=['type']),
        ]

    def save(self, *args, **kwargs):
        self.total_cost = self.cost_per_person * self.persons
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.date} {self.time_of_day} - {self.title or self.type}"


class TripInvoice(models.Model):
    trip = models.OneToOneField(TripPlan, on_delete=models.CASCADE, related_name="invoice")
    invoice_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=10.0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes = models.TextField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    paid_date = models.DateTimeField(blank=True, null=True)

    def generate_invoice(self):
        self.subtotal = self.trip.calculate_total_cost()
        self.tax_amount = (self.subtotal * self.tax_percentage) / 100
        self.total_amount = self.subtotal + self.tax_amount - self.discount

        if not self.due_date:
            self.due_date = timezone.now() + timedelta(days=15)

        self.save()
        return self

    def __str__(self):
        return f"Invoice #{self.invoice_number} for {self.trip}"


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(TripInvoice, on_delete=models.CASCADE, related_name="items")
    description = models.CharField(max_length=200)
    date = models.DateField()
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['date']

    def save(self, *args, **kwargs):
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.description} - {self.total_price}"


class PackingItem(models.Model):
    trip = models.ForeignKey(TripPlan, on_delete=models.CASCADE, related_name='packing_items')
    name = models.CharField(max_length=100)
    is_checked = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class TripPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="trip_preferences")
    interests = models.TextField(blank=True, help_text="Comma-separated: beach, adventure, culture")
    travel_class = models.ForeignKey(TravelClass, on_delete=models.SET_NULL, null=True, blank=True)
    budget_per_person = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    max_days = models.PositiveIntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Trip Preferences"

    def __str__(self):
        return f"{self.user.username} preferences"
