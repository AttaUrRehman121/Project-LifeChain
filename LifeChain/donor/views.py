import json
import os
import pickle
import pandas as pd
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import Http404
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import joblib

from LifeChain.settings import EMAIL_HOST_USER
from registration.models import UserProfile
from.models import donor_Registered, PredictionRecord
from django.contrib.auth import get_user_model
import logging
from django.shortcuts import redirect
from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from home.views import index



# Donor Home Page 
@login_required
def donorpage(request):
    user = request.user
    if UserProfile.objects.filter(username=user, role='donor').exists():
        messages.success(request, "Welcome to Donor Side. You can make a prediction or view your previous report.")
        return render(request, 'donorPage.html')
    else:
        messages.error(request, "You do not have permission to visit Donor Side. Make sure you register as Donor.")
        return redirect(index)




# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

base_dir = os.path.dirname(os.path.abspath(__file__))
model_file_path = os.path.join(base_dir, 'MLmodel', 'donor_decision_tree.pkl')

model = joblib.load(model_file_path)


blood_type_mapping = {'A': 0, 'B': 1, 'AB': 2, 'O': 3}
@login_required
@csrf_protect
def donorpridict(request):
    # Check if user already has a prediction
    if PredictionRecord.objects.filter(user=request.user).exists():
        record = PredictionRecord.objects.get(user=request.user)
        messages.info(request, "You have already made a compatibility check. Here is your previous result. One prediction per user is allowed.")
        
        # Create result context for existing prediction
        result = {
            'eligibility': 'Eligible' if record.donation_status == 1 else 'Not Eligible',
            'compatibility_score': 85 if record.donation_status == 1 else 35,
            'assessment_date': record.created_at.strftime('%B %d, %Y') if hasattr(record, 'created_at') else 'Previously completed',
            'organ_type': record.organ_type,
            'medical_notes': 'Your medical profile has been thoroughly analyzed for compatibility factors.',
            'genetic_notes': 'Genetic compatibility has been assessed based on your profile information.',
            'risk_notes': 'Comprehensive risk assessment completed with safety protocols in place.'
        }
        
        return render(request, 'DonorResult.html', {
            'record': record,
            'result': result
        })
    
    if request.method == 'POST':
        try:
            logger.debug("Received POST request for donor prediction.")
            
            # Extract and transform form data
            data = {
                'age': float(request.POST.get('age', 0)),
                'gender': 1 if request.POST.get('gender') == 'M' else 0,
                'blood_type': blood_type_mapping[request.POST.get('blood_type')],  # This converts to 0,1,2,3
                'rh_factor': 1 if request.POST.get('rh_factor') == 'positive' else 0,  # This converts to 0,1
                'height_cm': float(request.POST.get('height_cm', 0)),
                'weight_kg': float(request.POST.get('weight_kg', 0)),
                'bmi': float(request.POST.get('bmi', 0)),
                'systolic_bp': float(request.POST.get('systolic_bp', 0)),
                'diastolic_bp': float(request.POST.get('diastolic_bp', 0)),
                'heart_rate': float(request.POST.get('heart_rate', 0)),
                'temperature_celsius': float(request.POST.get('temperature_celsius', 0)),
                'respiratory_rate': float(request.POST.get('respiratory_rate', 0)),
                'hemoglobin': float(request.POST.get('hemoglobin', 0)),
                'wbc_count': float(request.POST.get('wbc_count', 0)),
                'platelet_count': float(request.POST.get('platelet_count', 0)),
                'creatinine': float(request.POST.get('creatinine', 0)),
                'alt': float(request.POST.get('alt', 0)),
                'ast': float(request.POST.get('ast', 0)),
                'total_bilirubin': float(request.POST.get('total_bilirubin', 0)),
                'albumin': float(request.POST.get('albumin', 0)),
                'hiv_status': 1 if request.POST.get('hiv_status', 'negative') == 'positive' else 0,
                'hbv_status': 1 if request.POST.get('hbv_status', 'negative') == 'positive' else 0,
                'hcv_status': 1 if request.POST.get('hcv_status', 'negative') == 'positive' else 0,
                'cmv_status': 1 if request.POST.get('cmv_status', 'negative') == 'positive' else 0,
                'ebv_status': 1 if request.POST.get('ebv_status', 'negative') == 'positive' else 0,
                'diabetes': 1 if request.POST.get('diabetes', 'no') == 'yes' else 0,
                'hypertension': 1 if request.POST.get('hypertension', 'no') == 'yes' else 0,
                'cardiac_disease': 1 if request.POST.get('cardiac_disease', 'no') == 'yes' else 0,
                'cancer_history': 1 if request.POST.get('cancer_history', 'no') == 'yes' else 0,
                'organ_type': request.POST.get('organ_type', 'Unknown'),
                'organ_condition_score': float(request.POST.get('organ_condition_score', 0))
            }

            logger.debug(f"Extracted form data: {data}")
            
            # This Will Ensure required fields are present for prediction
            input_df = pd.DataFrame([data])

            # This Will Ensure only feature columns are used (exclude target variable)
            feature_columns = [col for col in input_df.columns if col != 'donation_status']
            input_df = input_df[feature_columns]
            logger.debug(f"DataFrame for prediction: {input_df}")
            
            logger.debug(f"Model expected features: {model.feature_names_in_}")
            logger.debug(f"Input DataFrame features: {input_df.columns}")

            # Perform the prediction
            prediction_result = model.predict(input_df)[0]
            logger.debug(f"Prediction result: {prediction_result}")
            
            # Map prediction to readable output
            data['prediction_result'] = 'eligible' if prediction_result == 1 else 'not eligible'
            data['donation_status'] = prediction_result
            # Save to database
            record = PredictionRecord(**data)
            record.user = request.user
            record.save()
            logger.info("Prediction record saved successfully.")
            
            # Create result context with proper formatting
            result = {
                'eligibility': 'Eligible' if prediction_result == 1 else 'Not Eligible',
                'compatibility_score': 85 if prediction_result == 1 else 35,  # Mock score for now
                'assessment_date': record.created_at.strftime('%B %d, %Y') if hasattr(record, 'created_at') else 'Recently completed',
                'organ_type': record.organ_type,
                'medical_notes': 'Your medical profile has been thoroughly analyzed for compatibility factors.',
                'genetic_notes': 'Genetic compatibility has been assessed based on your profile information.',
                'risk_notes': 'Comprehensive risk assessment completed with safety protocols in place.'
            }
            
            return render(request, 'DonorResult.html', {
                'record': record, 
                'result': result,
                'message': 'Success!'
            })
        
        except Exception as e:
            logger.error(f"Error in donor prediction: {str(e)}", exc_info=True)
            return render(request, 'DonorPredict.html', {'error_message': f'Error: {str(e)}'})
    
    return render(request, 'DonorPredict.html')



# Set up logging
logger = logging.getLogger(__name__)
User = get_user_model()
@login_required
@csrf_exempt
def donor_Applicants(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Log incoming request data for debugging
            logger.debug(f"Received POST data: {data}")

            # Ensure user_id is present in the incoming data
            user_id = data.get('user_id')
            if not user_id:
                logger.error("user_id not found in request data")
                return JsonResponse({'error': 'user_id is required'}, status=400)

            # Fetch the UserProfile instance by the user_id
            try:
                user_instance = UserProfile.objects.get(id=user_id)
                logger.debug(f"User found: {user_instance}")
            except UserProfile.DoesNotExist:
                logger.error(f"User with ID {user_id} not found")
                return JsonResponse({'error': 'User not found'}, status=404)

            # Convert gender from 1/0 to 'Male'/'Female'
            gender = 'Male' if data.get('gender') == '1' else 'Female'

            # Convert blood_type from 0-3 to 'A', 'B', 'AB', 'O'
            blood_type_mapping = {
                '0': 'A',
                '1': 'B',
                '2': 'AB',
                '3': 'O'
            }
            blood_type = blood_type_mapping.get(data.get('blood_type'), 'Unknown')  # Default to 'Unknown' if not found
            
            
            # Convert rh_factor from 1/0 to '+'/'-'
            rh_factor = '+' if data.get('rh_factor') == '1' else '-'
            
            # Convert organ_type from '1' to 'Kidney' (you can add more mappings if needed)
            organ_type_mapping = {
                '1': 'Kidney',
                '2': 'Liver',
                '3': 'Heart',
                '4': 'Lungs',
                '5': 'Pancreas'
            }
            organ_type = organ_type_mapping.get(data.get('organ_type'), 'Unknown')

            # Create the donor_Registered object
            donor = donor_Registered.objects.create(
                user=user_instance,  # Assign the UserProfile instance here
                username=data.get('username'),
                contact=data.get('contact', ''),  # Default empty string if contact not provided
                email=data.get('email'),
                age=float(data.get('age')),  # Ensure age is a float
                gender=gender,  # Set the gender to 'Male' or 'Female'
                blood_type=blood_type,  # Convert and set the blood type
                rh_factor=rh_factor,  # Convert and set the rh_factor
                address=data.get('address', ''),  # Default empty string if address not provided
                eligibility=data.get('eligibility'),
                 organ_type=organ_type
            )

            logger.info(f"Donor saved successfully: {donor}")
            send_mail(
                subject='Donor Registration Confirmation',
                message=(
                    f"Dear {user_instance.username},\n\n"
                    f"Thank you for registering as an organ donor. Below are your registration details:\n\n"
                    f"Username: {data.get('username')}\n"
                    f"Contact: {data.get('contact', 'Not provided')}\n"
                    f"Email: {data.get('email')}\n"
                    f"Age: {data.get('age')}\n"
                    f"Gender: {gender}\n"
                    f"Blood Type: {blood_type} {rh_factor}\n"
                    f"Address: {data.get('address', 'Not provided')}\n\n"
                    f"We deeply appreciate your selfless decision to contribute to saving lives. "
                    f"Your generosity and compassion make a significant impact.\n\n"
                    f"Should you have any questions or need further assistance, please do not hesitate to contact us.\n\n"
                    f"Best regards,\n"
                    f"LifeChain Team"
                ),
                from_email=EMAIL_HOST_USER,
                recipient_list=[user_instance.email],
                fail_silently=False
            )
            return JsonResponse({'message': 'Donor saved successfully'})

        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


# Fetching All Eligible Donors 
# @login_required
# def fetch_eligible_donors(request):
#     try:
        
#         eligible_donors = donor_Registered.objects.filter(eligibility='Eligible', is_allocated=False)
#         donors_data = [
#             {
#                 'id': donor.id,
#                 'username': donor.username,
#                 'contact': donor.contact,
#                 'email': donor.email,
#                 'age': donor.age,
#                 'gender': donor.gender,
#                 'blood_type': donor.blood_type,
#                 'rh_factor': donor.rh_factor,
#                 'organ_type': donor.organ_type,
#                 'address': donor.address,
#                 'eligibility': donor.eligibility,
#             }
#             for donor in eligible_donors
#         ]

#         # Return the data as JSON response
#         return JsonResponse(donors_data, safe=False)
#     except Exception as e:
#         # Log the error and return an error response
#         logger.error(f"Error fetching eligible donors: {str(e)}")
#         return JsonResponse({'error': str(e)}, status=500)
    

@login_required
def DonorResultpage(request):
    # Check if user has a prediction record
    if PredictionRecord.objects.filter(user=request.user).exists():
        record = PredictionRecord.objects.get(user=request.user)
        
        # Create result context for existing prediction
        result = {
            'eligibility': 'Eligible' if record.donation_status == 1 else 'Not Eligible',
            'compatibility_score': 85 if record.donation_status == 1 else 35,
            'assessment_date': record.created_at.strftime('%B %d, %Y') if hasattr(record, 'created_at') else 'Previously completed',
            'organ_type': record.organ_type,
            'medical_notes': 'Your medical profile has been thoroughly analyzed for compatibility factors.',
            'genetic_notes': 'Genetic compatibility has been assessed based on your profile information.',
            'risk_notes': 'Comprehensive risk assessment completed with safety protocols in place.'
        }
        
        return render(request, 'DonorResult.html', {
            'record': record,
            'result': result
        })
    else:
        # No prediction record found
        messages.warning(request, "No prediction record found. Please complete a compatibility assessment first.")
        return redirect('donorpridict')


