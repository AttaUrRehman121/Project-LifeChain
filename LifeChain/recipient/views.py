from datetime import timezone
import os
from django.contrib import messages
from venv import logger
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
import joblib
import numpy as np
import logging
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
import pandas as pd
from .models import AllocatedDonorToRecipient, Recipient
from donor.models import donor_Registered
from django.core.mail import send_mail
from django.utils import timezone
# Create your views here.
@login_required
def recipientpage(request):
    return render(request, 'recipientPage.html')
 

# Configure logging
logging.basicConfig(
    filename='recipient_prediction.log',  
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Model file path
base_dir = os.path.abspath(os.path.dirname(__file__))
model_filename = 'recipient_model_RandomForest.pkl'
model_file_path = os.path.join(base_dir, 'MLmodel', model_filename)

# Load the model safely
model = None
if os.path.exists(model_file_path):
    try:
        model = joblib.load(model_file_path)
        logging.info("Model loaded successfully from %s", model_file_path)
        print("Model type:", type(model))  # Ensure it's correct
    except Exception as e:
        logging.error("Error loading model: %s", str(e))
else:
    logging.warning("Model file not found at %s", model_file_path)

# Blood type mapping
blood_type_mapping = {'A': 0, 'B': 1, 'AB': 2, 'O': 3}

def recipientprictiction(request):
    if request.method == 'POST':
        try:
            logging.info("Received POST request for recipient prediction.")
            #login user 
            logging.info("User is authenticated: %s", request.user.id)
            
            # Extract input values safely
            age = float(request.POST.get('age', 0))
            gender = 1 if request.POST.get('gender') == 'male' else 0
            blood_type = blood_type_mapping.get(request.POST.get('blood_type'), -1)  # Use `.get()` to avoid KeyError
            rh_factor = 1 if request.POST.get('rh_factor') == 'positive' else 0
            height_cm = float(request.POST.get('height_cm', 0))
            weight_kg = float(request.POST.get('weight_kg', 0))
            bmi = float(request.POST.get('bmi', 0))
            wait_list_days = int(request.POST.get('wait_list_days', 0))
            medical_urgency_score = float(request.POST.get('medical_urgency_score', 0))
            hemoglobin = float(request.POST.get('hemoglobin', 0))
            wbc_count = float(request.POST.get('wbc_count', 0))
            platelet_count = float(request.POST.get('platelet_count', 0))
            creatinine = float(request.POST.get('creatinine', 0))
            alt = float(request.POST.get('alt', 0))
            ast = float(request.POST.get('ast', 0))
            diabetes = 1 if request.POST.get('diabetes') == 'yes' else 0
            hypertension = 1 if request.POST.get('hypertension') == 'yes' else 0
            previous_transplant = 1 if request.POST.get('previous_transplant') == 'yes' else 0
            dialysis_status = 1 if request.POST.get('dialysis_status') == 'yes' else 0
            required_organ = request.POST.get('required_organ', 'Unknown')
            antibody_screen = float(request.POST.get('antibody_screen', 0))
            pra_score = float(request.POST.get('pra_score', 0))

            logging.info("Extracted input data successfully.")

            # Check if model is loaded
            if model:
                input_features = [[
                    age, gender, blood_type, rh_factor, height_cm, weight_kg, bmi, wait_list_days, medical_urgency_score, hemoglobin, wbc_count, platelet_count, creatinine, alt, ast, diabetes, hypertension, previous_transplant, dialysis_status, required_organ, antibody_screen, pra_score
                ]]

                # Make prediction
                prediction = model.predict(input_features)[0]  
                print("Prediction:", prediction)  # Log the prediction
                transplant_eligibility = 'Eligible' if prediction == 1 else 'Not Eligible'
                logging.info("Prediction result: %s", transplant_eligibility)
            else:
                transplant_eligibility = 'Model not available'
                logging.warning("Prediction could not be made because the model is missing.")
            #
            # Save the data to the database
            record = Recipient(
                user = request.user,  
                age=age,
                gender=gender,
                blood_type=blood_type,
                rh_factor=rh_factor,
                height_cm=height_cm,
                weight_kg=weight_kg,
                bmi=bmi,
                wait_list_days=wait_list_days,
                medical_urgency_score=medical_urgency_score,
                hemoglobin=hemoglobin,
                wbc_count=wbc_count,
                platelet_count=platelet_count,
                creatinine=creatinine,
                alt=alt,
                ast=ast,
                diabetes=diabetes,
                hypertension=hypertension,
                previous_transplant=previous_transplant,
                dialysis_status=dialysis_status,
                required_organ=required_organ,
                antibody_screen=antibody_screen,
                pra_score=pra_score,
                transplant_eligibility=transplant_eligibility  # Store prediction
            )
            record.save()
            logging.info("Prediction record saved successfully to the database.")

            # Render the result with a success message
            context = {'record': record, 'message': 'Prediction record saved successfully!'}
            return render(request, 'RecipientResultPage.html', context)
        
        except Exception as e:
            error_message = f'An error occurred: {str(e)}'
            logging.error("Error processing recipient prediction: %s", error_message)
            context = {'error_message': error_message}
            return render(request, 'RecipientPrediction.html', context)

    logging.info("Received GET request for recipient prediction page.")
    return render(request, 'RecipientPrediction.html')

 
# def recipientprictiction(request):
#     if request.method == 'POST':
#         try:
#             age = float(request.POST.get('age'))
#             gender = 1 if request.POST.get('gender') == 'male' else 0
#             blood_type = request.POST.get('blood_type')
#             rh_factor = 1 if request.POST.get('rh_factor') == 'positive' else 0
#             height_cm = float(request.POST.get('height_cm'))
#             weight_kg = float(request.POST.get('weight_kg'))
#             bmi = float(request.POST.get('bmi'))
#             wait_list_days = int(request.POST.get('wait_list_days'))
#             medical_urgency_score = float(request.POST.get('medical_urgency_score'))
#             hemoglobin = float(request.POST.get('hemoglobin'))
#             wbc_count = float(request.POST.get('wbc_count'))
#             platelet_count = float(request.POST.get('platelet_count'))
#             creatinine = float(request.POST.get('creatinine'))
#             alt = float(request.POST.get('alt'))
#             ast = float(request.POST.get('ast'))
#             diabetes = 1 if request.POST.get('diabetes') == 'yes' else 0
#             hypertension = 1 if request.POST.get('hypertension') == 'yes' else 0
#             previous_transplant = 1 if request.POST.get('previous_transplant') == 'yes' else 0
#             dialysis_status = 1 if request.POST.get('dialysis_status') == 'yes' else 0
#             required_organ = request.POST.get('required_organ')
#             antibody_screen = float(request.POST.get('antibody_screen'))
#             pra_score = float(request.POST.get('pra_score'))
#             # Provide default values for required fields not coming from the form.
#             donation_status = 0              # Default value; update as needed
#             prediction_result = 'not eligible'  # Default value; update as needed
            

#             # Save the data to the database
#             record = Recipient(
#                 age=age,
#                 gender=gender,
#                 blood_type=blood_type,
#                 rh_factor=rh_factor,
#                 height_cm=height_cm,
#                 weight_kg=weight_kg,
#                 bmi=bmi,
#                 wait_list_days=wait_list_days,
#                 medical_urgency_score=medical_urgency_score,
#                 hemoglobin=hemoglobin,
#                 wbc_count=wbc_count,
#                 platelet_count=platelet_count,
#                 creatinine=creatinine,
#                 alt=alt,
#                 ast=ast,
#                 diabetes=diabetes,
#                 hypertension=hypertension,
#                 previous_transplant=previous_transplant,
#                 dialysis_status=dialysis_status,
#                 required_organ=required_organ,
#                 antibody_screen=antibody_screen,
#                 pra_score=pra_score,
#                 donation_status=donation_status,
#                 prediction_result=prediction_result
#             )
#             record.save()

#             # Render the result with a success message
#             context = {'record': record, 'message': 'Prediction record saved successfully!'}
#             return render(request, 'RecipientResultPage.html', context)
#         except Exception as e:
#             # Render the form with an error message if something goes wrong
#             context = {'error_message': f'An error occurred: {str(e)}'}
#             return render(request, 'RecipientPrediction.html', context)
#     else:  
#         return render(request, 'RecipientPrediction.html')



    #  this function is to display all  available donors in the database which are eligible for donation and they choose to be a donor  
def eligible_donors(request):
    try:
        eligible_donors = donor_Registered.objects.filter(eligibility='Eligible')

        donors_data = [
            {
                'id': donor.id,
                'username': donor.username,
                'contact': donor.contact,
                'email': donor.email,
                'age': donor.age,
                'gender': donor.gender,
                'blood_type': donor.blood_type,
                'rh_factor': donor.rh_factor,
                'organ_type': donor.organ_type,
                'address': donor.address,
                'eligibility': donor.eligibility,
            }
            for donor in eligible_donors
        ]

        return render(request, 'eligibleDonors.html', {'donors': donors_data})
        
    except Exception as e:
        logger.error(f"Error fetching eligible donors: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)
    
    

    

@login_required
def allocate_donor(request, donor_id):
    print("Allocate donor triggered", donor_id)
    donor = get_object_or_404(donor_Registered, id=donor_id)
    user = request.user
    recipient = get_object_or_404(Recipient, user=user)

    # Avoid duplicate allocation
    if AllocatedDonorToRecipient.objects.filter(donor=donor, recipient=recipient).exists():
        return JsonResponse({'error': 'Already allocated'}, status=400)

    # Create allocation with token and expiry
    allocation = AllocatedDonorToRecipient.objects.create(
        recipient=recipient,
        donor=donor
    )

    # Generate verification URL
    verify_url = request.build_absolute_uri(
        reverse('verify_donor_email', args=[allocation.verification_token])
    )

    # Send verification email to donor
    send_mail(
        subject='Organ Donation Request',
        message=f'''Dear {donor.username},

            You have been matched with a recipient for organ donation.

            Recipient: {recipient.user.username}
            Organ Requested: {donor.organ_type}
            Blood Type: {donor.blood_type}

            Please confirm your agreement to donate by clicking the link below within 24 hours:
            {verify_url}

            If you do not respond within 1 day, this request will be canceled.

            Thank you,
            LifeChain Team
            ''',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[donor.email],
        fail_silently=False,
    )

    return JsonResponse({'status': 'success'})

def verify_donor_email(request, token):
    try:
        allocation = AllocatedDonorToRecipient.objects.get(verification_token=token)

        if timezone.now() > allocation.token_expiry:
            recipient_user = allocation.recipient.user
            donor_name = allocation.donor.username

            # Delete expired allocation
            allocation.delete()

            # Notify recipient via email
            send_mail(
                subject='Donation Request Expired',
                message=f'''Dear {recipient_user.username},

                Unfortunately, the donor "{donor_name}" did not verify their donation within 24 hours. The request has now been cancelled.

                You may try allocating a different donor.

                Regards,  
                LifeChain Team
                ''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient_user.email],
                fail_silently=False,
            )

            messages.error(request, "Verification link expired. Allocation has been cancelled.")
            return redirect('profile_view')

        # Mark as verified
        allocation.verification_status = True
        allocation.save()

        messages.success(request, "Thank you for confirming your donation.")
        return redirect('profile_view')

    except AllocatedDonorToRecipient.DoesNotExist:
        messages.error(request, "Invalid or expired verification link.")
        return redirect('profile_view')
    
    
def RecipientResultpage(request):
    return render(request, 'RecipientResultPage.html')

