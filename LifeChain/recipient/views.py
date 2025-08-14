from datetime import timedelta, timezone
import json
import os
from urllib import request
from django.contrib import messages
import logging
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
import joblib
import numpy as np
import logging
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from web3 import Web3
from django.utils.timezone import now
from .models import UserProfile
from .models import AllocatedDonorToRecipient, Recipient
from donor.models import donor_Registered
from django.core.mail import send_mail
from django.utils import timezone
from .blockchain import contract, w3, backend_wallet_address, backend_private_key
from home.views import index
# Create your views here.
@login_required
def recipientpage(request):
    user = request.user
    if UserProfile.objects.filter(username=user, role='recipient').exists():
        messages.success(request, "Welcome to Recipient. You can make a prediction or view your previous report.")
        return render(request, 'recipientPage.html')
    else:
        messages.info(request, "You are not registered as a recipient. Please register first.")
        return redirect(reverse('index'))

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
@login_required
def recipientprictiction(request):
    user = request.user
   
    if Recipient.objects.filter(user=user).exists():
        recipient = Recipient.objects.get(user=user)
        messages.info(request, "You have already made a prediction. Here is your previous report. One prediction per user is allowed.")
        
        # Create result context for existing recipient
        result = {
            'eligibility': recipient.transplant_eligibility,
            'compatibility_score': 90 if recipient.transplant_eligibility == 'Eligible' else 25,
            'assessment_date': 'Previously completed',
            'organ_type': recipient.required_organ,
            'priority_level': 'High' if recipient.medical_urgency_score > 7 else 'Standard',
            'matching_notes': 'Our system will search for compatible donors based on your medical profile.',
            'wait_time_notes': 'Estimated wait time based on current donor availability and your priority level.',
            'safety_notes': 'Comprehensive safety protocols ensure the highest standards for transplantation.'
        }
        
        return render(request, 'RecipientResultPage.html', {
            'record': recipient,
            'result': result
        })

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
                user=request.user,
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
            # Create result context with proper formatting
            result = {
                'eligibility': record.transplant_eligibility,
                'compatibility_score': 90 if record.transplant_eligibility == 'Eligible' else 25,  # Mock score for now
                'assessment_date': 'Recently completed',
                'organ_type': record.required_organ,
                'priority_level': 'High' if record.medical_urgency_score > 7 else 'Standard',
                'matching_notes': 'Our system will search for compatible donors based on your medical profile.',
                'wait_time_notes': 'Estimated wait time based on current donor availability and your priority level.',
                'safety_notes': 'Comprehensive safety protocols ensure the highest standards for transplantation.'
            }
            
            context = {
                'record': record, 
                'result': result,
                'message': 'Prediction record saved successfully!'
            }
            return render(request, 'RecipientResultPage.html', context)
        
        except Exception as e:
            error_message = f'An error occurred: {str(e)}'
            logging.error("Error processing recipient prediction: %s", error_message)
            context = {'error_message': error_message}
            return render(request, 'RecipientPrediction.html', context)

    logging.info("Received GET request for recipient prediction page.")
    return render(request, 'RecipientPrediction.html')

  
@login_required
def eligible_donors(request):
    try:
        # Check if user is a recipient
        if not Recipient.objects.filter(user=request.user).exists():
            messages.error(request, "You are not registered as a recipient.")
            return redirect('profile_view')

        recipient = Recipient.objects.get(user=request.user)

        # Check for existing valid allocation (not expired)
        allocation = AllocatedDonorToRecipient.objects.filter(
            recipient=recipient,
            verification_status__in=[False, True],
            token_expiry__gt=now()
        ).first()

        if allocation:
            messages.info(
                request,
                f"You have already been allocated with donor '{allocation.donor.username}'. Check your profile for details."
            )
            return redirect('profile_view')

        # No valid allocation, show available eligible donors
        # Exclude donors who are already allocated to any recipient (with a non-expired allocation)
        allocated_donor_ids = AllocatedDonorToRecipient.objects.filter(
            verification_status__in=[False, True],
            token_expiry__gt=now()
        ).values_list('donor_id', flat=True)

        eligible_donors = donor_Registered.objects.filter(
            eligibility='Eligible',
            is_allocated=False
        ).exclude(id__in=allocated_donor_ids)

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
    
    

    

# @login_required
# def allocate_donor(request, donor_id):
#     print("Allocate donor triggered", donor_id)
#     donor = get_object_or_404(donor_Registered, id=donor_id)
#     user = request.user
#     recipient = get_object_or_404(Recipient, user=user)

#     # Avoid duplicate allocation
#     if AllocatedDonorToRecipient.objects.filter(donor=donor, recipient=recipient).exists():
#         return JsonResponse({'error': 'Already allocated'}, status=400)

#     # Create allocation with token and expiry
#     allocation = AllocatedDonorToRecipient.objects.create(
#         recipient=recipient,
#         donor=donor
#     )

#     # Generate verification URL
#     verify_url = request.build_absolute_uri(
#         reverse('verify_donor_email', args=[allocation.verification_token])
#     )

#     # Send verification email to donor
#     send_mail(
#         subject='Organ Donation Request',
#         message=f'''Dear {donor.username},

#             You have been matched with a recipient for organ donation.

#             Recipient: {recipient.user.username}
#             Organ Requested: {donor.organ_type}
#             Blood Type: {donor.blood_type}

#             Please confirm your agreement to donate by clicking the link below within 24 hours:
#             {verify_url}

#             If you do not respond within 1 day, this request will be canceled.

#             Thank you,
#             LifeChain Team
#             ''',
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         recipient_list=[donor.email],
#         fail_silently=False,
#     )

#     return JsonResponse({'status': 'success'})

# def verify_donor_email(request, token):
#     try:
#         # Get allocation using the token
#         allocation = AllocatedDonorToRecipient.objects.get(verification_token=token)
#         donor = allocation.donor
#         recipient_user = allocation.recipient.user  # UserProfile from Recipient

#         # Check token expiration
#         if timezone.now() > allocation.token_expiry:
#             donor_name = donor.username

#             # Delete expired allocation
#             allocation.delete()

#             # Mark donor as eligible again
#             donor.is_allocated = False
#             donor.save()

#             # Email recipient about expiration
#             send_mail(
#                 subject='Donation Request Expired',
#                 message=f'''Dear {recipient_user.username},

#             Unfortunately, the donor "{donor_name}" did not verify their donation within 24 hours. The request has now been cancelled.

#             You may try allocating a different donor.

#             Regards,  
#             LifeChain Team
#             ''',
#                 from_email=settings.DEFAULT_FROM_EMAIL,
#                 recipient_list=[recipient_user.email],
#                 fail_silently=False,
#             )

#             messages.error(request, "Verification link expired. Allocation has been cancelled.")
#             return redirect('profile_view')

#         # Donor verified in time
#         allocation.verification_status = True
#         allocation.save()

#         # Mark donor as no longer eligible
#         donor.is_allocated = True
#         donor.save()

#         messages.success(request, "Thank you for confirming your donation.")
#         return redirect('profile_view')

#     except AllocatedDonorToRecipient.DoesNotExist:
#         messages.error(request, "Invalid or already used verification link.")
#         return redirect('profile_view')
# Setup Web3
from web3 import Web3
BACKEND_ADDRESS = Web3.to_checksum_address(settings.BACKEND_WALLET_ADDRESS)
PRIVATE_KEY = settings.BACKEND_PRIVATE_KEY

# Connect to Ganache
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
@login_required
@csrf_exempt
def allocate_donor(request, donor_id):
    try:
        print("Allocate donor triggered", donor_id)
        donor = get_object_or_404(donor_Registered, id=donor_id)
        recipient = get_object_or_404(Recipient, user=request.user)

        if not donor.user.wallet_address or not recipient.user.wallet_address:
            return JsonResponse({'error': 'Missing wallet address.'}, status=400)

        nonce = w3.eth.get_transaction_count(backend_wallet_address)
        txn = contract.functions.allocateDonorToRecipient(
            donor.user.wallet_address,
            recipient.user.wallet_address
        ).build_transaction({
            'from': backend_wallet_address,
            'nonce': nonce,
            'gas': 3000000,
            'gasPrice': w3.to_wei('1', 'gwei'),
        })

        signed_tx = w3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        # Process event logs
        event_logs = contract.events.DonorAllocated().process_receipt(receipt)
        
        if not event_logs:
            logger.error("DonorAllocated event not found in logs.")
            return JsonResponse({'error': 'Event not found in logs.'}, status=500)

        event = event_logs[0]
        token = event['args']['token'].hex()
        donor_address = event['args']['donor']
        recipient_address = event['args']['recipient']
        expiry_timestamp = event['args']['expiry']

        print("✅ Event decoded:")
        print("Token:", token)
        print("Donor:", donor_address)
        print("Recipient:", recipient_address)
        print("Expiry:", expiry_timestamp)

        # Create allocation in database
        allocation = AllocatedDonorToRecipient.objects.create(
            donor=donor,
            recipient=recipient,
            token=token,
            token_expiry=timezone.datetime.fromtimestamp(expiry_timestamp, tz=timezone.utc),
            transaction_hash=tx_hash.hex(),
        )

        # Generate verification URL and send email
        verify_url = request.build_absolute_uri(reverse('verify_donor_email', args=[token]))
        send_mail(
            subject='Organ Donation Request',
            message=f'''Dear {donor.user.username},

You have been matched with a recipient.
Please verify your consent by clicking this link within 7 days:
{verify_url}

Regards,
LifeChain Team
''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[donor.user.email],
            fail_silently=False,
        )

        return JsonResponse({'message': 'Donor allocated successfully', 'token': token})

    except Exception as e:
        logger.exception("Allocation error:")
        return JsonResponse({'error': str(e)}, status=500)



@login_required
def verify_donor_email(request, token):
    try:
        allocation = get_object_or_404(AllocatedDonorToRecipient, token=token)

        if request.user != allocation.donor.user:
            messages.error(request, "You are not authorized to verify this donation.")
            return redirect('profile_view')

        token_bytes = bytes.fromhex(token.replace("0x", ""))
        donor_address, recipient_address, is_verified, token_expiry = contract.functions.getAllocation(token_bytes).call()

        if is_verified:
            messages.error(request, "This link has already been used.")
            return redirect('profile_view')

        if timezone.now().timestamp() > token_expiry:
            messages.error(request, "Verification link has expired.")
            return redirect('profile_view')

        nonce = w3.eth.get_transaction_count(backend_wallet_address)
        txn = contract.functions.verifyDonation(token_bytes).build_transaction({
            'from': backend_wallet_address,
            'nonce': nonce,
            'gas': 3000000,
            'gasPrice': w3.to_wei('1', 'gwei'),
        })

        signed_txn = w3.eth.account.sign_transaction(txn, private_key=backend_private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        w3.eth.wait_for_transaction_receipt(tx_hash)

        allocation.verification_status = True
        allocation.transaction_hash = tx_hash.hex()
        allocation.save()

        messages.success(request, "Thank you for verifying your donation.")
        return redirect('profile_view')

    except Exception as e:
        logger.exception("Blockchain verification error:")
        messages.error(request, "Invalid or expired verification link.")
        return redirect('profile_view')

@login_required
def RecipientResultpage(request):
    # Check if user has a recipient record
    if Recipient.objects.filter(user=request.user).exists():
        record = Recipient.objects.get(user=request.user)
        
        # Create result context for existing recipient
        result = {
            'eligibility': record.transplant_eligibility,
            'compatibility_score': 90 if record.transplant_eligibility == 'Eligible' else 25,
            'assessment_date': 'Previously completed',
            'organ_type': record.required_organ,
            'priority_level': 'High' if record.medical_urgency_score > 7 else 'Standard',
            'matching_notes': 'Our system will search for compatible donors based on your medical profile.',
            'wait_time_notes': 'Estimated wait time based on current donor availability and your priority level.',
            'safety_notes': 'Comprehensive safety protocols ensure the highest standards for transplantation.'
        }
        
        return render(request, 'RecipientResultPage.html', {
            'record': record,
            'result': result
        })
    else:
        # No recipient record found
        messages.warning(request, "No recipient record found. Please complete a compatibility assessment first.")
        return redirect('recipientprictiction')

