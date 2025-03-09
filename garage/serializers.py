from dj_rest_auth.serializers import LoginSerializer
from allauth.account import app_settings as allauth_settings
from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from django.db.models import Sum

# pylint: disable=E1101,W0702


class CustomLoginSerializer(LoginSerializer):
    username = None
    email = serializers.EmailField(required=True, allow_blank=False)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"), username=email, password=password
            )  # Pass email as username
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User account is disabled.")
            else:
                raise serializers.ValidationError(
                    "Unable to log in with provided credentials."
                )
        else:
            raise serializers.ValidationError('Must include "email" and "password".')

        attrs["user"] = user
        return attrs


class AddEmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = "__all__"


class UpdatesalarySerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ["net_payable_salary", "other_expense"]


class ListsalarySerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ["net_payable_salary", "other_expense"]


class AddRemarkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Remarks
        fields = "__all__"


class ListRemarkSerializer(serializers.ModelSerializer):
    employee = AddEmployeeSerializer()

    class Meta:
        model = Remarks
        fields = ["remarks", "employee", "created_at", "updated_at"]

class JobTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobType
        fields = "__all__"

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"  

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__" 
class JobcardSerializer(serializers.ModelSerializer):

    branch = BranchSerializer(read_only=True)  
    customer = CustomerSerializer(read_only=True)
    job_type = JobTypeSerializer(many=True)

    cabin_ac = serializers.CharField(write_only=True, required=False)
    reefer_unit = serializers.CharField(write_only=True, required=False)
    chiller_unit = serializers.CharField(write_only=True, required=False)
    ref_body = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = JobCard
        fields = ["vehicle_nmbr","phn_nmbr","email","address","vehicle_type","model",
                  "fuel_type","engine_hour_info","status","remarks","branch","customer"
                  ,"make_and_model","job_type","bill_type","advance_payment",
                  "average_daily_usage","next_service_hour","next_service_date","cabin_ac","reefer_unit","chiller_unit","ref_body"]

    def update(self, instance, validated_data):

        cabin_ac = validated_data.pop("cabin_ac", None)
        reefer_unit = validated_data.pop("reefer_unit", None)
        chiller_unit = validated_data.pop("chiller_unit", None)
        ref_body = validated_data.pop("ref_body", None)

        # bill_type = validated_data.pop("bill_type", None)
        # customer = validated_data.pop("customer", None)
        # customer_data = Customer.objects.get(id=customer)

        job_type_data = validated_data.pop("job_type", None)

        # if bill_type:
        #     instance.bill_type = bill_type

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if job_type_data:
            instance.job_type.set(job_type_data)
    
        # if customer_data:
        #     instance.customer.set(customer_data)
        # if bill_type == "Cash":
        cabic_ac_job_type = JobType.objects.get(name="Cabin Ac")
        reefer_unit_job_type = JobType.objects.get(name="Reefer Unit")
        chiller_unit_job_type = JobType.objects.get(name="Chiller Unit")
        ref_body_job_type = JobType.objects.get(name="Ref Body")
            
        if cabin_ac:
            BillAmount.objects.create(
                job_card=instance, job_type=cabic_ac_job_type, amount=cabin_ac
            )
        if reefer_unit:
            BillAmount.objects.create(
                job_card=instance, job_type=reefer_unit_job_type, amount=reefer_unit
            )
        if chiller_unit:
            BillAmount.objects.create(
                job_card=instance,
                job_type=chiller_unit_job_type,
                amount=chiller_unit,
            )
        if ref_body:
            BillAmount.objects.create(
                job_card=instance, job_type=ref_body_job_type, amount=ref_body
            )
        total_amount = BillAmount.objects.filter(job_card_id=instance.id).aggregate(
            Sum("amount")
        )["amount__sum"]

        Income.objects.create(
            type="Job",
            total_income=total_amount,
            job_card_id=instance.id,
            date=instance.created_at,
            name = instance.customer.name
        )
        return instance


class AddJobCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCard
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password"]


class TechnicianAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Technician
        fields = "__all__"


class TechnicianSerializer(serializers.ModelSerializer):
    employee = AddEmployeeSerializer()
    job_card = JobcardSerializer()

    class Meta:
        model = Technician
        fields = ["employee", "labour_charge", "job_card", "id"]


class SparePartsAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpareParts
        fields = "__all__"


class SparePartsSerializer(serializers.ModelSerializer):
    job_card = JobcardSerializer()

    class Meta:
        model = SpareParts
        fields = ["name", "category", "cost", "quantity", "job_card", "id"]


class IssuesAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issues
        fields = "__all__"


class IssuesSerializer(serializers.ModelSerializer):
    job_card = JobcardSerializer()

    class Meta:
        model = Issues
        fields = ["heading", "description", "job_card", "completed", "id"]


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"





class OtherExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherExpense
        fields = "__all__"


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class ContactPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactPerson
        fields = ["name", "designation", "email", "phone_nmbr"]


class AddCustomerSerializer(serializers.ModelSerializer):
    contact_persons = ContactPersonSerializer(many=True)

    class Meta:
        model = Customer
        fields = [
            "name",
            "customer_type",
            "prefered_currency",
            "permanent_address",
            "country",
            "state",
            "town",
            "contact_persons",
            "phn_nmbr",
            "whatsapp",
            "landmark",
            "zip_code",
            "email",
        ]

    def create(self, validated_data):

        contact_persons_data = validated_data.pop("contact_persons", [])
        customer = Customer.objects.create(**validated_data)
        for contact_person_data in contact_persons_data:
            ContactPerson.objects.create(customer=customer, **contact_person_data)
        return customer


class ListCustomerSerializer(serializers.ModelSerializer):
    contact_persons = ContactPersonSerializer(many=True)

    class Meta:
        model = Customer
        fields = [
            "id",
            "name",
            "customer_type",
            "prefered_currency",
            "permanent_address",
            "country",
            "state",
            "town",
            "contact_persons",
            "phn_nmbr",
            "whatsapp",
            "landmark",
            "zip_code",
            "email",
        ]


class BillAmountSerializer(serializers.ModelSerializer):

    class Meta:
        model = BillAmount
        fields = "__all__"
        


class RetrieveJobSerializer(serializers.ModelSerializer):
    branch = BranchSerializer()
    customer = CustomerSerializer()
    job_type = JobTypeSerializer(many=True)
    technician = serializers.SerializerMethodField()
    bill_amount = serializers.SerializerMethodField()

    class Meta:
        model = JobCard
        fields = [
            "id",
            "vehicle_nmbr",
            "phn_nmbr",
            "email",
            "address",
            "vehicle_type",
            "model",
            "fuel_type",
            "engine_hour_info",
            "status",
            "remarks",
            "branch",
            "customer",
            "make_and_model",
            "job_type",
            "bill_type",
            "technician",
            "advance_payment",
            "bill_amount",
        ]

    def get_technician(self, obj):
        technician = Technician.objects.filter(job_card=obj)
        return TechnicianAddSerializer(technician, many=True).data 
    
    def get_bill_amount(self, obj):
        bill_amount = BillAmount.objects.filter(job_card=obj)
        return BillAmountSerializer(bill_amount, many=True).data     



class AddExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = "__all__"


class AddIncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = "__all__"


class AddAdvance_amountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advance_amount
        fields = "__all__"
