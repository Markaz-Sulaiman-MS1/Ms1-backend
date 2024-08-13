from dj_rest_auth.serializers import LoginSerializer
from allauth.account import app_settings as allauth_settings
from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate


class CustomLoginSerializer(LoginSerializer):
    username = None  
    email = serializers.EmailField(required=True, allow_blank=False)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), username=email, password=password)  # Pass email as username
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User account is disabled.")
            else:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError('Must include "email" and "password".')

        attrs['user'] = user
        return attrs
 
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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']

class TechnicianAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Technician
        fields = '__all__'

class TechnicianSerializer(serializers.ModelSerializer):
    employee = AddEmployeeSerializer()
    job_card = JobcardSerializer()
    class Meta:
        model = Technician
        fields = ["employee","labour_charge","job_card","id"]

class SparePartsAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpareParts
        fields ='__all__'

class SparePartsSerializer(serializers.ModelSerializer):
    job_card = JobcardSerializer()
    class Meta:
        model = SpareParts
        fields =["name","category","cost","quantity","job_card","id"]


class IssuesAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issues
        fields ='__all__'

class IssuesSerializer(serializers.ModelSerializer):
    job_card = JobcardSerializer()
    class Meta:
        model = Issues
        fields =["heading","description","job_card","completed","id"]