from django.contrib import admin
from .models import Recipient

class RecipientAdmin(admin.ModelAdmin):
    list_display = (
        'age', 'gender', 'blood_type', 'rh_factor', 'height_cm', 'weight_kg', 
        'bmi', 'wait_list_days', 'medical_urgency_score', 'hemoglobin', 'wbc_count', 
        'platelet_count', 'creatinine', 'alt', 'ast', 'diabetes', 'hypertension', 
        'previous_transplant', 'dialysis_status', 'required_organ', 'antibody_screen', 
        'pra_score', 'transplant_eligibility'
    )
    list_filter = ('transplant_eligibility', 'required_organ', 'gender', 'diabetes', 'hypertension')
    search_fields = ('required_organ', 'transplant_eligibility', 'blood_type')
    list_per_page = 20

# Register the Recipient model with the admin interface
admin.site.register(Recipient, RecipientAdmin)
