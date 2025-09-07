from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

import os
import pickle

from predictor.utils.apis import fetch_data

try:
    model_path = os.path.join(os.path.dirname(__file__), 'saved_models', 'lgbm_final_model (10).pkl')
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
except Exception as e:
    model = None
    print("Model loading failed:", e)

# Sign Up View
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('signup')

        user = User.objects.create_user(username=username, password=password)
        user.save()
        messages.success(request, "Account created successfully!")
        return redirect('login')

    return render(request, 'signup.html')

# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'login.html')

    return render(request, 'login.html')

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

# Home/Dashboard View
@login_required(login_url='login')
def home_view(request):
    if request.method == 'POST':
        city_name = request.POST.get('city', '').strip()

        try:
        
            input_data, input_df = fetch_data(city_name)

            if model:
                raw_prediction = model.predict(input_df)[0]

                prediction = max(0, int(round(raw_prediction)))
            else:
                prediction = "Model not available."

            return render(request, 'home.html', {
                'prediction': prediction,
                'city': city_name,
                'parameters': input_data
            })

        except Exception as e:
            print("Error during prediction:", e)
            messages.error(request, "Failed to fetch or predict data. Please try again later.")
            return redirect('home')

    return render(request, 'home.html')


def about_us(request):
    return render(request, 'about.html')

def contact_us(request):
    return render(request, 'contact.html')
