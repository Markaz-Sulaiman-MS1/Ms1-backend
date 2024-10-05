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
    
    cabin_ac = serializers.CharField(write_only=True, required=False)
    reefer_unit = serializers.CharField(write_only=True, required=False)
    chiller_unit = serializers.CharField(write_only=True, required=False)
    ref_body = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = JobCard
        fields ='__all__'

    def update(self, instance, validated_data):
    # Pop fields that are not part of the JobCard model but are needed for BillAmount
        cabin_ac = validated_data.pop('cabin_ac', None)
        reefer_unit = validated_data.pop('reefer_unit', None)
        chiller_unit = validated_data.pop('chiller_unit', None)
        ref_body = validated_data.pop('ref_body', None) 
        print("cabin_ac",cabin_ac)

        # Pop job_type separately as it's a ManyToMany field
        job_type_data = validated_data.pop('job_type', None)
        print("job_type_data",job_type_data)

        # Update JobCard instance (except for the ManyToManyField)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update the ManyToManyField using the set() method
        if job_type_data:
            instance.job_type.set(job_type_data)

        # Handle the BillAmount updates
        cabic_ac_job_type = JobType.objects.get(name='cabin ac')
        reefer_unit_job_type = JobType.objects.get(name='reefer unit')
        chiller_unit_job_type = JobType.objects.get(name='chiller unit')
        ref_body_job_type = JobType.objects.get(name='ref body')

        if cabin_ac:
            BillAmount.objects.create(
                job_card=instance,
                job_type= cabic_ac_job_type, amount= cabin_ac
            )
        if reefer_unit:
            BillAmount.objects.create(
                job_card=instance,
                job_type= reefer_unit_job_type,amount=reefer_unit
            )
        if chiller_unit:
            BillAmount.objects.create(
                job_card=instance,
                job_type= chiller_unit_job_type, amount= chiller_unit
            )
        if ref_body:
            BillAmount.objects.create(
                job_card=instance,
                job_type= ref_body_job_type, amount= ref_body
            )

        return instance

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

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields ='__all__'


class JobTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobType
        fields ='__all__'


class OtherExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherExpense
        fields ='__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields ='__all__'