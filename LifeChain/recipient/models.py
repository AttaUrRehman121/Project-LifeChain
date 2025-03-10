from django.db import models

# Create your models here.
class Recipient(models.Model):
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
    
    def __str__(self):
        return f"{self.required_organ} - {self.transplant_eligibility}"