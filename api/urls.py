from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('save-assessment/', views.save_assessment, name='save_assessment'),
    path('start-assessment/', views.start_assessment, name='start_assessment'),
    path('save-physical-parameters/', views.save_physical_parameters, name='save_physical_parameters'),
    path('save-dietary-habits/', views.save_dietary_habits, name='save_dietary_habits'),
    path('save-lifestyle-habits/', views.save_lifestyle_habits, name='save_lifestyle_habits'),
    path('save-symptoms/', views.save_symptoms, name='save_symptoms'),
    path('save-medical-history/', views.save_medical_history, name='save_medical_history'),
    path('get-assessment-details/', views.get_assessment_details, name='get_assessment_details'),
    path('update-personal-details/', views.update_personal_details, name='update_personal_details'),
    path('submit-assessment/', views.submit_assessment, name='submit_assessment'),
    path('history/', views.get_user_history, name='get_user_history'),
    path('profile/', views.get_user_profile, name='get_user_profile'),
    path('profile/update/', views.update_user_profile, name='update_user_profile'),
    path('change-password/', views.change_password, name='change_password'),
]
