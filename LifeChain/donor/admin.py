from django.contrib import admin
from .models import PredictionRecord, donor_Registered

class PredictionRecordAdmin(admin.ModelAdmin):
    list_display = (
        'age', 'gender', 'blood_type', 'rh_factor', 'height_cm', 'weight_kg',
        'bmi', 'systolic_bp', 'diastolic_bp', 'heart_rate', 'temperature_celsius',
        'respiratory_rate', 'hemoglobin', 'wbc_count', 'platelet_count', 'creatinine',
        'alt', 'ast', 'total_bilirubin', 'albumin', 'hiv_status', 'hbv_status',
        'hcv_status', 'cmv_status', 'ebv_status', 'diabetes', 'hypertension',
        'cardiac_disease', 'cancer_history', 'organ_type', 'organ_condition_score',
        'donation_status', 'prediction_result', 'created_at'
    )
    list_filter = ('prediction_result', 'organ_type', 'donation_status')
    search_fields = ('username', 'email', 'organ_type')
    list_per_page = 20

class DonorRegisteredAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'contact', 'email', 'age', 'gender', 'blood_type', 'rh_factor', 
        'address', 'eligibility', 'organ_type', 'user'
    )
    search_fields = ('username', 'email', 'eligibility', 'organ_type', 'blood_type')
    list_filter = ('eligibility', 'organ_type', 'blood_type', 'rh_factor', 'gender')
    list_per_page = 20

# Register models with custom admin views
admin.site.register(PredictionRecord, PredictionRecordAdmin)
admin.site.register(donor_Registered, DonorRegisteredAdmin)

