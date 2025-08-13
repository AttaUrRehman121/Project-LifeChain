from django.db import models
from django.conf import settings
from registration.models import UserProfile
    



class PredictionRecord(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    age = models.FloatField()
    gender = models.IntegerField()  # this will store like This 1 for 'M', 0 for 'F'
    blood_type = models.CharField(max_length=2)  # this will store like This 'A', 'B', 'AB', 'O'
    rh_factor = models.IntegerField()  # this will store like This 1 for '+', 0 for '-'
    height_cm = models.FloatField()
    weight_kg = models.FloatField()
    bmi = models.FloatField()
    systolic_bp = models.FloatField()
    diastolic_bp = models.FloatField()
    heart_rate = models.FloatField()
    temperature_celsius = models.FloatField()
    respiratory_rate = models.FloatField()
    hemoglobin = models.FloatField()
    wbc_count = models.FloatField()
    platelet_count = models.FloatField()
    creatinine = models.FloatField()
    alt = models.FloatField()
    ast = models.FloatField()
    total_bilirubin = models.FloatField()
    albumin = models.FloatField()
    hiv_status = models.IntegerField()  #  this will store like This 1 for 'positive', 0 for 'negative'
    hbv_status = models.IntegerField()  #  this will store like This 1 for 'positive', 0 for 'negative'
    hcv_status = models.IntegerField()  # this will store like This 1 for 'positive', 0 for 'negative'
    cmv_status = models.IntegerField()  #  this will store like This 1 for 'positive', 0 for 'negative'
    ebv_status = models.IntegerField()  # this will store like This 1 for 'positive', 0 for 'negative'
    diabetes = models.IntegerField()  # this will store like This 1 for 'yes', 0 for 'no'
    hypertension = models.IntegerField()  # this will store like This 1 for 'yes', 0 for 'no'
    cardiac_disease = models.IntegerField()  # this will store like This 1 for 'yes', 0 for 'no'
    cancer_history = models.IntegerField()  # this will store like This 1 for 'yes', 0 for 'no'
    organ_type = models.CharField(max_length=20)  # 'kidney', 'liver', etc.
    organ_condition_score = models.FloatField()
    donation_status = models.IntegerField(default=0) # this will store like This 1 for 'eligible', 0 for 'not eligible'
    prediction_result = models.CharField(max_length=20)  # this will store like This 'eligible' or 'not eligible'
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Record {self.id} - Prediction: {self.prediction_result}"
    
    
    

class donor_Registered(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    email = models.EmailField()
    age = models.FloatField()
    # Changed gender to store 'Male' and 'Female' as strings
    gender = models.CharField(max_length=6, choices=[('Male', 'Male'), ('Female', 'Female')])
    
    # Changed blood_type to store 'A', 'B', 'AB', 'O' as strings
    blood_type = models.CharField(max_length=2, choices=[('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O')])
    
    # Changed rh_factor to store '+' and '-' as strings
    rh_factor = models.CharField(max_length=1, choices=[('+', '+'), ('-', '-')])
    
    organ_type = models.CharField(max_length=50, choices=[
        ('Kidney', 'Kidney'),
        ('Liver', 'Liver'),
        ('Heart', 'Heart'),
        ('Lungs', 'Lungs'),
        ('Pancreas', 'Pancreas')
    ])
    address = models.TextField()
    eligibility = models.CharField(max_length=50)
    is_allocated = models.BooleanField(default=False)

    wallet_address = models.CharField(max_length=42, blank=True, null=True)
    def __str__(self):
        return self.username




