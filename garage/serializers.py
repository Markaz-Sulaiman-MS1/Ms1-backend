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
        )["amount__sum"]
        
        if status == "Closed":

            Income.objects.create(
                type="Job",
                total_income=total_amount,
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
                    'cash_balance': total_amount,
                }
                )
            
                if not created:
                    balance.cash_balance += total_amount
                    balance.save()
                if instance.bill_type == JobCard.CASH:
                    RecentTransaction.objects.create(
                            transaction_type=RecentTransaction.INCOME,
                            description = "Job card income transferred as cash",
                            payment_type = instance.payment_type,
                            amount = total_amount,
                            balance_cash = balance.cash_balance,
                            balance_bank = balance.bank_balance,
                            branch_id=instance.branch.id
                    )
                else:
                    RecentTransaction.objects.create(
                            transaction_type=RecentTransaction.INCOME,
                            description = "Job card income closed as cashed credit",
                            payment_type = instance.payment_type,
                            amount = total_amount,
                            balance_cash = balance.cash_balance,
                            balance_bank = balance.bank_balance,
                            branch_id=instance.branch.id
                    )
                

            else:
                balance, created = Balance.objects.get_or_create(
                branch_id=instance.branch.id,
                defaults={
                    'bank_balance': total_amount,
                }
                )
            
                if not created:
                    balance.bank_balance += total_amount
                    balance.save()

                if instance.bill_type == JobCard.CASH:
                    RecentTransaction.objects.create(
                            transaction_type=RecentTransaction.INCOME,
                            description = "Job card income transferred to bank",
                            payment_type = instance.payment_type,
                            amount = total_amount,
                            balance_cash = balance.cash_balance,
                            balance_bank = balance.bank_balance,
                            branch_id=instance.branch.id
                    )
                else:
                    RecentTransaction.objects.create(
                            transaction_type=RecentTransaction.INCOME,
                            description = "Job card income closed as banked credit",
                            payment_type = instance.payment_type,
                            amount = total_amount,
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
            "job_card_doc"
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
            "brand", "cost_price", "base_quantity", "category", "selling_price",
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
            "brand", "cost_price", "base_quantity", "category", "selling_price",
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
        read_only_fields = ["id"]

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
    """Serializer for creating StockAdjustmentItem without stock_adjustment reference"""
    class Meta:
        model = StockAdjustmentItem
        fields = ["product", "current_quantity", "adjust_quantity", "rate", "rate_adjustment", "amount"]


class CreateStockAdjustmentSerializer(serializers.ModelSerializer):
    """
    Serializer for creating StockAdjustment with nested StockAdjustmentItems.
    Handles:
    1. Creating StockAdjustment and nested items
    2. Updating stock quantities based on adjust_quantity
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
            # Create the adjustment item
            adjustment_item = StockAdjustmentItem.objects.create(
                stock_adjustment=stock_adjustment,
                **item_data
            )
            
            # Calculate total amount for financial transactions
            if adjustment_item.amount:
                total_amount += float(adjustment_item.amount)
            
            # Update stock quantity for the product
            product = item_data.get('product')
            adjust_quantity = item_data.get('adjust_quantity', 0) or 0
            
            if product and adjust_quantity != 0:
                # Get or create stock for this product
                stock = Stock.objects.filter(product=product).first()
                if stock:
                    # Update existing stock quantity
                    stock.quantity = (stock.quantity or 0) + adjust_quantity
                    stock.save()
                else:
                    # Create new stock record if doesn't exist
                    Stock.objects.create(
                        product=product,
                        quantity=adjust_quantity
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
        batch_stock = self.context.get('batch_stock', 0) or 0
        sell_pack_quantity = obj.sell_pack.quantity if obj.sell_pack and obj.sell_pack.quantity else 1
        
        if sell_pack_quantity > 0:
            return int(batch_stock // sell_pack_quantity)
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
                return stock.quantity or 0
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
            "brand", "cost_price", "category", "selling_price",
            "stock_reorder_level", "description", "batches"
        ]

    def get_batches(self, obj):
        batches = Batch.objects.filter(product=obj, is_deleted=False)
        return BatchDetailSerializer(batches, many=True).data