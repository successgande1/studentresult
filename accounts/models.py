from django.db import models
from django.contrib.auth.models import User
import uuid
from imagekit.models import ProcessedImageField
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from imagekit.processors import ResizeToFill, Transpose
from django.utils import timezone
from datetime import timedelta


@deconstructible
class FileExtensionValidator:
    """ImageKit Validation Decorator"""
    def __init__(self, extensions):
        self.extensions = extensions

    def __call__(self, value):
        extension = value.name.split('.')[-1].lower()
        if extension not in self.extensions:
            valid_extensions = ', '.join(self.extensions)
            raise ValidationError(f"Invalid file extension. Only {valid_extensions} files are allowed.")


image_extensions = ['jpeg', 'jpg', 'gif', 'png']


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name

 
# Ticket Model
class Subscription(models.Model):
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    pin = models.UUIDField(default=uuid.uuid4, unique=True)
    expiration_date = models.DateTimeField()
    duration_days = models.IntegerField()

    def __str__(self):
        return f'{self.plan} - {self.pin}'

    def is_expired(self):
        return timezone.now() > self.expiration_date

    def save(self, *args, **kwargs):
        if not self.pin:
            self.pin = self.generate_pin()

        # Calculate the expiration date based on the duration of the associated subscription plan
        self.expiration_date = timezone.now() + timedelta(days=self.duration_days)

        super().save(*args, **kwargs)

    @staticmethod
    def generate_pin():
        import random
        import string

        # Generate a random 6-character PIN
        pin = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return pin


class BusinessAccount(models.Model):
    ACCOUNT_CHOICES = [
        ('NURSERY & PRIMARY SCHOOL', 'Nursery & Primary School'),
        ('JUNIOR & SENIOR SECONDARY SCHOOL', 'Junior & Senior Secondary School'),
        ('JUNIOR SECONDARY SCHOOL', 'Junior Secondary School'),
        ('SENIOR SECONDARY SCHOOL', 'Senior Secondary School'),
    ]
    name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=100, choices=ACCOUNT_CHOICES, null=True)
    address = models.CharField(max_length=200, null=True)
    lga = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    subscription_plan = models.ForeignKey(Subscription, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class SubscriptionHistory(models.Model):
    business_account = models.ForeignKey(BusinessAccount, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    pin = models.UUIDField(default=uuid.uuid4, unique=True)
    start_date = models.DateField()
    expiration_date = models.DateField()

    def __str__(self):
        return f'Subscription for {self.business_account.name} ({self.plan.name})'


class Profile(models.Model):
    STATE_CHOICES = [
        ('benue', 'Benue'),
    ]
    LGA_CHOICES = [
        ('gboko', 'Gboko'), 
        ('kwande', 'Kwande'),
        ('katsina-ala', 'Katsina-Ala'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(BusinessAccount, on_delete=models.CASCADE, null=True)
    role = models.CharField(max_length=20, blank=True)  # 'admin', 'cashier', 'customer'
    full_name = models.CharField(max_length=60, blank=True)
    phone = models.CharField(max_length=14, blank=True)
    address = models.CharField(max_length=160, blank=True)
    state = models.CharField(max_length=50, choices=STATE_CHOICES, null=True)
    lga = models.CharField(max_length=50, choices=LGA_CHOICES, null=True)
    is_active = models.BooleanField(default=True)  
    image = ProcessedImageField(upload_to='profile_images', processors=[Transpose(), ResizeToFill(150, 200)], format='JPEG', options={'quality': 97}, validators=[FileExtensionValidator(image_extensions)], default='avatar.jpg')
    last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}-Profile'
