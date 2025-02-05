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
model_path = os.path.join(os.path.dirname(__file__), '../static/ML_Models/donor_decision_tree_96.pkl')
with open(model_path, 'rb') as file:
    loaded_object = pickle.load(file)
    if isinstance(loaded_object, dict) and 'model' in loaded_object:
        model = loaded_object['model']
    else:
        model = loaded_object

print("Loaded model type:", type(model))  # Debugging statement

@csrf_protect
def donorpridict(request):
    if request.method == 'POST':
        # Get data from the form
        data = {
            'age': float(request.POST.get('age')),
            'gender': request.POST.get('gender'),
            'blood_type': request.POST.get('blood_type'),
            'rh_factor': request.POST.get('rh_factor'),
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
            'hiv_status': request.POST.get('hiv_status'),
            'hbv_status': request.POST.get('hbv_status'),
            'hcv_status': request.POST.get('hcv_status'),
            'cmv_status': request.POST.get('cmv_status'),
            'ebv_status': request.POST.get('ebv_status'),
            'diabetes': request.POST.get('diabetes'),
            'hypertension': request.POST.get('hypertension'),
            'cardiac_disease': request.POST.get('cardiac_disease'),
            'cancer_history': request.POST.get('cancer_history'),
            'organ_type': request.POST.get('organ_type'),
            'organ_condition_score': float(request.POST.get('organ_condition_score')),
        }

        # Prepare the data for prediction
        input_data = [[
            data['age'], data['gender'], data['blood_type'], data['rh_factor'],
            data['height_cm'], data['weight_kg'], data['bmi'],
            data['systolic_bp'], data['diastolic_bp'], data['heart_rate'],
            data['temperature_celsius'], data['respiratory_rate'], data['hemoglobin'],
            data['wbc_count'], data['platelet_count'], data['creatinine'],
            data['alt'], data['ast'], data['total_bilirubin'], data['albumin'],
            data['hiv_status'], data['hbv_status'], data['hcv_status'], data['cmv_status'],
            data['ebv_status'], data['diabetes'], data['hypertension'],
            data['cardiac_disease'], data['cancer_history'], data['organ_type'],
            data['organ_condition_score']
        ]]
    
        # Make prediction
        prediction = model.predict(input_data)
        donation_status = 'eligible' if prediction[0] == 1 else 'not eligible'
        
        print(f"Prediction: {prediction}, Donation Status: {donation_status}")
    
        # Save the data and prediction result to the database
        record = PredictionRecord(**data, donation_status=donation_status, prediction_result=donation_status)
        record.save()
    
        # Render the result in HTML
        context = {**data, 'prediction': donation_status, 'record': record}
        return render(request, 'result.html', context)
    else:
        return render(request, 'DonorPredict.html')
def download_pdf(request, record_id):
    # Fetch the record from the database
    record = PredictionRecord.objects.get(id=record_id)

    # Render the HTML template with the record data
    html_string = render_to_string('pdf_template.html', {'record': record})

    # # Create a PDF using WeasyPrint
    # html = HTML(string=html_string)
    # pdf_file = html.write_pdf()

    return render(request, 'DonorPredict.html')

# Result Page of Prediction 
def DonorResultpage(request):
    return render(request, 'RecipientResultPage.html')