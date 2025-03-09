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

# Create your views here.

# Donor Home Page 
def donorpage(request):
    return render(request, 'donorPage.html')


# Load the model
# base_dir = os.path.dirname(os.path.abspath(__file__))
# model_file_path = os.path.join(base_dir, 'MLmodel', 'donor_decision_tree.pkl')

# try:
#     model = joblib.load(model_file_path)
#     print("Loaded model type:", type(model))
#     # Print model features
#     print("Model features:", model.feature_names_in_)
#     # Example input data
#     # Define categorical mappings
#     blood_type_mapping = {'A': 0, 'B': 1, 'AB': 2, 'O': 3}
#     organ_type_mapping = {'Kidney': 0, 'Liver': 1, 'Heart': 2, 'Lung': 3}

#     example_data = {
#         'age': 30.0,
#         'gender': 1,
#         'blood_type': blood_type_mapping['B'],
#         'rh_factor': 0,
#         'height_cm': 176.0,
#         'weight_kg': 70.0,
#         'bmi': 26.0,
#         'systolic_bp': 120.0,
#         'diastolic_bp': 80.0,
#         'heart_rate': 75.0,
#         'temperature_celsius': 38.0,
#         'respiratory_rate': 16.0,
#         'hemoglobin': 13.0,
#         'wbc_count': 7000.0,
#         'platelet_count': 250000.0,
#         'creatinine': 12.0,
#         'alt': 25.0,
#         'ast': 30.0,
#         'total_bilirubin': 1.2,
#         'albumin': 3.5,
#         'hiv_status': 1,
#         'hbv_status': 0,
#         'hcv_status': 0,
#         'cmv_status': 0,
#         'ebv_status': 0,
#         'diabetes': 0,
#         'hypertension': 0,
#         'cardiac_disease': 0,
#         'cancer_history': 0,
#         'organ_type': organ_type_mapping['Kidney'],
#         'organ_condition_score': 8.0,
#     }
#     example_df = pd.DataFrame([example_data])
#     example_df = example_df[model.feature_names_in_]
#     print("Example input data:", example_df)
#     # Make prediction with example data
#     prediction = model.predict(example_df)
#     prediction_result = 'eligible' if prediction[0] == 1 else 'not eligible'
#     print("Prediction result for example data:", prediction_result)
# except FileNotFoundError:
#     print(f"Model file not found at {model_file_path}")
#     model = None
# except Exception as e:
#     print(f"Error loading model: {str(e)}")
#     model = None

# @csrf_protect
# def donorpridict(request):
#     if request.method == 'POST':
#         if model is None:
#             return render(request, 'DonorPredict.html', {'error_message': 'Model not loaded. Please check the server logs.'})

#         try:
#             data = {
#                 'age': float(request.POST.get('age')),
#                 'gender': 1 if request.POST.get('gender') == 'M' else 0,
#                 'blood_type': blood_type_mapping[request.POST.get('blood_type')],
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
#                 'organ_type': organ_type_mapping[request.POST.get('organ_type')],
#                 'organ_condition_score': float(request.POST.get('organ_condition_score')),
#                 'prediction_result': 'not predicted'  # Default value
#             }

#             # Save prediction record
#             record = PredictionRecord(**data)
#             record.save()

#             return render(request, 'DonorResult.html', {'record': record, 'message': 'Record saved successfully!'})
#         except Exception as e:
#             return render(request, 'DonorPredict.html', {'error_message': f'An error occurred: {str(e)}'})

#     return render(request, 'DonorPredict.html')

import os
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from .models import PredictionRecord  # Ensure this model exists in your models.py


@csrf_protect
def donorpridict(request):
    if request.method == 'POST':
        try:
            # Extract and transform form data
            data = {
                'age': float(request.POST.get('age')),
                'gender': 1 if request.POST.get('gender') == 'M' else 0,
                'blood_type': request.POST.get('blood_type'),
                'rh_factor': 1 if request.POST.get('rh_factor') == 'positive' else 0,
                'height_cm': float(request.POST.get('height_cm')),
                'weight_kg': float(request.POST.get('weight_kg')),
                'bmi': float(request.POST.get('bmi')),
                'systolic_bp': float(request.POST.get('systolic_bp')),
                'diastolic_bp': float(request.POST.get('diastolic_bp')),
                'heart_rate': float(request.POST.get('heart_rate')),
                'temperature_celsius': float(request.POST.get('temperature_celsius')),
                'respiratory_rate': float(request.POST.get('respiratory_rate')),
                'hemoglobin': float(request.POST.get('hemoglobin')),
                'wbc_count': float(request.POST.get('wbc_count')),
                'platelet_count': float(request.POST.get('platelet_count')),
                'creatinine': float(request.POST.get('creatinine')),
                'alt': float(request.POST.get('alt')),
                'ast': float(request.POST.get('ast')),
                'total_bilirubin': float(request.POST.get('total_bilirubin')),
                'albumin': float(request.POST.get('albumin')),
                'hiv_status': 1 if request.POST.get('hiv_status', 'negative') == 'positive' else 0,
                'hbv_status': 1 if request.POST.get('hbv_status', 'negative') == 'positive' else 0,
                'hcv_status': 1 if request.POST.get('hcv_status', 'negative') == 'positive' else 0,
                'cmv_status': 1 if request.POST.get('cmv_status', 'negative') == 'positive' else 0,
                'ebv_status': 1 if request.POST.get('ebv_status', 'negative') == 'positive' else 0,
                'diabetes': 1 if request.POST.get('diabetes', 'no') == 'yes' else 0,
                'hypertension': 1 if request.POST.get('hypertension', 'no') == 'yes' else 0,
                'cardiac_disease': 1 if request.POST.get('cardiac_disease', 'no') == 'yes' else 0,
                'cancer_history': 1 if request.POST.get('cancer_history', 'no') == 'yes' else 0,
                'organ_type': request.POST.get('organ_type'),
                'organ_condition_score': float(request.POST.get('organ_condition_score')),
            }

            # Set default values for fields not provided by the form
            data['donation_status'] = 0  # Default donation_status
            data['prediction_result'] = ''  # Leave prediction result empty since we're not calling the model

            # Create and save the record
            record = PredictionRecord(**data)
            record.save()
            
            # Render the DonorResult page with the saved record and a success message
            return render(request, 'DonorResult.html', {'record': record, 'message': 'Success!'})
        except Exception as e:
            # Render the input form with the error message if something goes wrong
            return render(request, 'DonorPredict.html', {'error_message': f'Error: {str(e)}'})
    # Render the prediction form on GET request
    return render(request, 'DonorPredict.html')

def DonorResultpage(request):
    return render(request, 'DonorResult.html')


