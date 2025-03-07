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
base_dir = os.path.dirname(os.path.abspath(__file__))
model_file_path = os.path.join(base_dir, 'MLmodel', 'donor_decision_tree.pkl')

try:
    model = joblib.load(model_file_path)
    print("Loaded model type:", type(model))
except FileNotFoundError:
    print(f"Model file not found at {model_file_path}")
    model = None
except Exception as e:
    print(f"Error loading model: {str(e)}")
    model = None

@csrf_protect
def donorpridict(request):
    if request.method == 'POST':
        if model is None:
            return render(request, 'DonorPredict.html', {'error_message': 'Model not loaded. Please check the server logs.'})

        try:
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

            # Expected feature order (must match training data)
            expected_features = [
                'age', 'gender', 'blood_type', 'rh_factor', 'height_cm', 'weight_kg', 'bmi',
                'systolic_bp', 'diastolic_bp', 'heart_rate', 'temperature_celsius', 'respiratory_rate',
                'hemoglobin', 'wbc_count', 'platelet_count', 'creatinine', 'alt', 'ast', 
                'total_bilirubin', 'albumin', 'hiv_status', 'hbv_status', 'hcv_status', 
                'cmv_status', 'ebv_status', 'diabetes', 'hypertension', 'cardiac_disease', 
                'cancer_history', 'organ_type', 'organ_condition_score'
            ]

            # Convert dictionary to DataFrame
            input_df = pd.DataFrame([data])

            # Ensure column order matches training data
            input_df = input_df[expected_features]

            try:
                # Make prediction
                
                prediction = model.predict(input_df)
                print('I;m Here')
                prediction_result = 'eligible' if prediction[0] == 1 else 'not eligible'
                data['prediction_result'] = prediction_result
                print(data['prediction_result'])

                # Save prediction record
                record = PredictionRecord(**data)
                record.save()

                return render(request, 'DonorResult.html', {'record': record, 'message': 'Prediction record saved successfully!'})
            except Exception as e:
                return render(request, 'DonorPredict.html', {'error_message': f'Prediction error: {str(e)}'})

        except Exception as e:
            return render(request, 'DonorPredict.html', {'error_message': f'An error occurred: {str(e)}'})

    return render(request, 'DonorPredict.html')



# # Load the model
# base_dir = os.path.dirname(os.path.abspath(__file__))

# # Construct the path to the model file
# model_file_path = os.path.join(base_dir, 'MLmodel', 'donor_decision_tree.pkl')

# # Load the trained model with exception handling
# try:
#     model = joblib.load(model_file_path)
#     print("Loaded model type:", type(model))  # Debugging statement
# except FileNotFoundError:
#     print(f"Model file not found at {model_file_path}")
#     model = None
# except Exception as e:
#     print(f"Error loading model: {str(e)}")
#     model = None

# print("Loaded model type:", type(model))  # Debugging statement

# @csrf_protect
# def donorpridict(request):
#     if request.method == 'POST':
#         try:
#             # Get data from the form and convert values as needed
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
#                 # Provide default values for required fields not coming from the form.
#                 'donation_status': 0,              # Default value; update as needed
#                 'prediction_result': 'not eligible'  # Default value; update as needed
#             }
            
#             try:
#                 # Make predictions using the loaded model and the input data
#                 prediction = model.predict([data.values()])
#                 prediction_result = 'eligible' if prediction[0] == 1 else 'not eligible'
#                 data['prediction_result'] = prediction_result

#                 # Save the data to the database
#                 record = PredictionRecord(**data)
#                 record.save()

#                 # Render the result with a success message
#                 context = {**data, 'record': record, 'message': 'Prediction record saved successfully!'}
#                 return render(request, 'DonorResult.html', context)
#             except Exception as e:
#                 # Handle prediction errors
#                 context = {'error_message': f'Prediction error: {str(e)}'}
#                 return render(request, 'DonorPredict.html', context)
#         except Exception as e:
#             # Render the form with an error message if something goes wrong
#             context = {'error_message': f'An error occurred: {str(e)}'}
#             return render(request, 'DonorPredict.html', context)
#     else:
#         return render(request, 'DonorPredict.html')
        
        
#         # Load the model

# # Load the model
# base_dir = os.path.dirname(os.path.abspath(__file__))

# # Construct the path to the model file
# model_file_path = os.path.join(base_dir, 'MLmodel', 'donor_decision_tree')

# # Load the trained model with exception handling
# try:
#     model = joblib.load(model_file_path)
#     print("Loaded model type:", type(model))  # Debugging statement
# except FileNotFoundError:
#     print(f"Model file not found at {model_file_path}")
#     model = None
# except Exception as e:
#     print(f"Error loading model: {str(e)}")
#     model = None

# print("Loaded model type:", type(model))  # Debugging statement

# # Define categorical mappings (adjust according to your model's training)
# blood_type_mapping = {'A': 0, 'B': 1, 'AB': 2, 'O': 3}
# organ_type_mapping = {'Liver': 0, 'Kidney': 1, 'Heart': 2, 'Lung': 3}

# @csrf_protect
# def donorpridict(request):
#     if request.method == 'POST':
#         try:
#             # Extract and transform form data
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
#             }

#             # Get model's expected features (adjust if using feature_names_in_)
#             model_features = [
#                 'age', 'gender', 'blood_type', 'rh_factor', 'height_cm', 'weight_kg',
#                 'bmi', 'systolic_bp', 'diastolic_bp', 'heart_rate', 'temperature_celsius',
#                 'respiratory_rate', 'hemoglobin', 'wbc_count', 'platelet_count', 'creatinine',
#                 'alt', 'ast', 'total_bilirubin', 'albumin', 'hiv_status', 'hbv_status',
#                 'hcv_status', 'cmv_status', 'ebv_status', 'diabetes', 'hypertension',
#                 'cardiac_disease', 'cancer_history', 'organ_type', 'organ_condition_score'
#             ]

#             # Prepare input data for prediction
#             input_data = [data[feature] for feature in model_features]

#             # Make prediction
#             prediction = model.predict([input_data])
#             prediction_result = 'eligible' if prediction[0] == 1 else 'not eligible'

#             # Add additional fields for database record
#             data['donation_status'] = 0  # Example default value
#             data['prediction_result'] = prediction_result

#             # Save to database
#             record = PredictionRecord(**data)
#             record.save()

#             # Render result page
#             return render(request, 'DonorResult.html', {'record': record, 'message': 'Success!'})

#         except Exception as e:
#             # Handle errors
#             return render(request, 'DonorPredict.html', {'error_message': f'Error: {str(e)}'})
    
#     return render(request, 'DonorPredict.html')


def DonorResultpage(request):
    return render(request, 'DonorResult.html')


