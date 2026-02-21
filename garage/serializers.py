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



class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id","name"]



class DesignationSerializer(serializers.ModelSerializer):

    role = RoleSerializer()
    class Meta:
        model = Designation
        fields = ["id", "title", "role","account"]

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


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"  

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__" 

class BillAmountSerializer(serializers.ModelSerializer):
    job_type = JobTypeSerializer(many=True)  # or use JobTypeSerializer if you want full details

    class Meta:
        model = BillAmount
        fields = ['job_type', 'amount']


class LabourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Labour
        fields = "__all__"
        read_only_fields = ("id", "is_deleted", "created_at", "updated_at")

class JobcardSerializer(serializers.ModelSerializer):

    branch = BranchSerializer(read_only=True)  
    customer = CustomerSerializer(read_only=True)
    job_type = JobTypeSerializer(many=True)
    bill_amounts = serializers.SerializerMethodField()
    labour = LabourSerializer(many=True)

    bill_items = serializers.ListField(
        child=serializers.DictField(
            child=serializers.DecimalField(max_digits=10, decimal_places=2)
        ),
        write_only=True,
        required=False
    )


    class Meta:
        model = JobCard
        fields = ["vehicle_nmbr","phn_nmbr","email","address","vehicle_type","model",
                  "fuel_type","engine_hour_info","status","remarks","branch","customer"
                  ,"make_and_model","job_type","bill_type","advance_payment",
                  "average_daily_usage","next_service_hour","next_service_date","bill_amounts","payment_type","bill_items","job_card_doc","labour","payment_due_date","delivery_due_date","created_at",
                  "payment_due_date","delivery_due_date"]
    
    def get_bill_amounts(self, obj):
        bills = BillAmount.objects.filter(job_card=obj)
        return BillAmountSerializer(bills, many=True).data 

    def update(self, instance, validated_data):

        bill_items = validated_data.pop("bill_items", None)
        job_type_data = validated_data.pop("job_type", None)
        labour_data = validated_data.pop("labour", None)

        status = validated_data.pop("status", None)
        

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        
        if status is not None:
            instance.status = status

        instance.save()
     

        if job_type_data:
            instance.job_type.set(job_type_data)
        
        if labour_data:
            instance.labour.set(labour_data)
        

        if bill_items:
                for item in bill_items:
                    for job_type_id, amount in item.items():
                        try:
                            job_type_obj = JobType.objects.get(id=job_type_id)
                            if status == "Credit":
                                BillAmount.objects.create(
                                    job_card=instance,
                                    job_type=job_type_obj,
                                    amount=amount
                                )
                            if status == "Closed":
                                bill_amount = BillAmount.objects.filter(job_card=instance,job_type=job_type_obj).first()
                                if bill_amount:
                                    bill_amount.amount = amount
                                    bill_amount.save()
                                else:
                                    BillAmount.objects.create(
                                    job_card=instance,
                                    job_type=job_type_obj,
                                    amount=amount
                                )

                        except JobType.DoesNotExist:
                            raise serializers.ValidationError(
                                {"bill_items": f"JobType with id {job_type_id} does not exist"}
                            )



        total_amount = BillAmount.objects.filter(job_card_id=instance.id).aggregate(
            Sum("amount")
        )["amount__sum"] or 0
        
        # Calculate final amount (Total - Advance from Advance_amount table)
        advance_payment = Advance_amount.objects.filter(job_card=instance).aggregate(
            Sum("amount")
        )["amount__sum"] or 0
        
        final_amount = total_amount - advance_payment
        
        if status == "Closed":

            Income.objects.create(
                type="Job",
                total_income=final_amount,
                job_card_id=instance.id,
                date=instance.created_at,
                name = instance.customer.name,
                branch = instance.branch,
                payment_type = instance.payment_type
            )

            if instance.payment_type == JobCard.CASH:
                balance, created = Balance.objects.get_or_create(
                branch_id=instance.branch.id,
                defaults={
                    'cash_balance': final_amount,
                }
                )
            
                if not created:
                    balance.cash_balance += final_amount
                    balance.save()
                if instance.bill_type == JobCard.CASH:
                    RecentTransaction.objects.create(
                            transaction_type=RecentTransaction.INCOME,
                            description = "Job card income transferred as cash",
                            payment_type = instance.payment_type,
                            amount = final_amount,
                            balance_cash = balance.cash_balance,
                            balance_bank = balance.bank_balance,
                            branch_id=instance.branch.id
                    )
                else:
                    RecentTransaction.objects.create(
                            transaction_type=RecentTransaction.INCOME,
                            description = "Job card income closed as cashed credit",
                            payment_type = instance.payment_type,
                            amount = final_amount,
                            balance_cash = balance.cash_balance,
                            balance_bank = balance.bank_balance,
                            branch_id=instance.branch.id
                    )
                

            else:
                balance, created = Balance.objects.get_or_create(
                branch_id=instance.branch.id,
                defaults={
                    'bank_balance': final_amount,
                }
                )
            
                if not created:
                    balance.bank_balance += final_amount
                    balance.save()

                if instance.bill_type == JobCard.CASH:
                    RecentTransaction.objects.create(
                            transaction_type=RecentTransaction.INCOME,
                            description = "Job card income transferred to bank",
                            payment_type = instance.payment_type,
                            amount = final_amount,
                            balance_cash = balance.cash_balance,
                            balance_bank = balance.bank_balance,
                            branch_id=instance.branch.id
                    )
                else:
                    RecentTransaction.objects.create(
                            transaction_type=RecentTransaction.INCOME,
                            description = "Job card income closed as banked credit",
                            payment_type = instance.payment_type,
                            amount = final_amount,
                            balance_cash = balance.cash_balance,
                            balance_bank = balance.bank_balance,
                            branch_id=instance.branch.id
                    )


        return instance


class AddJobCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCard
        fields = "__all__"


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['id', 'name']


class AccountSerializer(serializers.ModelSerializer):
    branches = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ['id', 'company', 'address', 'branches']

    def get_branches(self, obj):
        branches = Branch.objects.filter(account=obj)
        return BranchSerializer(branches, many=True).data
    

class UserSerializer(serializers.ModelSerializer):
    account = AccountSerializer()
    branch = BranchSerializer()
    role  = RoleSerializer()
    designation = DesignationSerializer()
    class Meta:
        model = User
        fields = ["user_img","role","designation","branch","passport_nmbr","visa_type",
                  "visa_expiry","address","country","state","phone_personal","email","account","branch","team","first_name","last_name"]


class TechnicianAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Technician
        fields = "__all__"


class TechnicianSerializer(serializers.ModelSerializer):
    employee = AddEmployeeSerializer()
    job_card = JobcardSerializer()
    user = UserSerializer()

    class Meta:
        model = Technician
        fields = ["employee", "labour_charge", "job_card", "id","user"]


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



class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecentTransaction
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
            "account"
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
            "account"
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
    labour = LabourSerializer(many=True)

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
            "payment_type",
            "created_at",
            "labour",
            "job_card_doc",
            "payment_due_date",
            "delivery_due_date"

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

    def create(self, validated_data):
       
        expense = super().create(validated_data)

        branch_id = expense.branch.id
        if expense.type == "Salary":
            total_amount = float(expense.salary) + float(expense.other_expense)  
        else:
            total_amount = float(expense.total_cost) + float(expense.other_expense)
             
        payment_type = expense.payment_type

        if payment_type == JobCard.CASH:
                                    
            balance, created = Balance.objects.get_or_create(
            branch_id=branch_id,
            defaults={
                'cash_balance': total_amount,
            }
            )
            if not created:
                
                balance.cash_balance -= total_amount
                balance.save()

            RecentTransaction.objects.create(
                    transaction_type=RecentTransaction.EXPENSE,
                    description = f"{expense.type} expense transferred as cash",
                    payment_type = expense.payment_type,
                    amount = total_amount,
                    balance_cash = balance.cash_balance,
                    balance_bank = balance.bank_balance,
                    branch_id=expense.branch.id
            )

        elif payment_type == JobCard.BANK:
            balance, created = Balance.objects.get_or_create(
            branch_id=branch_id,
            defaults={
                'bank_balance': total_amount,
            }
            )
                      
            if not created:
                balance.bank_balance -= total_amount
                balance.save()

            RecentTransaction.objects.create(
                    transaction_type=RecentTransaction.EXPENSE,
                    description = f"{expense.type} expense transferred to bank",
                    payment_type = expense.payment_type,
                    amount = total_amount,
                    balance_cash = balance.cash_balance,
                    balance_bank = balance.bank_balance,
                    branch_id=expense.branch.id
                    
            )

        return expense


class AddIncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = "__all__"

    def create(self, validated_data):
        # Create the Income object first
        income = super().create(validated_data)

        branch_id = income.branch.id
        total_amount = income.total_income  # or the field name for amount
        payment_type = income.payment_type

        if payment_type == JobCard.CASH:
            # Create or update cash balance
            balance, created = Balance.objects.get_or_create(
            branch_id=branch_id,
            defaults={
                'cash_balance': total_amount,
            }
            )
        
            if not created:
                balance.cash_balance += total_amount
                balance.save()

            RecentTransaction.objects.create(
                    transaction_type=RecentTransaction.INCOME,
                    description = "Other income transferred as cash",
                    payment_type = income.payment_type,
                    amount = income.total_income,
                    balance_cash = balance.cash_balance,
                    balance_bank = balance.bank_balance,
                    branch_id=income.branch.id
            )
                

        elif payment_type == JobCard.BANK:
            # Create or update bank balance
            balance, created = Balance.objects.get_or_create(
            branch_id=branch_id,
            defaults={
                'bank_balance': total_amount,
            }
            )
        
            if not created:
                balance.bank_balance += total_amount
                balance.save()
             
            RecentTransaction.objects.create(
                    transaction_type=RecentTransaction.INCOME,
                    description = "Other income transferred to bank",
                    payment_type = income.payment_type,
                    amount = income.total_income,
                    balance_cash = balance.cash_balance,
                    balance_bank = balance.bank_balance,
                    branch_id=income.branch.id

            )
                

        return income


class AddAdvance_amountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advance_amount
        fields = "__all__"


class UsersSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    account_info =  AccountSerializer(source="account",read_only=True)
    branch_info =  BranchSerializer(source="branch",read_only=True)
    role  = RoleSerializer()
    designation = DesignationSerializer()

    class Meta:
        model = User
        fields = [
            "id", "email", "username", "password", "first_name", "last_name",
            "user_img", "role", "passport_nmbr", "visa_type", "visa_expiry",
            "address", "country", "state", "phone_personal", "account",
            "branch", "team", "designation", "date_of_joining", "date_of_birth",
            "town", "zip_code", "net_payable_salary", "other_expense","account_info","branch_info"
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password) 
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
    



class UsersCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "id", "email", "username", "password", "first_name", "last_name",
            "user_img", "role", "passport_nmbr", "visa_type", "visa_expiry",
            "address", "country", "state", "phone_personal", "account",
            "branch", "team", "designation", "date_of_joining", "date_of_birth",
            "town", "zip_code", "net_payable_salary", "other_expense"
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password) 
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance




class TimeZoneSerilaizer(serializers.ModelSerializer):

    class Meta:
        model = TimeZone
        fields = "__all__"
    
class BrandSerializer(serializers.ModelSerializer):
    account =  AccountSerializer(read_only=True)
    class Meta:
        model=Brand
        fields=["name","description","account","id"]



class CategorySerializer(serializers.ModelSerializer):
    account =  AccountSerializer(read_only=True)
    class Meta:
        model=Category
        fields=["name","description","account","id"]



class VendorSerializer(serializers.ModelSerializer):
    account =  AccountSerializer(read_only=True)
    class Meta:
        model=Vendor
        fields=["name","description","account","address","id"]



class ProductSerializer(serializers.ModelSerializer):
    product_img = serializers.ImageField(required=False)

    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all())
    base_quantity = serializers.PrimaryKeyRelatedField(
        queryset=Units.objects.all(),
        required=False,
        allow_null=True
    )
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())


    class Meta:
        model = Product
        fields = [
            "id", "product_img", "product_code", "product_name", "condition_type",
            "brand", "cost_price", "base_quantity", "base_quantity_value", "category", "selling_price",
            "stock_reorder_level", "description","account"
        ]

class ProductListSerializer(serializers.ModelSerializer):
    product_img = serializers.ImageField(required=False)
    account =  AccountSerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    category = CategorySerializer(read_only=True)


    class Meta:
        model = Product
        fields = [
            "id", "product_img", "product_code", "product_name", "condition_type",
            "brand", "cost_price", "base_quantity", "base_quantity_value", "category", "selling_price",
            "stock_reorder_level", "description","account"
        ]


class SellPackSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellPack
        fields = "__all__"


class SellPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellPart    
        fields = "__all__"


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = "__all__"
        read_only_fields = ["po_nmbr"]



# class PurchaseListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Purchase
#         fields = "__all__"
        


class ProductItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductItem
        fields = "__all__"



class ProductItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.product_name', read_only=True)

    class Meta:
        model = ProductItem
        fields = ["id", "product", "product_name", "quantity", "amount", "purchase", "created_at", "updated_at"]


class PurchaseDetailWithBatchesSerializer(serializers.ModelSerializer):
    """
    Purchase serializer with nested batch details and batch sell packs.
    Used by ListPurchaseItems API to return comprehensive purchase information.
    """
    vendor_name = serializers.CharField(source='vendor.name', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    batches = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()
    items_no = serializers.SerializerMethodField()
    total_bill = serializers.SerializerMethodField()

    class Meta:
        model = Purchase
        fields = [
            "id", "po_nmbr", "vendor", "vendor_name", "branch", "branch_name",
            "exp_date_delivery", "description", "purchase_type", "discount",
            "tax", "total_amount", "created_at", "updated_at", "items_no",
            "total_bill", "items", "batches"
        ]

    def get_items_no(self, obj):
        return ProductItem.objects.filter(purchase=obj, is_deleted=False).count()

    def get_total_bill(self, obj):
        total = ProductItem.objects.filter(purchase=obj, is_deleted=False).aggregate(
            total_amount=Sum('amount')
        )['total_amount']
        return total or 0

    def get_items(self, obj):
        """Get purchase items for this purchase."""
        items = ProductItem.objects.filter(purchase=obj, is_deleted=False)
        return ProductItemSerializer(items, many=True).data

    def get_batches(self, obj):
        """
        Get batches for this purchase with nested batch sell packs.
        Uses BatchDetailSerializer which includes batch_sell_packs.
        """
        from .serializers import BatchDetailSerializer
        batches = Batch.objects.filter(purchase=obj, is_deleted=False)
        return BatchDetailSerializer(batches, many=True).data


class PurchaseListSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source='vendor.name', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    items_no = serializers.SerializerMethodField()
    total_bill = serializers.SerializerMethodField()

    class Meta:
        model = Purchase
        fields = [
            "id", "po_nmbr", "vendor", "vendor_name", "branch", "branch_name",
            "exp_date_delivery", "description", "purchase_type", "created_at","items_no","total_bill"
        ]
        
    def get_items_no(self, obj):
            return ProductItem.objects.filter(purchase=obj,is_deleted=False).count()

    def get_total_bill(self, obj):
        total = ProductItem.objects.filter(purchase=obj, is_deleted=False).aggregate(
            total_amount=Sum('amount')
        )['total_amount']
        return total or 0 

class EditPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ["vendor", "exp_date_delivery", "branch", "description", "purchase_type"]

class BatchSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = Batch
        fields = [
            "id", "batch_code", "product_code", "manufacture_date",
            "expiry_date", "cost_price", "product", "product_name", "created_at"
        ]


class BatchSellPackCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating BatchSellPack without batch reference (will be set in parent)"""
    class Meta:
        model = BatchSellPack
        fields = ["sell_pack", "sell_price", "cost_price"]


class CreateBatchSerializer(serializers.ModelSerializer):
    """Serializer for creating Batch with nested BatchSellPack records"""
    batch_sell_packs = BatchSellPackCreateSerializer(many=True, required=False, write_only=True)

    class Meta:
        model = Batch
        fields = [
            "id", "batch_code", "product_code", "manufacture_date",
            "expiry_date", "cost_price", "sell_price", "product", "purchase",
            "batch_sell_packs"
        ]
        read_only_fields = ["id", "batch_code"]

    def create(self, validated_data):
        # Extract batch_sell_packs data
        batch_sell_packs_data = validated_data.pop('batch_sell_packs', [])
        
        # Create the batch
        batch = Batch.objects.create(**validated_data)
        
        # Create associated BatchSellPack records
        for sell_pack_data in batch_sell_packs_data:
            BatchSellPack.objects.create(batch=batch, **sell_pack_data)
        
        return batch

    def update(self, instance, validated_data):
        # Extract batch_sell_packs data
        batch_sell_packs_data = validated_data.pop('batch_sell_packs', None)
        
        # Update batch fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # If batch_sell_packs data provided, update them
        if batch_sell_packs_data is not None:
            # Delete existing batch sell packs and create new ones
            BatchSellPack.objects.filter(batch=instance).delete()
            for sell_pack_data in batch_sell_packs_data:
                BatchSellPack.objects.create(batch=instance, **sell_pack_data)
        
        return instance


class StockAdjustmentItemCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating StockAdjustmentItem with batch_sell_pack reference"""
    whole_sell_pack = serializers.UUIDField(write_only=True, required=False)
    unbatched_whole_pack = serializers.UUIDField(write_only=True, required=False)
    unbatched_sell_pack = serializers.UUIDField(write_only=True, required=False)

    class Meta:
        model = StockAdjustmentItem
        fields = ["product", "batch_sell_pack", "whole_sell_pack", "unbatched_whole_pack", "unbatched_sell_pack", "current_quantity", "adjust_quantity", "rate", "rate_adjustment", "amount"]


class CreateStockAdjustmentSerializer(serializers.ModelSerializer):
    """
    Serializer for creating StockAdjustment with nested StockAdjustmentItems.
    Handles:
    1. Creating StockAdjustment and nested items
    2. Updating stock quantities based on batch_sell_pack, whole_sell_pack, unbatched_whole_pack, unbatched_sell_pack and adjust_quantity
       - batch_sell_pack: actual_stock_adjustment = adjust_quantity * sell_pack.quantity / product.base_quantity_value
       - whole_sell_pack: actual_stock_adjustment = adjust_quantity
       - unbatched_whole_pack: actual_stock_adjustment = adjust_quantity (Product directly)
       - unbatched_sell_pack: actual_stock_adjustment = adjust_quantity * sell_pack.quantity / product.base_quantity_value
    3. Creating Income/Expense records based on adjustment_impact
    4. Updating Balance and creating RecentTransaction records
    """
    items = StockAdjustmentItemCreateSerializer(many=True, required=False, write_only=True)

    class Meta:
        model = StockAdjustment
        fields = [
            "id", "adjustment_number", "adjusted_by", "reason_for_adjustment",
            "payment_type", "branch", "adjustment_impact", "items"
        ]
        read_only_fields = ["id", "adjustment_number"]

    def create(self, validated_data):
        # Extract items data
        items_data = validated_data.pop('items', [])
        
        # Create the StockAdjustment
        stock_adjustment = StockAdjustment.objects.create(**validated_data)
        
        total_amount = 0
        
        # Create StockAdjustmentItems and update stock
        for item_data in items_data:
            # Extract special keys
            whole_sell_pack_id = item_data.pop('whole_sell_pack', None)
            unbatched_whole_pack_id = item_data.pop('unbatched_whole_pack', None)
            unbatched_sell_pack_id = item_data.pop('unbatched_sell_pack', None)
            
            # Resolve Product if not explicitly provided but special keys are present
            resolved_product = item_data.get('product')
            
            # Resolve objects
            whole_sell_pack = None
            if whole_sell_pack_id:
                try:
                    whole_sell_pack = Batch.objects.get(id=whole_sell_pack_id)
                    if not resolved_product:
                        resolved_product = whole_sell_pack.product
                except Batch.DoesNotExist:
                    pass

            unbatched_whole_pack_product = None
            if unbatched_whole_pack_id:
                try:
                    unbatched_whole_pack_product = Product.objects.get(id=unbatched_whole_pack_id)
                    if not resolved_product:
                        resolved_product = unbatched_whole_pack_product
                except Product.DoesNotExist:
                    pass

            unbatched_sell_pack_obj = None
            if unbatched_sell_pack_id:
                try:
                    unbatched_sell_pack_obj = SellPack.objects.get(id=unbatched_sell_pack_id)
                    if not resolved_product:
                        resolved_product = unbatched_sell_pack_obj.product
                except SellPack.DoesNotExist:
                    pass
            
            # Before creating item, ensure product is set if resolved
            if resolved_product and not item_data.get('product'):
                item_data['product'] = resolved_product

            # Create the adjustment item
            adjustment_item = StockAdjustmentItem.objects.create(
                stock_adjustment=stock_adjustment,
                **item_data
            )
            
            # Calculate total amount for financial transactions
            if adjustment_item.amount:
                total_amount += float(adjustment_item.amount)
            
            # Get adjustment params
            batch_sell_pack = item_data.get('batch_sell_pack')
            adjust_quantity = item_data.get('adjust_quantity', 0) or 0
            
            actual_stock_adjustment = 0
            product = resolved_product # Use resolved product
            
            if whole_sell_pack and adjust_quantity != 0:
                # Logic for Batched Whole Sell Pack
                # User request: "just have to reduce the adjust quantity from that stock connected to that whole_sell_pack_id"
                actual_stock_adjustment = adjust_quantity
                
            elif batch_sell_pack and adjust_quantity != 0:
                # Logic for Batched Sell Pack
                sell_pack = batch_sell_pack.sell_pack
                sell_pack_quantity = sell_pack.quantity if sell_pack and sell_pack.quantity else 1
                
                # Product already resolved likely via batch_sell_pack -> sell_pack -> product relation in serializer validation?
                # Or handled by item_data['product'] if provided.
                # If not provided, we rely on sell_pack.product
                if not product:
                    product = sell_pack.product
                base_quantity_value = product.base_quantity_value if product and product.base_quantity_value else 1
                
                actual_stock_adjustment = (adjust_quantity * sell_pack_quantity) / base_quantity_value
            
            elif unbatched_whole_pack_product and adjust_quantity != 0:
                # Logic for Unbatched Whole Pack
                # User request: "take whole pack unbatched... updated on that particular stock of that product which is not having any batches"
                # This implies direct adjustment (1 product unit = 1 stock unit)
                product = unbatched_whole_pack_product
                actual_stock_adjustment = adjust_quantity
                
            elif unbatched_sell_pack_obj and adjust_quantity != 0:
                # Logic for Unbatched Sell Pack
                product = unbatched_sell_pack_obj.product
                base_quantity_value = product.base_quantity_value if product and product.base_quantity_value else 1
                
                actual_stock_adjustment = (adjust_quantity * unbatched_sell_pack_obj.quantity) / base_quantity_value

            elif item_data.get('product') and adjust_quantity != 0:
                # Fallback Logic (General Product Adjustment via direct product ID)
                product = item_data.get('product')
                actual_stock_adjustment = adjust_quantity

            # Update Stock
            if product and actual_stock_adjustment != 0:
                stock = None
                purchase = None
                
                # Determine purchase from batch info
                if whole_sell_pack:
                    purchase = whole_sell_pack.purchase
                elif batch_sell_pack and batch_sell_pack.batch:
                    purchase = batch_sell_pack.batch.purchase
                
                # Try to find stock specific to this purchase
                if purchase:
                    stock = Stock.objects.filter(product=product, purchase=purchase).first()
                
                # Fallback: Use general stock if no specific stock found
                if not stock:
                    stock = Stock.objects.filter(product=product).order_by('created_at').first()

                if stock:
                    stock.quantity = (stock.quantity or 0) + actual_stock_adjustment
                    stock.save()
                else:
                    Stock.objects.create(
                        product=product,
                        quantity=actual_stock_adjustment,
                        branch=stock_adjustment.branch, 
                        purchase=purchase
                    )
        
        
        # Handle financial transactions based on adjustment_impact
        branch = stock_adjustment.branch
        payment_type = stock_adjustment.payment_type
        adjustment_impact = stock_adjustment.adjustment_impact
        
        if branch and payment_type and adjustment_impact and adjustment_impact != StockAdjustment.IGNORE and total_amount > 0:
            branch_id = branch.id
            
            if adjustment_impact == StockAdjustment.INCOME:
                # Create Income record
                Income.objects.create(
                    type="Other",
                    name=f"Stock Adjustment - {stock_adjustment.adjustment_number}",
                    description=stock_adjustment.reason_for_adjustment,
                    total_income=total_amount,
                    date=stock_adjustment.created_at,
                    branch=branch,
                    payment_type=payment_type
                )
                
                # Update Balance - increase
                if payment_type == "Cash":
                    balance, created = Balance.objects.get_or_create(
                        branch_id=branch_id,
                        defaults={'cash_balance': total_amount}
                    )
                    if not created:
                        balance.cash_balance = (balance.cash_balance or 0) + total_amount
                        balance.save()
                    
                    RecentTransaction.objects.create(
                        transaction_type=RecentTransaction.INCOME,
                        description=f"Stock adjustment income - {stock_adjustment.adjustment_number}",
                        payment_type=payment_type,
                        amount=total_amount,
                        balance_cash=balance.cash_balance,
                        balance_bank=balance.bank_balance,
                        branch=branch
                    )
                else:  # Bank
                    balance, created = Balance.objects.get_or_create(
                        branch_id=branch_id,
                        defaults={'bank_balance': total_amount}
                    )
                    if not created:
                        balance.bank_balance = (balance.bank_balance or 0) + total_amount
                        balance.save()
                    
                    RecentTransaction.objects.create(
                        transaction_type=RecentTransaction.INCOME,
                        description=f"Stock adjustment income - {stock_adjustment.adjustment_number}",
                        payment_type=payment_type,
                        amount=total_amount,
                        balance_cash=balance.cash_balance,
                        balance_bank=balance.bank_balance,
                        branch=branch
                    )
            
            elif adjustment_impact == StockAdjustment.EXPENSE:
                # Create Expense record
                Expense.objects.create(
                    type="Other",
                    name=f"Stock Adjustment - {stock_adjustment.adjustment_number}",
                    description=stock_adjustment.reason_for_adjustment,
                    total_cost=total_amount,
                    date=stock_adjustment.created_at,
                    branch=branch,
                    payment_type=payment_type
                )
                
                # Update Balance - decrease
                if payment_type == "Cash":
                    balance, created = Balance.objects.get_or_create(
                        branch_id=branch_id,
                        defaults={'cash_balance': 0}
                    )
                    if not created:
                        balance.cash_balance = (balance.cash_balance or 0) - total_amount
                        balance.save()
                    
                    RecentTransaction.objects.create(
                        transaction_type=RecentTransaction.EXPENSE,
                        description=f"Stock adjustment expense - {stock_adjustment.adjustment_number}",
                        payment_type=payment_type,
                        amount=total_amount,
                        balance_cash=balance.cash_balance,
                        balance_bank=balance.bank_balance,
                        branch=branch
                    )
                else:  # Bank
                    balance, created = Balance.objects.get_or_create(
                        branch_id=branch_id,
                        defaults={'bank_balance': 0}
                    )
                    if not created:
                        balance.bank_balance = (balance.bank_balance or 0) - total_amount
                        balance.save()
                    
                    RecentTransaction.objects.create(
                        transaction_type=RecentTransaction.EXPENSE,
                        description=f"Stock adjustment expense - {stock_adjustment.adjustment_number}",
                        payment_type=payment_type,
                        amount=total_amount,
                        balance_cash=balance.cash_balance,
                        balance_bank=balance.bank_balance,
                        branch=branch
                    )
        
        return stock_adjustment


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Units
        fields = ["id", "name", "created_at"]


class BatchSellPackSerializer(serializers.ModelSerializer):
    sell_pack_name = serializers.CharField(source='sell_pack.name', read_only=True)
    sell_pack_code = serializers.CharField(source='sell_pack.product_code', read_only=True)
    no_of_pieces = serializers.IntegerField(source='sell_pack.no_of_pieces', read_only=True)
    stock_quantity = serializers.SerializerMethodField()
    
    class Meta:
        model = BatchSellPack
        fields = [
            "id", "batch", "sell_pack", "sell_pack_name", "sell_pack_code",
            "sell_price", "cost_price", "no_of_pieces", "stock_quantity", "created_at"
        ]

    def get_stock_quantity(self, obj):
        """
        Calculate stock quantity for this sell pack by dividing batch stock by sell pack quantity.
        Example: if batch stock is 100L and sell pack is 2L, stock_quantity = 100/2 = 50 packs.
        batch_stock is passed through context from parent serializer.
        """
        batch_stock = self.context.get('batch_stock') 
        sell_pack_quantity = obj.sell_pack.quantity if obj.sell_pack and obj.sell_pack.quantity else 1
        
        if sell_pack_quantity > 0:
            return int(batch_stock * obj.sell_pack.product.base_quantity_value // sell_pack_quantity)
        return 0


class BatchDetailSerializer(serializers.ModelSerializer):
    """Batch serializer with nested BatchSellPack details"""
    product_name = serializers.CharField(source='product.product_name', read_only=True)
    batch_sell_packs = serializers.SerializerMethodField()
    stock_quantity = serializers.SerializerMethodField()

    class Meta:
        model = Batch
        fields = [
            "id", "batch_code", "product_code", "manufacture_date",
            "expiry_date", "cost_price", "sell_price", "product", "product_name", 
            "stock_quantity", "created_at", "batch_sell_packs"
        ]

    def get_stock_quantity(self, obj):
        """
        Get stock quantity from Stock model based on the purchase linked to this batch.
        """
        if obj.purchase:
            stock = Stock.objects.filter(purchase=obj.purchase, product=obj.product).first()
            if stock:
                return stock.quantity
        return 0

    def get_batch_sell_packs(self, obj):
        """
        Get batch sell packs and pass batch stock quantity to child serializer context.
        """
        batch_stock = self.get_stock_quantity(obj)
        batch_sell_packs = BatchSellPack.objects.filter(batch=obj)
        return BatchSellPackSerializer(
            batch_sell_packs, 
            many=True, 
            context={'batch_stock': batch_stock}
        ).data


class ProductBatchDetailSerializer(serializers.ModelSerializer):
    """Product serializer with nested Batch and BatchSellPack details"""
    # brand = BrandSerializer(read_only=True)
    # category = CategorySerializer(read_only=True)
    batches = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id", "product_img", "product_code", "product_name", "condition_type",
            "brand", "cost_price", "base_quantity", "base_quantity_value", "category", "selling_price",
            "stock_reorder_level", "description", "batches"
        ]

    def get_batches(self, obj):
        batches = Batch.objects.filter(product=obj, is_deleted=False)
        return BatchDetailSerializer(batches, many=True).data


class PurchaseLogSerializer(serializers.ModelSerializer):
    """Serializer for PurchaseLog with purchase details"""
    purchase_number = serializers.CharField(source='purchase.po_nmbr', read_only=True)
    
    class Meta:
        model = PurchaseLog
        fields = [
            "id", "purchase", "purchase_number", "created_by", 
            "status", "created_at", "updated_at"
        ]


class SellPackSerializer(serializers.ModelSerializer):
    """Serializer for SellPack CRUD operations"""
    product_name = serializers.CharField(source='product.product_name', read_only=True)
    
    class Meta:
        model = SellPack
        fields = [
            "id", "name", "product_code", "quantity", "no_of_pieces",
            "cost_price", "selling_price", "product", "product_name",
            "created_at", "updated_at"
        ]


class SellPartSerializer(serializers.ModelSerializer):
    """Serializer for SellPart CRUD operations"""
    product_name = serializers.CharField(source='product.product_name', read_only=True)
    
    class Meta:
        model = SellPart
        fields = [
            "id", "name", "product_code", "no_of_pieces",
            "cost_price", "selling_price", "product", "product_name",
            "created_at", "updated_at"
        ]
class ProductStockSerializer(serializers.ModelSerializer):
    """Serializer for Stock with batch and batch sell pack details"""
    batch_details = serializers.SerializerMethodField()
    
    class Meta:
        model = Stock
        fields = ["id", "quantity", "product", "purchase", "branch", "created_at", "batch_details"]
    
    def get_batch_details(self, obj):
        """Get batch details with nested batch sell packs for this stock's purchase"""
        if obj.purchase:
            batches = Batch.objects.filter(
                purchase=obj.purchase, 
                product=obj.product, 
                is_deleted=False
            )
            return BatchDetailSerializer(
                batches, 
                many=True, 
                context={'stock_quantity': obj.quantity}
            ).data
        return []


class ProductWithStockSerializer(serializers.ModelSerializer):
    """
    Product serializer with stock details and batch sell pack information.
    Used for listing products with stock for a specific branch.
    Includes:
    - sell_packs: SellPack details for products (shown when no batches exist)
    - unbatched_quantity: total stock - sum of batch quantities
    """
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    base_quantity_name = serializers.CharField(source='base_quantity.name', read_only=True)
    stocks = serializers.SerializerMethodField()
    total_stock_quantity = serializers.SerializerMethodField()
    sell_packs = serializers.SerializerMethodField()
    unbatched_quantity = serializers.SerializerMethodField()
    has_batches = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            "id", "product_img", "product_code", "product_name", "condition_type",
            "brand", "brand_name", "cost_price", "base_quantity", "base_quantity_name",
            "base_quantity_value", "category", "category_name", "selling_price",
            "stock_reorder_level", "description", "total_stock_quantity", 
            "unbatched_quantity", "has_batches", "sell_packs", "stocks"
        ]
    
    def get_stocks(self, obj):
        """Get stocks for this product filtered by branch from context"""
        branch_id = self.context.get('branch_id')
        if branch_id:
            stocks = Stock.objects.filter(product=obj, branch_id=branch_id)
        else:
            stocks = Stock.objects.filter(product=obj)
        return ProductStockSerializer(stocks, many=True).data
    
    def get_total_stock_quantity(self, obj):
        """Get total stock quantity for this product in the branch"""
        branch_id = self.context.get('branch_id')
        if branch_id:
            total = Stock.objects.filter(product=obj, branch_id=branch_id).aggregate(
                total=Sum('quantity')
            )['total']
        else:
            total = Stock.objects.filter(product=obj).aggregate(
                total=Sum('quantity')
            )['total']
        return total or 0
    
    def get_has_batches(self, obj):
        """Check if product has any batches"""
        return Batch.objects.filter(product=obj, is_deleted=False).exists()
    
    def get_sell_packs(self, obj):
        """Get SellPack details for this product (useful when no batches exist)"""
        sell_packs = SellPack.objects.filter(product=obj)
        return SellPackSerializer(sell_packs, many=True).data
    
    def get_unbatched_quantity(self, obj):
        """
        Calculate unbatched quantity = total stock - sum of batched stock quantities.
        This represents stock that is not associated with any batch.
        """
        branch_id = self.context.get('branch_id')
        
        # Get total stock for this product in the branch
        if branch_id:
            total_stock = Stock.objects.filter(product=obj, branch_id=branch_id).aggregate(
                total=Sum('quantity')
            )['total'] or 0
            
            # Get sum of stock that has purchases with batches
            batched_stock = Stock.objects.filter(
                product=obj, 
                branch_id=branch_id,
                purchase__isnull=False
            ).filter(
                purchase__in=Batch.objects.filter(product=obj, is_deleted=False).values('purchase')
            ).aggregate(total=Sum('quantity'))['total'] or 0
        else:
            total_stock = Stock.objects.filter(product=obj).aggregate(
                total=Sum('quantity')
            )['total'] or 0
            
            batched_stock = Stock.objects.filter(
                product=obj,
                purchase__isnull=False
            ).filter(
                purchase__in=Batch.objects.filter(product=obj, is_deleted=False).values('purchase')
            ).aggregate(total=Sum('quantity'))['total'] or 0
        
        return total_stock - batched_stock



class InventoryStockItemSerializer(serializers.ModelSerializer):
    """Read serializer for listing InventoryStockItem records with full product details"""
    product = ProductWithStockSerializer(read_only=True)

    class Meta:
        model = InventoryStockItem
        fields = "__all__"


class InventoryStockItemCreateSerializer(serializers.ModelSerializer):
    whole_sell_pack = serializers.UUIDField(required=False, write_only=True)
    unbatched_whole_pack = serializers.UUIDField(required=False, write_only=True)
    unbatched_sell_pack = serializers.UUIDField(required=False, write_only=True)

    class Meta:
        model = InventoryStockItem
        fields = [
            "id", "product", "batch_sell_pack", "whole_sell_pack", 
            "unbatched_whole_pack", "unbatched_sell_pack",
            "item_type", "current_quantity", "adjust_quantity", "rate", 
            "rate_adjustment", "amount"
        ]

class CreateInventoryStockSerializer(serializers.Serializer):
    job_card = serializers.PrimaryKeyRelatedField(queryset=JobCard.objects.all())
    items = InventoryStockItemCreateSerializer(many=True)

    def create(self, validated_data):
        job_card = validated_data.get('job_card')
        items_data = validated_data.get('items', [])
        
        created_items = []
        
        for item_data in items_data:
            # Extract special keys
            whole_sell_pack_id = item_data.pop('whole_sell_pack', None)
            unbatched_whole_pack_id = item_data.pop('unbatched_whole_pack', None)
            unbatched_sell_pack_id = item_data.pop('unbatched_sell_pack', None)
            item_data.pop('item_type', None)  # Auto-set below; ignore any frontend value
            
            # Resolve Product if not explicitly provided but special keys are present
            resolved_product = item_data.get('product')
            
            # Resolve objects (Same logic as StockAdjustment)
            whole_sell_pack = None
            if whole_sell_pack_id:
                try:
                    whole_sell_pack = Batch.objects.get(id=whole_sell_pack_id)
                    if not resolved_product:
                        resolved_product = whole_sell_pack.product
                except Batch.DoesNotExist:
                    pass

            unbatched_whole_pack_product = None
            if unbatched_whole_pack_id:
                try:
                    unbatched_whole_pack_product = Product.objects.get(id=unbatched_whole_pack_id)
                    if not resolved_product:
                        resolved_product = unbatched_whole_pack_product
                except Product.DoesNotExist:
                    pass

            unbatched_sell_pack_obj = None
            if unbatched_sell_pack_id:
                try:
                    unbatched_sell_pack_obj = SellPack.objects.get(id=unbatched_sell_pack_id)
                    if not resolved_product:
                        resolved_product = unbatched_sell_pack_obj.product
                except SellPack.DoesNotExist:
                    pass
            
            # Ensure product is set
            if resolved_product and not item_data.get('product'):
                item_data['product'] = resolved_product

            # Auto-detect item_type based on which key was provided
            if whole_sell_pack_id:
                detected_item_type = InventoryStockItem.WHOLE_SELL_PACK
            elif unbatched_whole_pack_id:
                detected_item_type = InventoryStockItem.UNBATCHED_WHOLE_PACK
            elif unbatched_sell_pack_id:
                detected_item_type = InventoryStockItem.UNBATCHED_SELL_PACK
            elif item_data.get('batch_sell_pack'):
                detected_item_type = InventoryStockItem.BATCH_SELL_PACK
            else:
                detected_item_type = None

            # Create InventoryStockItem
            inventory_item = InventoryStockItem.objects.create(
                job_card=job_card,
                item_type=detected_item_type,
                **item_data
            )
            created_items.append(inventory_item)
            
            # Stock Update Logic
            batch_sell_pack = item_data.get('batch_sell_pack')
            # Assuming adjust_quantity is POSITIVE (quantity to take) from frontend
            # So we subtract it from stock.
            adjust_quantity = item_data.get('adjust_quantity', 0) or 0
            
            # Calculate stock reduction amount
            actual_stock_reduction = 0
            product = resolved_product 
            
            if whole_sell_pack and adjust_quantity != 0:
                actual_stock_reduction = adjust_quantity
                
            elif batch_sell_pack and adjust_quantity != 0:
                sell_pack = batch_sell_pack.sell_pack
                sell_pack_quantity = sell_pack.quantity if sell_pack and sell_pack.quantity else 1
                if not product:
                    product = sell_pack.product
                base_quantity_value = product.base_quantity_value if product and product.base_quantity_value else 1
                
                actual_stock_reduction = (adjust_quantity * sell_pack_quantity) / base_quantity_value
            
            elif unbatched_whole_pack_product and adjust_quantity != 0:
                product = unbatched_whole_pack_product
                actual_stock_reduction = adjust_quantity
                
            elif unbatched_sell_pack_obj and adjust_quantity != 0:
                product = unbatched_sell_pack_obj.product
                base_quantity_value = product.base_quantity_value if product and product.base_quantity_value else 1
                
                actual_stock_reduction = (adjust_quantity * unbatched_sell_pack_obj.quantity) / base_quantity_value

            elif item_data.get('product') and adjust_quantity != 0:
                product = item_data.get('product')
                actual_stock_reduction = adjust_quantity

            # Update Stock (Reduce)
            if product and actual_stock_reduction != 0:
                stock = None
                purchase = None
                
                # Determine purchase from batch info
                if whole_sell_pack:
                    purchase = whole_sell_pack.purchase
                elif batch_sell_pack and batch_sell_pack.batch:
                    purchase = batch_sell_pack.batch.purchase
                
                # Try to find stock specific to this purchase
                if purchase:
                    stock = Stock.objects.filter(product=product, purchase=purchase).first()
                
                # Fallback: Use general stock (FIFO or any available logic, here using oldest created)
                if not stock:
                    stock = Stock.objects.filter(product=product).order_by('created_at').first()

                if stock:
                    # Subtract from stock!
                    stock.quantity = (stock.quantity or 0) - actual_stock_reduction
                    stock.save()
                else:
                    # If stock doesn't exist, Create negative stock? Or error?
                    # Generally creating negative stock is allowed if we track it.
                    Stock.objects.create(
                        product=product,
                        quantity= -actual_stock_reduction,
                        branch=job_card.branch, 
                        purchase=purchase
                    )
        
        return job_card
