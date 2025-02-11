import os
import pickle
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import Http404
from django.views.decorators.csrf import csrf_protect

 
from.models import PredictionRecord

# Create your views here.

# Donor Home Page 
def donorpage(request):
    return render(request, 'donorPage.html')


# Load the model
# Correctly build the model path (avoid backslash issues)
model_path = os.path.join(os.path.dirname(__file__), 'MLmodel', 'donor_decision_tree_96.pkl')
with open(model_path, 'rb') as file:
    loaded_object = pickle.load(file)
    # If the pickle file is a dict containing the model, use the 'model' key.
    if isinstance(loaded_object, dict) and 'model' in loaded_object:
        model = loaded_object['model']
    else:
        model = loaded_object

print("Loaded model type:", type(model))  # Debugging statement

@csrf_protect
def donorpridict(request):
    if request.method == 'POST':
        try:
            # Get data from the form and convert values as needed
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
                'hiv_status': 1 if request.POST.get('hiv_status') == 'positive' else 0,
                'hbv_status': 1 if request.POST.get('hbv_status') == 'positive' else 0,
                'hcv_status': 1 if request.POST.get('hcv_status') == 'positive' else 0,
                'cmv_status': 1 if request.POST.get('cmv_status') == 'positive' else 0,
                'ebv_status': 1 if request.POST.get('ebv_status') == 'positive' else 0,
                'diabetes': 1 if request.POST.get('diabetes') == 'yes' else 0,
                'hypertension': 1 if request.POST.get('hypertension') == 'yes' else 0,
                'cardiac_disease': 1 if request.POST.get('cardiac_disease') == 'yes' else 0,
                'cancer_history': 1 if request.POST.get('cancer_history') == 'yes' else 0,
                'organ_type': request.POST.get('organ_type'),
                'organ_condition_score': float(request.POST.get('organ_condition_score')),
                # Provide default values for required fields not coming from the form.
                'donation_status': 0,              # Default value; update as needed
                'prediction_result': 'not eligible'  # Default value; update as needed
            }

            # Save the data to the database
            record = PredictionRecord(**data)
            record.save()

            # Render the result with a success message
            context = {**data, 'record': record, 'message': 'Prediction record saved successfully!'}
            return render(request, 'DonorResult.html', context)
        except Exception as e:
            # Render the form with an error message if something goes wrong
            context = {'error_message': f'An error occurred: {str(e)}'}
            return render(request, 'DonorPredict.html', context)
    else:
        return render(request, 'DonorPredict.html')
# Result Page of Prediction 

def DonorResultpage(request):
    return render(request, 'DonorResult.html')


