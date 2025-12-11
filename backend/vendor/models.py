from django.db import models
from helpers.models import TrackingModel
from django.db.models.deletion import CASCADE

class Vendor(TrackingModel):

    # Basic Details
    name = models.CharField(max_length=255)
    legal_name = models.CharField(max_length=255, null=True, blank=True)  # Registered company name
    vendor_code = models.CharField(max_length=50, unique=True, null=True, blank=True)

    # Contact Info
    phone = models.CharField(max_length=20)
    alternate_phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(unique=True)
    alternate_email = models.EmailField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)

    # Address Info
    address = models.TextField()
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=20, null=True, blank=True)

    # Business & Tax Details
    gst_number = models.CharField(max_length=50, null=True, blank=True)
    pan_number = models.CharField(max_length=20, null=True, blank=True)
    registration_number = models.CharField(max_length=100, null=True, blank=True)

    # Banking Details (for payments)
    bank_name = models.CharField(max_length=150, null=True, blank=True)
    account_number = models.CharField(max_length=50, null=True, blank=True)
    ifsc_code = models.CharField(max_length=20, null=True, blank=True)
    branch_name = models.CharField(max_length=150, null=True, blank=True)
    upi_id = models.CharField(max_length=100, null=True, blank=True)

    # Vendor Type & Category
    vendor_type = models.CharField(
        max_length=50,
        choices=[
            ('manufacturer', 'Manufacturer'),
            ('wholesaler', 'Wholesaler'),
            ('service_provider', 'Service Provider'),
            ('dealer', 'Dealer'),
            ('retailer', 'Retailer'),
        ],
        null=True, blank=True
    )
    category = models.CharField(max_length=200, null=True, blank=True)

    # Status & Internal Notes
    notes = models.TextField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name
