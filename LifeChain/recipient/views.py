from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Recipient
# Create your views here.
# @login_required
def recipientpage(request):
    return render(request, 'recipientPage.html')
 
 
def recipientprictiction(request):
    if request.method == 'POST':
        try:
            # Get data from the form and convert values as needed
            data = {
                'age': float(request.POST.get('age')),
                'gender': 1 if request.POST.get('gender') == 'male' else 0,
                'blood_type': request.POST.get('blood_type'),
                'rh_factor': 1 if request.POST.get('rh_factor') == 'positive' else 0,
                'height_cm': float(request.POST.get('height_cm')),
                'weight_kg': float(request.POST.get('weight_kg')),
                'bmi': float(request.POST.get('bmi')),
                'wait_list_days': int(request.POST.get('wait_list_days')),
                'medical_urgency_score': float(request.POST.get('medical_urgency_score')),
                'hemoglobin': float(request.POST.get('hemoglobin')),
                'wbc_count': float(request.POST.get('wbc_count')),
                'platelet_count': float(request.POST.get('platelet_count')),
                'creatinine': float(request.POST.get('creatinine')),
                'alt': float(request.POST.get('alt')),
                'ast': float(request.POST.get('ast')),
                'diabetes': 1 if request.POST.get('diabetes') == 'yes' else 0,
                'hypertension': 1 if request.POST.get('hypertension') == 'yes' else 0,
                'previous_transplant': 1 if request.POST.get('previous_transplant') == 'yes' else 0,
                'dialysis_status': 1 if request.POST.get('dialysis_status') == 'yes' else 0,
                'required_organ': request.POST.get('required_organ'),
                'antibody_screen': float(request.POST.get('antibody_screen')),
                'pra_score': float(request.POST.get('pra_score')),
                # Provide default values for required fields not coming from the form.
                'donation_status': 0,              # Default value; update as needed
                'prediction_result': 'not eligible'  # Default value; update as needed
            }

            # Save the data to the database
            record = Recipient(**data)
            record.save()

            # Render the result with a success message
            context = {**data, 'record': record, 'message': 'Prediction record saved successfully!'}
            return render(request, 'DonorResult.html', context)
        except Exception as e:
            # Render the form with an error message if something goes wrong
            context = {'error_message': f'An error occurred: {str(e)}'}
            return render(request, 'DonorPredict.html', context)
    else:  
        return render(request, 'RecipientPrediction.html')


def RecipientResultpage(request):
    return render(request, 'RecipientResultPage.html')

