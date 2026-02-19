from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer, LoginSerializer, AssessmentSerializer, UserProfileSerializer
from .models import Assessment
from rest_framework.authtoken.models import Token # Optional if using Token Auth, but for now simple response

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            "message": "User registered successfully",
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name
            }
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data
        # You could generate a token here (JWT or DRF Token)
        return Response({
            "message": "Login successful",
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name
            }
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def save_assessment(request):
    data = request.data.copy()
    user_id = data.get('user_id')
    
    # If user_id is provided, try to find the user instance
    if user_id:
        try:
            from .models import CustomUser
            user = CustomUser.objects.get(pk=user_id)
            # We can't direct assign to serializer field if it's not in fields or read_only
            # But we can pass it to save()
        except CustomUser.DoesNotExist:
            user = None
    else:
        user = None

    serializer = AssessmentSerializer(data=data)
    if serializer.is_valid():
        assessment = serializer.save(user=user)
        return Response({
            "message": "Assessment saved successfully",
            "id": assessment.id
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def start_assessment(request):
    """
    Starts a new assessment with personal details.
    """
    data = request.data.copy()
    user_id = data.get('user_id')
    
    # Optional: link to user if logged in
    user = None
    if user_id:
        try:
            from .models import CustomUser
            user = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            pass

    # Create assessment with just personal details
    # We use validation from serializer but allow partial since other fields are empty initially
    # actually, for a new assessment, other fields ARE blank=True in model, so full validator works?
    # No, because blank=True in model doesn't mean optional in serializer necessarily if required=True default.
    # But ModelSerializer usually respects blank=True.
    
    serializer = AssessmentSerializer(data=data)
    if serializer.is_valid():
        assessment = serializer.save(user=user)
        return Response({
            "message": "Assessment started successfully",
            "assessment_id": assessment.id
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def save_physical_parameters(request):
    """
    Updates an existing assessment with physical parameters.
    """
    data = request.data
    assessment_id = data.get('assessment_id')
    
    if not assessment_id:
        return Response({"error": "assessment_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        assessment = Assessment.objects.get(pk=assessment_id)
    except Assessment.DoesNotExist:
         return Response({"error": "Assessment not found"}, status=status.HTTP_404_NOT_FOUND)

    # Update fields
    assessment.height = data.get('height', assessment.height)
    assessment.weight = data.get('weight', assessment.weight)
    assessment.bmi = data.get('bmi', assessment.bmi)
    
    assessment.save()
    
    return Response({
        "message": "Physical parameters saved successfully",
        "assessment_id": assessment.id
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def save_dietary_habits(request):
    """
    Updates an existing assessment with dietary habits.
    """
    data = request.data
    assessment_id = data.get('assessment_id')
    
    if not assessment_id:
        return Response({"error": "assessment_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        assessment = Assessment.objects.get(pk=assessment_id)
    except Assessment.DoesNotExist:
         return Response({"error": "Assessment not found"}, status=status.HTTP_404_NOT_FOUND)

    # Update fields
    assessment.fruit_veg_intake = data.get('fruit_veg_intake', assessment.fruit_veg_intake)
    assessment.processed_food_intake = data.get('processed_food_intake', assessment.processed_food_intake)
    
    # dietary_habits is a list in request, but TextField in model. Join if list.
    habits = data.get('dietary_habits', [])
    if isinstance(habits, list):
        assessment.dietary_habits = ", ".join(habits)
    else:
        assessment.dietary_habits = str(habits)
    
    assessment.save()
    
    return Response({
        "message": "Dietary habits saved successfully",
        "assessment_id": assessment.id
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def save_lifestyle_habits(request):
    """
    Updates an existing assessment with lifestyle habits.
    """
    data = request.data
    assessment_id = data.get('assessment_id')
    
    if not assessment_id:
        return Response({"error": "assessment_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        assessment = Assessment.objects.get(pk=assessment_id)
    except Assessment.DoesNotExist:
         return Response({"error": "Assessment not found"}, status=status.HTTP_404_NOT_FOUND)

    # Update fields
    assessment.physical_activity_level = data.get('physical_activity_level', assessment.physical_activity_level)
    assessment.average_sleep_time = data.get('average_sleep_time', assessment.average_sleep_time)
    assessment.smoking_habit = data.get('smoking_habit', assessment.smoking_habit)
    assessment.alcohol_consumption = data.get('alcohol_consumption', assessment.alcohol_consumption)
    
    assessment.save()
    
    return Response({
        "message": "Lifestyle habits saved successfully",
        "assessment_id": assessment.id
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def save_symptoms(request):
    """
    Updates an existing assessment with selected symptoms.
    """
    data = request.data
    assessment_id = data.get('assessment_id')
    
    if not assessment_id:
        return Response({"error": "assessment_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        assessment = Assessment.objects.get(pk=assessment_id)
    except Assessment.DoesNotExist:
         return Response({"error": "Assessment not found"}, status=status.HTTP_404_NOT_FOUND)

    # Update fields
    symptoms = data.get('symptoms', [])
    if isinstance(symptoms, list):
        assessment.symptoms = ", ".join(symptoms)
    else:
        assessment.symptoms = str(symptoms)
    
    assessment.save()
    
    return Response({
        "message": "Symptoms saved successfully",
        "assessment_id": assessment.id
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def save_medical_history(request):
    """
    Updates an existing assessment with medical history.
    """
    data = request.data
    assessment_id = data.get('assessment_id')
    
    if not assessment_id:
        return Response({"error": "assessment_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        assessment = Assessment.objects.get(pk=assessment_id)
    except Assessment.DoesNotExist:
         return Response({"error": "Assessment not found"}, status=status.HTTP_404_NOT_FOUND)

    # Update fields
    medical_history = data.get('medical_history', [])
    if isinstance(medical_history, list):
        assessment.medical_history = ", ".join(medical_history)
    else:
        assessment.medical_history = str(medical_history)
    
    assessment.save()
    
    return Response({
        "message": "Medical history saved successfully",
        "assessment_id": assessment.id
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_assessment_details(request):
    """
    Get details of a specific assessment.
    """
    assessment_id = request.query_params.get('assessment_id')
    
    if not assessment_id:
        return Response({"error": "assessment_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        assessment = Assessment.objects.get(pk=assessment_id)
        serializer = AssessmentSerializer(assessment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Assessment.DoesNotExist:
         return Response({"error": "Assessment not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([AllowAny])
def update_personal_details(request):
    """
    Update personal details of an existing assessment.
    """
    data = request.data
    assessment_id = data.get('assessment_id')
    
    if not assessment_id:
        return Response({"error": "assessment_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        assessment = Assessment.objects.get(pk=assessment_id)
    except Assessment.DoesNotExist:
         return Response({"error": "Assessment not found"}, status=status.HTTP_404_NOT_FOUND)

    # Update fields
    assessment.full_name = data.get('full_name', assessment.full_name)
    assessment.age = data.get('age', assessment.age)
    assessment.gender = data.get('gender', assessment.gender)
    assessment.region = data.get('region', assessment.region)
    
    assessment.save()
    
    return Response({
        "message": "Personal details updated successfully",
        "assessment_id": assessment.id
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_history(request):
    user_id = request.query_params.get('user_id')
    if not user_id:
        return Response({"error": "user_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    assessments = Assessment.objects.filter(user_id=user_id).order_by('-created_at')
    serializer = AssessmentSerializer(assessments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def submit_assessment(request):
    """
    Finalizes the assessment, calculates risk, and saves the result.
    """
    print(f"DEBUG: submit_assessment called with data: {request.data}")
    data = request.data
    assessment_id = data.get('assessment_id')
    user_id = data.get('user_id') # Optional, to link if not already linked
    
    if not assessment_id:
        print("DEBUG: assessment_id missing")
        return Response({"error": "assessment_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        assessment = Assessment.objects.get(pk=assessment_id)
        print(f"DEBUG: Assessment found: {assessment}")
    except Assessment.DoesNotExist:
         print(f"DEBUG: Assessment {assessment_id} not found")
         return Response({"error": "Assessment not found"}, status=status.HTTP_404_NOT_FOUND)

    # Link user if provided and not already linked
    if user_id and not assessment.user:
        try:
            from .models import CustomUser
            user = CustomUser.objects.get(pk=user_id)
            assessment.user = user
            print(f"DEBUG: Linked user {user_id}")
        except CustomUser.DoesNotExist:
            print(f"DEBUG: User {user_id} not found")
            pass

    # --- Simple Risk Calculation Logic ---
    risk_score = 0
    risk_reasons = []

    try:
        # 1. BMI
        try:
            bmi = float(assessment.bmi) if assessment.bmi else 0
            if bmi >= 30:
                risk_score += 2
                risk_reasons.append("High BMI (Obesity)")
            elif bmi >= 25:
                risk_score += 1
                risk_reasons.append("Overweight")
        except (ValueError, TypeError):
            print(f"DEBUG: Error parsing BMI: {assessment.bmi}")
            pass

        # 2. Age
        try:
            age = int(assessment.age) if assessment.age else 0
            if age > 60:
                risk_score += 2
                risk_reasons.append("Age over 60")
            elif age > 45:
                risk_score += 1
                risk_reasons.append("Age over 45")
        except (ValueError, TypeError):
            print(f"DEBUG: Error parsing Age: {assessment.age}")
            pass

        # 3. Lifestyle
        smoking_habit = str(assessment.smoking_habit or "").lower()
        alcohol_consumption = str(assessment.alcohol_consumption or "").lower()

        if "smoking" in smoking_habit and "no" not in smoking_habit:
            risk_score += 2
            risk_reasons.append("Smoking")
        
        if "high" in alcohol_consumption:
            risk_score += 1
            risk_reasons.append("High Alcohol Consumption")

        # 4. Symptoms (Count)
        symptoms_str = str(assessment.symptoms or "")
        symptoms_list = symptoms_str.split(",") if symptoms_str else []
        if len(symptoms_list) > 3:
            risk_score += 2
            risk_reasons.append("Multiple Symptoms reported")
        elif len(symptoms_list) > 0:
            risk_score += 1

        print(f"DEBUG: Risk Score: {risk_score}, Reasons: {risk_reasons}")

        # Determine Level
        if risk_score >= 4:
            risk_level = "High"
            risk_message = "Your risk profile indicates a HIGH risk. Please consult a doctor immediately."
        elif risk_score >= 2:
            risk_level = "Medium"
            risk_message = "Your risk profile indicates a MEDIUM risk. Consider lifestyle changes and monitoring."
        else:
            risk_level = "Low"
            risk_message = "Your risk profile indicates a LOW risk. Keep up the healthy habits!"

        if risk_reasons:
            risk_message += " Factors: " + ", ".join(risk_reasons)

        # Save Result
        assessment.risk_level = risk_level
        assessment.risk_message = risk_message
        assessment.save()
        print("DEBUG: Assessment saved successfully")
        
        return Response({
            "message": "Assessment submitted successfully",
            "assessment_id": assessment.id,
            "risk_level": risk_level,
            "risk_message": risk_message
        }, status=status.HTTP_200_OK)

    except Exception as e:
        print(f"DEBUG: Exception in submit_assessment: {e}")
        import traceback
        traceback.print_exc()
        return Response({"error": f"Internal Server Error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny]) # In real app, use IsAuthenticated
def get_user_profile(request):
    user_id = request.query_params.get('user_id')
    if not user_id:
        return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        from .models import CustomUser
        user = CustomUser.objects.get(pk=user_id)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST']) # Using POST for update to avoid method issues, ideally PUT/PATCH
@permission_classes([AllowAny])
def update_user_profile(request):
    user_id = request.data.get('user_id')
    if not user_id:
        return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        from .models import CustomUser
        user = CustomUser.objects.get(pk=user_id)
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
    # Update fields
    full_name = request.data.get('full_name')
    phone_number = request.data.get('phone_number')
    
    # Optional: Email update logic (requires validation usually)
    # email = request.data.get('email')
    
    if full_name is not None:
        user.full_name = full_name
    if phone_number is not None:
        user.phone_number = phone_number
        
    user.save()
    
    return Response({"message": "Profile updated successfully"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def change_password(request):
    user_id = request.data.get('user_id')
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    if not all([user_id, old_password, new_password]):
        return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        from .models import CustomUser
        user = CustomUser.objects.get(pk=user_id)
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # Check old password
    if not user.check_password(old_password):
        return Response({"error": "Incorrect current password"}, status=status.HTTP_400_BAD_REQUEST)

    # Set new password
    user.set_password(new_password)
    user.save()

    return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
