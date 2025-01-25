from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse
# from django.template.loader import get_template
# from weasyprint import HTML
# import tempfile



import prediction
from .forms import ForgotPasswordForm, PasswordResetForm
from .models import User
from .forms import RegistrationForm, PredictionForm
from .models import PredictionHistory
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm
import pickle
import numpy as np
import pandas as pd


# Load the model and scaler
with open(r'E:\HOuse_p\HOUSEPRICE7thSemProjekt\houseprice\prediction\best_rf_model.pkl', 'rb') as model_file:
    best_rf_model = pickle.load(model_file)
    # Check if the loaded object is a numpy array (indicating the wrong format)
    if isinstance(best_rf_model, np.ndarray):
        print("The model is incorrectly saved as a numpy array. This is not a valid model.")
        # Handle error or provide fallback logic here
        best_rf_model = None  # or load a model from another source

with open(r'E:\HOuse_p\HOUSEPRICE7thSemProjekt\houseprice\prediction\scaler.pkl', 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)
    # Check if the loaded object is a numpy array (indicating the wrong format)
    if isinstance(scaler, np.ndarray):
        print("The scaler is incorrectly saved as a numpy array. This is not a valid scaler.")
        # Handle error or provide fallback logic here
        scaler = None  # or load a scaler from another source


def model_predict_price(features):
    # Check if the model and scaler are correctly loaded
    if best_rf_model is None or scaler is None:
        raise ValueError("Model or Scaler is not correctly loaded. Please verify the pickle files.")

    # Perform prediction using the model
    scaled_price_pred = best_rf_model.predict(features)

    # If scaler is loaded correctly, inverse transform the predicted prices
    if scaler:
        price_pred_actual = scaler.inverse_transform(np.array(scaled_price_pred).reshape(-1, 1))
        return price_pred_actual[0][0]
    else:
        raise ValueError("Scaler is not available for inverse transformation.")



@login_required
def home(request):
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            # Get input features from the form
            number_of_rooms = form.cleaned_data['number_of_rooms']
            number_of_bathrooms = form.cleaned_data['number_of_bathrooms']
            number_of_floors = form.cleaned_data['number_of_floors']
            area = form.cleaned_data['area']
            road_width = form.cleaned_data['road_width']
            amenities_count = form.cleaned_data['amenities_count']
            city = form.cleaned_data['city']
            road_type = form.cleaned_data['road_type']

            # Create a DataFrame for input features
            input_features = pd.DataFrame([{
                'Bedroom': number_of_rooms,
                'Bathroom': number_of_bathrooms,
                'Floors': number_of_floors,
                'Area': area,
                'Road Width': road_width,
                'Amenities_Count': amenities_count,
                'City_Bhaktapur': int(city == 'Bhaktapur'),
                'City_Kathmandu': int(city == 'Kathmandu'),
                'City_Lalitpur': int(city == 'Lalitpur'),
                'Road Type_Blacktopped': int(road_type == 'Blacktopped'),
                'Road Type_Gravelled': int(road_type == 'Gravelled'),
                'Road Type_Soil Stabilized': int(road_type == 'Soil Stabilized')
            }])

            # Get the predicted price
            try:
                predicted_price = model_predict_price(input_features)
            except ValueError as e:
                return render(request, 'home.html', {
                    'form': form,
                    'error_message': str(e)
                })

            # Save prediction to history
            PredictionHistory.objects.create(
                user=request.user,
                number_of_rooms=number_of_rooms,
                number_of_bathrooms=number_of_bathrooms,
                number_of_floors=number_of_floors,
                area=area,
                road_width=road_width,
                amenities_count=amenities_count,
                city=city,
                road_type=road_type,
                predicted_price=predicted_price
            )

            return render(request, 'home.html', {
                'form': form,
                'predicted_price': predicted_price
            })

    else:
        form = PredictionForm()
    return render(request, 'home.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Redirect to 'next' if provided, or default to 'home' page
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})



# Prediction History View
@login_required
def history(request):
    # Get the current logged-in user
    user = request.user

    # Filter predictions by the logged-in user and order by prediction_date
    user_predictions = PredictionHistory.objects.filter(user=user).order_by('-prediction_date')

    return render(request, 'history.html', {'predictions': user_predictions})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def forgot_password(request):
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            try:
                # Check if a user exists with matching username, first name, and last name
                user = User.objects.get(username=username, first_name=first_name, last_name=last_name)
                # If the user exists, redirect to the password reset page
                return redirect('password_reset', username=user.username)
            except User.DoesNotExist:
                # If no user is found with the provided details, show an error message
                messages.error(request, "Invalid name, first name, last name, or username.")
                return render(request, 'forgot_password.html', {'form': form})
            
    else:
        form = ForgotPasswordForm()

    return render(request, 'forgot_password.html', {'form': form})


def password_reset(request, username):
    user = User.objects.get(username=username)
    error = None
    success = None

    if request.method == "POST":
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            error = "Passwords do not match. Please try again."
            
        elif len(new_password) < 8:
            error = "Password must be at least 8 characters long."
            
        else:
            # Update the user's password
            user.password = make_password(new_password)
            user.save()
            success = "Password successfully reset!"
            return redirect('login')  # Redirect to the login page after a successful reset

    return render(request, 'reset_password.html', {'username': username, 'error': error, 'success': success})

# GEnerate PDF
# def generate_pdf(request):
#     # Fetch predictions from the database (Example queryset)
#     predictions = PredictionHistory.objects.filter(user=request.user)

#     # Load the template and render it
#     template = get_template('history.html')  # Your HTML template file
#     html_content = template.render({'predictions': predictions, 'request': request})

#     # Generate the PDF
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="prediction_history.pdf"'

#     # Use WeasyPrint to create PDF
#     HTML(string=html_content).write_pdf(response)
#     return response