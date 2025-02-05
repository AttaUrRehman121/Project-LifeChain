from django.db import models

# # Create your models here.

# class Signup(models.Model):
#     username = models.CharField(max_length=255)
#     email = models.EmailField()
#     password = models.CharField(max_length=255)
#     cpassword = models.CharField(max_length=255)
    
# # 

from django.db import models

class PredictionRecord(models.Model):
    age = models.FloatField()
    gender = models.CharField(max_length=1)  # 'M' or 'F'
    blood_type = models.CharField(max_length=2)  # 'A', 'B', 'AB', 'O'
    rh_factor = models.CharField(max_length=1)  # '+' or '-'
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
    hiv_status = models.CharField(max_length=10)  # 'negative' or 'positive'
    hbv_status = models.CharField(max_length=10)  # 'negative' or 'positive'
    hcv_status = models.CharField(max_length=10)  # 'negative' or 'positive'
    cmv_status = models.CharField(max_length=10)  # 'negative' or 'positive'
    ebv_status = models.CharField(max_length=10)  # 'negative' or 'positive'
    diabetes = models.CharField(max_length=3)  # 'no' or 'yes'
    hypertension = models.CharField(max_length=3)  # 'no' or 'yes'
    cardiac_disease = models.CharField(max_length=3)  # 'no' or 'yes'
    cancer_history = models.CharField(max_length=3)  # 'no' or 'yes'
    organ_type = models.CharField(max_length=20)  # 'kidney', 'liver', etc.
    organ_condition_score = models.FloatField()
    donation_status = models.CharField(max_length=20)  # 'eligible' or 'not eligible'
    prediction_result = models.CharField(max_length=20)  # 'eligible' or 'not eligible'
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Record {self.id} - Prediction: {self.prediction_result}"