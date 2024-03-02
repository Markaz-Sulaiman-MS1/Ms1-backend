from dj_rest_auth.serializers import LoginSerializer
from allauth.account import app_settings as allauth_settings
from rest_framework import serializers
from .models import *





class CustomLoginSerializer(LoginSerializer):
    username = None  # Remove the default username field

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[allauth_settings.USER_MODEL_USERNAME_FIELD] = serializers.CharField(
            required=False
        )

    def _validate_email(self, email, password):
        # Validate the email and password
        user = self.authenticate(email=email, password=password)
        if user:
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled.")
            return user
        else:
            raise serializers.ValidationError(
                "Unable to log in with provided credentials."
            )
        
class AddEmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = '__all__'

class UpdatesalarySerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ["net_payable_salary","other_expense"]

class ListsalarySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Employee
        fields = ["net_payable_salary","other_expense"]

class AddRemarkSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Remarks
        fields = '__all__'

class ListRemarkSerializer(serializers.ModelSerializer):
    employee = AddEmployeeSerializer()
    class Meta:
        model = Remarks
        fields = ["remarks","employee","created_at","updated_at"]

class JobcardSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCard
        fields ='__all__'


