from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('', lambda request: redirect('login')),              
    path('home/', views.home_view, name='home'),              
    path('login/', views.login_view, name='login'),           
    path('signup/', views.signup_view, name='signup'),        
    path('logout/', views.logout_view, name='logout'),      
    path('about/', views.about_us, name='about'),             
    path('contact/', views.contact_us, name='contact'),       
]
