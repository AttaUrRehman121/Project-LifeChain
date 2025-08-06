from django.db import models
from django.db import models
from django.conf import settings
from donor.models import donor_Registered
from registration.models import UserProfile
from django.utils import timezone
from datetime import timedelta
import uuid
from django.db import models
from datetime import timedelta


# Create your models here.
class Recipient(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    GENDER_CHOICES = [
        (0, 'Female'),
        (1, 'Male'),
    ]
    
    RH_FACTOR_CHOICES = [
        (0, 'Negative'),
        (1, 'Positive'),
    ]
    
    DIABETES_CHOICES = [
        (0, 'No'),
        (1, 'Yes'),
    ]
    
    HYPERTENSION_CHOICES = [
        (0, 'No'),
        (1, 'Yes'),
    ]
    
    TRANSPLANT_CHOICES = [
        (0, 'No'),
        (1, 'Yes'),
    ]
    
    DIALYSIS_CHOICES = [
        (0, 'No'),
        (1, 'Yes'),
    ]
    
    age = models.FloatField()
    gender = models.IntegerField(choices=GENDER_CHOICES)
    blood_type = models.CharField(max_length=3)
    rh_factor = models.IntegerField(choices=RH_FACTOR_CHOICES)
    height_cm = models.FloatField()
    weight_kg = models.FloatField()
    bmi = models.FloatField()
    wait_list_days = models.IntegerField()
    medical_urgency_score = models.FloatField()
    hemoglobin = models.FloatField()
    wbc_count = models.FloatField()
    platelet_count = models.FloatField()
    creatinine = models.FloatField()
    alt = models.FloatField()
    ast = models.FloatField()
    diabetes = models.IntegerField(choices=DIABETES_CHOICES)
    hypertension = models.IntegerField(choices=HYPERTENSION_CHOICES)
    previous_transplant = models.IntegerField(choices=TRANSPLANT_CHOICES)
    dialysis_status = models.IntegerField(choices=DIALYSIS_CHOICES)
    required_organ = models.CharField(max_length=50)
    antibody_screen = models.FloatField()
    pra_score = models.FloatField()
    transplant_eligibility = models.CharField(max_length=50, default='not eligible')
    wallet_address = models.CharField(max_length=42, blank=True, null=True)
    def __str__(self):
        return f"{self.required_organ} - {self.transplant_eligibility}"

 


def one_day_from_now():
    return timezone.now() + timedelta(days=7)

class AllocatedDonorToRecipient(models.Model):
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE)
    donor = models.ForeignKey(donor_Registered, on_delete=models.CASCADE)
    verification_status = models.BooleanField(default=False)
    verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    token = models.CharField(max_length=66, unique=True)  # 0x-prefixed hex string of 64 characters
    transaction_hash = models.CharField(max_length=66, blank=True, null=True)
    token_expiry = models.DateTimeField(default=one_day_from_now)
    allocation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Allocation of {self.donor} to {self.recipient} on {self.allocation_date}"