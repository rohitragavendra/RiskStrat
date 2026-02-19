from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

class Assessment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assessments', null=True, blank=True)
    
    # Personal Details
    full_name = models.CharField(max_length=255, blank=True)
    age = models.CharField(max_length=10, blank=True)
    gender = models.CharField(max_length=20, blank=True)
    region = models.CharField(max_length=100, blank=True)
    
    # Physical Parameters
    height = models.CharField(max_length=10, blank=True)
    weight = models.CharField(max_length=10, blank=True)
    bmi = models.CharField(max_length=10, blank=True)
    
    # Dietary Habits
    fruit_veg_intake = models.CharField(max_length=50, blank=True)
    processed_food_intake = models.CharField(max_length=50, blank=True)
    dietary_habits = models.TextField(blank=True) # JSON or Comma separated
    
    # Lifestyle Habits
    physical_activity_level = models.CharField(max_length=50, blank=True)
    average_sleep_time = models.CharField(max_length=50, blank=True)
    smoking_habit = models.CharField(max_length=50, blank=True)
    alcohol_consumption = models.CharField(max_length=50, blank=True)
    
    # Symptoms
    symptoms = models.TextField(blank=True) # JSON or Comma separated list of all selected symptoms
    
    # Medical History
    medical_history = models.TextField(blank=True) # JSON or Comma separated list of all selected medical history
    
    # Result
    risk_level = models.CharField(max_length=50, blank=True)
    risk_message = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Assessment for {self.user} at {self.created_at}"
