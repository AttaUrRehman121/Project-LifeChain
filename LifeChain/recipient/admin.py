from django.contrib import admin
from .models import Recipient , AllocatedDonorToRecipient

class RecipientAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'age', 'gender', 'blood_type', 'rh_factor', 'height_cm', 'weight_kg', 
        'bmi', 'wait_list_days', 'medical_urgency_score', 'hemoglobin', 'wbc_count', 
        'platelet_count', 'creatinine', 'alt', 'ast', 'diabetes', 'hypertension', 
        'previous_transplant', 'dialysis_status', 'required_organ', 'antibody_screen', 
        'pra_score', 'transplant_eligibility'
    )
    list_filter = ('transplant_eligibility', 'required_organ', 'gender', 'diabetes', 'hypertension')
    search_fields = ('required_organ', 'transplant_eligibility', 'blood_type')
    list_per_page = 20

class AllocatedDonorToRecipientAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'donor', 'verification_status', 'verification_token', 'token', 'transaction_hash','token_expiry','allocation_date')
    list_filter = ('verification_status', 'allocation_date')
    search_fields = ('recipient__user__username', 'donor__username')
    list_per_page = 20

# Register the Recipient model with the admin interface
admin.site.register(Recipient, RecipientAdmin)
admin.site.register(AllocatedDonorToRecipient, AllocatedDonorToRecipientAdmin)


admin.site.site_header = "LifeChain Admin"
