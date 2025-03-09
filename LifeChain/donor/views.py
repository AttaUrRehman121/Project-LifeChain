import os
import pickle

import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import Http404
from django.views.decorators.csrf import csrf_protect
import joblib
from.models import PredictionRecord
import logging

# Create your views here.

# Donor Home Page 
def donorpage(request):
    return render(request, 'donorPage.html')




# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

base_dir = os.path.dirname(os.path.abspath(__file__))
model_file_path = os.path.join(base_dir, 'MLmodel', 'donor_decision_tree.pkl')
# model_file_path = os.path.join(base_dir, 'MLmodel', 'donor_random_for
model = joblib.load(model_file_path)

# print('Donor model features are:', model.feature_names_in_)
# print('Donor model classes are:', model.classes_)
blood_type_mapping = {'A': 0, 'B': 1, 'AB': 2, 'O': 3}

@csrf_protect
def donorpridict(request):
    if request.method == 'POST':
        try:
            logger.debug("Received POST request for donor prediction.")
            
            # Extract and transform form data
            data = {
                'age': float(request.POST.get('age', 0)),
                'gender': 1 if request.POST.get('gender') == 'M' else 0,
                'blood_type': blood_type_mapping[request.POST.get('blood_type')],
                'rh_factor': 1 if request.POST.get('rh_factor') == 'positive' else 0,
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
            
            # Ensure required fields are present for prediction
            input_df = pd.DataFrame([data])

            # Ensure only feature columns are used (exclude target variable)
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
            record.save()
            logger.info("Prediction record saved successfully.")
            
            return render(request, 'DonorResult.html', {'record': record, 'message': 'Success!'})
        
        except Exception as e:
            logger.error(f"Error in donor prediction: {str(e)}", exc_info=True)
            return render(request, 'DonorPredict.html', {'error_message': f'Error: {str(e)}'})
    
    return render(request, 'DonorPredict.html')


# @csrf_protect
# def donorpridict(request):
#     if request.method == 'POST':
#         try:
#             # Extract and transform form data
#             data = {
#                 'age': float(request.POST.get('age')),
#                 'gender': 1 if request.POST.get('gender') == 'M' else 0,
#                 'blood_type': request.POST.get('blood_type'),
#                 'rh_factor': 1 if request.POST.get('rh_factor') == 'positive' else 0,
#                 'height_cm': float(request.POST.get('height_cm')),
#                 'weight_kg': float(request.POST.get('weight_kg')),
#                 'bmi': float(request.POST.get('bmi')),
#                 'systolic_bp': float(request.POST.get('systolic_bp')),
#                 'diastolic_bp': float(request.POST.get('diastolic_bp')),
#                 'heart_rate': float(request.POST.get('heart_rate')),
#                 'temperature_celsius': float(request.POST.get('temperature_celsius')),
#                 'respiratory_rate': float(request.POST.get('respiratory_rate')),
#                 'hemoglobin': float(request.POST.get('hemoglobin')),
#                 'wbc_count': float(request.POST.get('wbc_count')),
#                 'platelet_count': float(request.POST.get('platelet_count')),
#                 'creatinine': float(request.POST.get('creatinine')),
#                 'alt': float(request.POST.get('alt')),
#                 'ast': float(request.POST.get('ast')),
#                 'total_bilirubin': float(request.POST.get('total_bilirubin')),
#                 'albumin': float(request.POST.get('albumin')),
#                 'hiv_status': 1 if request.POST.get('hiv_status', 'negative') == 'positive' else 0,
#                 'hbv_status': 1 if request.POST.get('hbv_status', 'negative') == 'positive' else 0,
#                 'hcv_status': 1 if request.POST.get('hcv_status', 'negative') == 'positive' else 0,
#                 'cmv_status': 1 if request.POST.get('cmv_status', 'negative') == 'positive' else 0,
#                 'ebv_status': 1 if request.POST.get('ebv_status', 'negative') == 'positive' else 0,
#                 'diabetes': 1 if request.POST.get('diabetes', 'no') == 'yes' else 0,
#                 'hypertension': 1 if request.POST.get('hypertension', 'no') == 'yes' else 0,
#                 'cardiac_disease': 1 if request.POST.get('cardiac_disease', 'no') == 'yes' else 0,
#                 'cancer_history': 1 if request.POST.get('cancer_history', 'no') == 'yes' else 0,
#                 'organ_type': request.POST.get('organ_type'),
#                 'organ_condition_score': float(request.POST.get('organ_condition_score')),
#             }

#             # Set default values for fields not provided by the form
#             data['donation_status'] = 0  # Default donation_status
#             data['prediction_result'] = ''  # Leave prediction result empty since we're not calling the model

#             result = model.predict(pd.DataFrame([data]))
#             data['prediction_result'] = 'eligible' if result == 1 else 'not eligible'
#             # Create and save the record
#             record = PredictionRecord(**data)
#             record.save()
            
#             # Render the DonorResult page with the saved record and a success message
#             return render(request, 'DonorResult.html', {'record': record, 'message': 'Success!'})
#         except Exception as e:
#             # Render the input form with the error message if something goes wrong
#             return render(request, 'DonorPredict.html', {'error_message': f'Error: {str(e)}'})
#     # Render the prediction form on GET request
#     return render(request, 'DonorPredict.html')

def DonorResultpage(request):
    return render(request, 'DonorResult.html')


