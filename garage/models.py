from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from MsOne.models import TimestampedUUIDModel
from django.db.models import Max



class Account(TimestampedUUIDModel):
    company = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.company
    
class TimeZone(TimestampedUUIDModel):
    name=models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.name

class Branch(TimestampedUUIDModel):
    name = models.CharField(max_length=200,null=True,blank=True)
    address = models.TextField(max_length=500,null=True,blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)      
    town = models.CharField(max_length=100, null=True, blank=True)
    landmark = models.CharField(max_length=100, null=True, blank=True)
    zip_code = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    account = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    timezone = models.ForeignKey(TimeZone,on_delete=models.SET_NULL,null=True)

    
    def __str__(self):
        return f"{self.name} {self.account.company}"

class Team(TimestampedUUIDModel):
    name = models.CharField(max_length=200,null=True,blank=True)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE,null=True)


class Role(TimestampedUUIDModel):
    name=models.CharField(max_length=200,null=True,blank=True)
    
    def __str__(self):
        return self.name


class Designation(TimestampedUUIDModel):
    title = models.CharField(max_length=200,null=True,blank=True)
    role = models.ForeignKey(Role,on_delete=models.SET_NULL,null=True)
    account = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)

    
    def __str__(self):
        return self.title



class User(AbstractUser, TimestampedUUIDModel):

    user_img = models.ImageField(upload_to="users", null=True, blank=True)
    branch = models.CharField(max_length=100, null=True, blank=True)
    role = models.ForeignKey(Role,on_delete=models.SET_NULL,null=True)
    passport_nmbr = models.CharField(max_length=100, null=True, blank=True)
    visa_type = models.CharField(max_length=100, null=True, blank=True)
    visa_expiry = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    phone_personal = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    account = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,null=True,blank=True)
    team = models.ForeignKey(Team,on_delete=models.SET_NULL,null=True,blank=True)
    designation = models.ForeignKey(Designation,on_delete=models.SET_NULL,null=True,blank=True)
    date_of_joining = models.DateField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    town = models.CharField(max_length=100, null=True, blank=True)
    zip_code = models.CharField(max_length=100, null=True, blank=True)
    net_payable_salary = models.FloatField(null=True,blank=True)
    other_expense = models.FloatField(null=True,blank=True)



    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        unique_together = ("email", "username")


class Employee(TimestampedUUIDModel):
    RIYADH = 'Riyadh'
    JEDDAH = 'Jeddah'
    branch_choices = ((RIYADH,RIYADH),(JEDDAH,JEDDAH))
    PROFESSIONALVISA = 'Professional_visa'
    DRIVER_VISA = 'Driver_visa'
    NOTSPONSOREDVISA = 'Not_sponsored_visa'
    visa_choices = ((PROFESSIONALVISA,PROFESSIONALVISA),(DRIVER_VISA,DRIVER_VISA),(NOTSPONSOREDVISA,NOTSPONSOREDVISA))
    emp_name = models.CharField(max_length=100, null=True, blank=True)
    emp_img = models.ImageField(upload_to="employees", null=True, blank=True)
    role = models.CharField(max_length=100, null=True, blank=True)
    passport_nmbr = models.CharField(max_length=100, null=True, blank=True)
    visa_type = models.CharField(max_length=100, null=True,choices=visa_choices, blank=True)
    visa_expiry = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    phone_personal = models.CharField(max_length=100, null=True, blank=True)
    emp_email = models.EmailField(null=True, blank=True)
    town = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    zipcode = models.CharField(max_length=100, null=True, blank=True)
    net_payable_salary = models.FloatField(null=True, blank=True)
    other_expense = models.FloatField(null=True, blank=True)
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,null=True)

class Remarks(TimestampedUUIDModel):

    remarks = models.TextField(null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)



class Customer(TimestampedUUIDModel):
    INDIVIDUAL = "Individual"
    COMPANY = "Company"
    customer_type_choices = ((INDIVIDUAL, INDIVIDUAL), (COMPANY, COMPANY))
    name = models.CharField(max_length=200,null=True,blank=True)
    customer_type = models.CharField(
        max_length=100, choices=customer_type_choices, null=True, blank=True
    )
    prefered_currency = models.CharField(max_length=100, null=True, blank=True)
    permanent_address = models.TextField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    town = models.CharField(max_length=100, null=True, blank=True)
    phn_nmbr = models.CharField(max_length=100, null=True, blank=True)
    whatsapp = models.CharField(max_length=100, null=True, blank=True)
    landmark = models.CharField(max_length=100, null=True, blank=True)
    zip_code = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    account = models.ForeignKey(Account,on_delete=models.SET_NULL,null=True)
class JobType(TimestampedUUIDModel):
    name = models.CharField(max_length=200,null=True,blank=False)
    account = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)

    
    def __str__(self):
        return self.name
    



class Labour(TimestampedUUIDModel):
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField( null=True, blank=True)
    code = models.CharField(max_length=200, null=True, blank=True)
    rate = models.FloatField(null=True, blank=True)
    job_type = models.ForeignKey(JobType,on_delete=models.SET_NULL,null=True)
    account = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    is_deleted = models.BooleanField(default=False, null=True, blank=True)

class JobCard(TimestampedUUIDModel):
    IN_PROGRESS = "In progress"
    CLOSED = "Closed"
    CREDIT = "Credit"
    DRAFT = "Draft"
    status_choices = ((CLOSED, CLOSED), (CREDIT, CREDIT), (IN_PROGRESS, IN_PROGRESS),(DRAFT,DRAFT))
    CASH = "Cash"
    CREDIT = "Credit"
    BANK = "Bank"
    bill_choice = ((CASH,CASH),(CREDIT,CREDIT))
    payment_choice = ((CASH,CASH),(BANK,BANK))
    vehicle_nmbr = models.CharField(max_length=100, null=True, blank=True)
    phn_nmbr = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    vehicle_type = models.CharField(max_length=100, null=True, blank=True)
    model = models.CharField(max_length=100, null=True, blank=True)
    fuel_type = models.CharField(max_length=100, null=True, blank=True)
    engine_hour_info = models.IntegerField(null=True, blank=True)
    status = models.CharField(
        max_length=100, choices=status_choices, null=True, blank=True
    )
    remarks = models.CharField(max_length=200, null=True, blank=True)
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,null=True)
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    make_and_model = models.CharField(max_length=200,null=True,blank=True)
    job_type = models.ManyToManyField(JobType,blank=True)
    labour = models.ManyToManyField(Labour,blank=True)

    bill_type = models.CharField(max_length=200,choices=bill_choice,null=True)
    advance_payment = models.FloatField(null=True,blank=True)
    average_daily_usage = models.IntegerField(null=True, blank=True)
    next_service_hour = models.IntegerField(null=True, blank=True)
    next_service_date = models.DateField(null=True, blank=True)
    payment_type = models.CharField(max_length=200,choices=payment_choice,null=True)
    job_card_doc = models.FileField(upload_to="job_cards/",null=True,blank=True)
    payment_due_date = models.DateField(null=True, blank=True)
    delivery_due_date = models.DateField(null=True, blank=True)

class BillAmount(TimestampedUUIDModel):
    job_type = models.ForeignKey(JobType,on_delete=models.SET_NULL,null=True)
    amount = models.FloatField(null=True,blank=True)
    job_card = models.ForeignKey(JobCard, on_delete=models.CASCADE)


class Technician(TimestampedUUIDModel):

    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    labour_charge = models.FloatField(default=0)
    job_card = models.ForeignKey(JobCard, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Issues(TimestampedUUIDModel):

    heading = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    job_card = models.ForeignKey(JobCard, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False, null=True, blank=True)


class SpareParts(TimestampedUUIDModel):
    NEW = "New"
    USED = "Used"
    category_choices = ((NEW,NEW),(USED,USED))
    name = models.CharField(max_length=200, null=True, blank=True)
    category = models.CharField(max_length=200,choices=category_choices,null=True, blank=True)
    cost = models.FloatField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    job_type = models.ForeignKey(JobType,on_delete=models.SET_NULL,null=True)
    job_card = models.ForeignKey(JobCard, on_delete=models.CASCADE)

class OtherExpense(TimestampedUUIDModel):
    name = models.CharField(max_length=200, null=True, blank=True)
    job_type = models.ForeignKey(JobType,on_delete=models.SET_NULL,null=True)
    job_card = models.ForeignKey(JobCard, on_delete=models.CASCADE)
    amount = models.FloatField(null=True,blank=True)

class ContactPerson(TimestampedUUIDModel):
    name = models.CharField(max_length=200, null=True, blank=True)
    designation = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(null=True,blank=True)
    phone_nmbr = models.CharField(max_length=100, null=True, blank=True)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='contact_persons')


class Expense(TimestampedUUIDModel):
    JOB = "Job"
    SALARY = "Salary"
    OTHER = "Other"
    PURCHASE = "Purchase"
    OVERTIME = "Over Time"
    CASH = "Cash"
    BANK = "Bank"
    payment_choice = ((CASH,CASH),(BANK,BANK))
    type_choices = ((JOB,JOB),(SALARY,SALARY),(OTHER,OTHER))
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    total_cost = models.FloatField(null=True,blank=True)
    date = models.DateField(null=True, blank=True)
    type = models.CharField(max_length=200,choices=type_choices,null=True, blank=True)
    salary = models.FloatField(null=True,blank=True)
    other_expense = models.FloatField(null=True,blank=True,default=0.0)
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,null=True)
    payment_type = models.CharField(max_length=200,choices=payment_choice,null=True)


    

class Income(TimestampedUUIDModel):
    JOB = "Job"
    OTHER = "Other"
    SPAREPARTS = "SpareParts"
    CASH = "Cash"
    BANK = "Bank"
    payment_choice = ((CASH,CASH),(BANK,BANK))
    type_choices = ((JOB,JOB),(OTHER,OTHER),(SPAREPARTS,SPAREPARTS))
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    total_income = models.FloatField(null=True,blank=True)
    date = models.DateField(null=True, blank=True)
    job_card = models.OneToOneField(JobCard, on_delete=models.CASCADE,null=True,blank=True)
    type = models.CharField(max_length=200,choices=type_choices,null=True, blank=True)
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,null=True)
    payment_type = models.CharField(max_length=200,choices=payment_choice,null=True)



class Advance_amount(TimestampedUUIDModel):
    amount = models.FloatField(null=True,blank=True)                          
    job_card = models.ForeignKey(JobCard, on_delete=models.CASCADE)                  


class Balance(TimestampedUUIDModel):
    cash_balance =  models.FloatField(null=True,blank=True,default=0)
    bank_balance = models.FloatField(null=True,blank=True,default=0)
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,null=True)

    

class RecentTransaction(TimestampedUUIDModel):
    CASH = "Cash"
    BANK = "Bank"
    INCOME = "Income"
    EXPENSE = "Expense"
    DEPOSIT = "Deposit"
    WITHDRAWAL = "Withdrawal"
    payment_choice = ((CASH,CASH),(BANK,BANK))
    type_choice = ((INCOME,INCOME),(EXPENSE,EXPENSE),(DEPOSIT,DEPOSIT),(WITHDRAWAL,WITHDRAWAL))

    date = models.DateField(null=True, blank=True)
    transaction_type =  models.CharField(max_length=100, null=True,choices=type_choice)
    description = models.TextField(null=True, blank=True)
    payment_type = models.CharField(max_length=200,choices=payment_choice,null=True)
    amount = models.FloatField(null=True,blank=True)
    balance_cash =  models.FloatField(null=True,blank=True)
    balance_bank =  models.FloatField(null=True,blank=True)
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,null=True)


class Brand(TimestampedUUIDModel):
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    account = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)



class Category(TimestampedUUIDModel):
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    account = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)

class Units(TimestampedUUIDModel):
    name=models.CharField(max_length=200, null=True, blank=True)

class Vendor(TimestampedUUIDModel):
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    address=models.TextField(null=True, blank=True)
    account = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    

class Product(TimestampedUUIDModel):
    NEW = "New"
    USED = "Used"
    type_choice = ((NEW,NEW),(USED,USED))
    product_img = models.ImageField(upload_to="products", null=True, blank=True)
    product_code = models.CharField(max_length=200, null=True, blank=True)
    product_name = models.CharField(max_length=200, null=True, blank=True)
    condition_type = models.CharField(max_length=200,choices=type_choice,null=True)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE,null=True)
    cost_price = models.FloatField(null=True,blank=True)
    base_quantity = models.ForeignKey(Units,on_delete=models.SET_NULL,null=True,blank=True)
    base_quantity_value = models.FloatField(null=True, blank=True)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True)
    selling_price = models.FloatField(null=True,blank=True)
    stock_reorder_level  = models.IntegerField(null=True,blank=True)
    description = models.TextField(null=True, blank=True)
    account = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)


class SellPack(TimestampedUUIDModel):
    name = models.CharField(max_length=200, null=True, blank=True)
    product_code = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.FloatField(null=True,blank=True)
    no_of_pieces = models.IntegerField(null=True,blank=True)
    cost_price = models.FloatField(null=True,blank=True)
    selling_price = models.FloatField(null=True,blank=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)


class SellPart(TimestampedUUIDModel):
    name = models.CharField(max_length=200, null=True, blank=True)
    product_code = models.CharField(max_length=200, null=True, blank=True)
    no_of_pieces = models.IntegerField(null=True,blank=True)
    cost_price = models.FloatField(null=True,blank=True)
    selling_price = models.FloatField(null=True,blank=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)


class Purchase(TimestampedUUIDModel):
    DRAFT = "Draft"
    INPROGRESS = "In Progress"
    APPROVED = "Approved"
    RECEIVED = "Received"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    type_choice = ((DRAFT,DRAFT),(INPROGRESS,INPROGRESS),(RECEIVED,RECEIVED),(COMPLETED,COMPLETED),(CANCELLED,CANCELLED),(APPROVED,APPROVED))
    po_nmbr = models.CharField(max_length=200, unique=True, blank=True)
    vendor = models.ForeignKey(Vendor,on_delete=models.SET_NULL,null=True,blank=True)
    exp_date_delivery = models.DateField(null=True, blank=True)
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,null=True)
    description = models.TextField(null=True, blank=True)
    purchase_type = models.CharField(max_length=200,choices=type_choice,default=DRAFT,null=True,blank=True)
    is_deleted = models.BooleanField(default=False, null=True, blank=True)
    account = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    discount = models.FloatField(null=True,blank=True)
    tax = models.FloatField(null=True,blank=True)
    total_amount = models.FloatField(null=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.po_nmbr:
            last_po = Purchase.objects.aggregate(max_po=Max('po_nmbr'))['max_po']
            
            if last_po:
                # Extract number from MS001 → 1, MS245 → 245
                last_number = int(last_po.replace("MS", ""))
                new_number = last_number + 1
            else:
                new_number = 1

            self.po_nmbr = f"MS{new_number:03d}"   # Formats like MS001, MS002

        super().save(*args, **kwargs)

class ProductItem(TimestampedUUIDModel):
    quantity = models.IntegerField(null=True,blank=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    amount = models.FloatField(null=True,blank=True)
    purchase = models.ForeignKey(Purchase,on_delete=models.CASCADE,null=True)
    is_deleted = models.BooleanField(default=False, null=True, blank=True)


class Batch(TimestampedUUIDModel):
    batch_code = models.CharField(max_length=200, null=True, blank=True)
    product_code = models.CharField(max_length=200, null=True, blank=True)
    manufacture_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    cost_price = models.FloatField(null=True,blank=True)
    sell_price = models.FloatField(null=True,blank=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    is_deleted = models.BooleanField(default=False, null=True, blank=True)
    purchase = models.ForeignKey(Purchase,on_delete=models.CASCADE,null=True)


class PurchaseLog(TimestampedUUIDModel):
    DRAFT = "Draft"
    INPROGRESS = "In Progress"
    APPROVED = "Approved"
    RECEIVED = "Received"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    type_choice = ((DRAFT,DRAFT),(INPROGRESS,INPROGRESS),(RECEIVED,RECEIVED),(COMPLETED,COMPLETED),(CANCELLED,CANCELLED),(APPROVED,APPROVED))
    purchase = models.ForeignKey(Purchase,on_delete=models.CASCADE,null=True)
    created_by = models.CharField(max_length=200, null=True, blank=True)
    status=models.CharField(max_length=200,choices=type_choice,default=DRAFT,null=True,blank=True)


class Stock(TimestampedUUIDModel):

    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    purchase = models.ForeignKey(Purchase,on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.FloatField(null=True,blank=True)


class StockAdjustment(TimestampedUUIDModel):
    CASH = "Cash"
    BANK = "Bank"
    payment_choice = ((CASH, CASH), (BANK, BANK))
    
    IGNORE = "Ignore"
    INCOME = "Income"
    EXPENSE = "Expense"
    adjustment_choice = ((IGNORE, IGNORE), (INCOME, INCOME), (EXPENSE, EXPENSE))
    
    adjustment_number = models.CharField(max_length=200, unique=True, blank=True)
    adjusted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    reason_for_adjustment = models.TextField(null=True, blank=True)
    payment_type = models.CharField(max_length=200, choices=payment_choice, null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)
    adjustment_impact = models.CharField(max_length=200, choices=adjustment_choice, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.adjustment_number:
            last_adjustment = StockAdjustment.objects.aggregate(max_adj=Max('adjustment_number'))['max_adj']
            
            if last_adjustment:
                # Extract number from SA001 → 1, SA245 → 245
                last_number = int(last_adjustment.replace("SA", ""))
                new_number = last_number + 1
            else:
                new_number = 1

            self.adjustment_number = f"SA{new_number:03d}"   # Formats like SA001, SA002

        super().save(*args, **kwargs)

    def __str__(self):
        return self.adjustment_number


class StockAdjustmentItem(TimestampedUUIDModel):
    """Child table to store multiple product adjustments per StockAdjustment"""
    stock_adjustment = models.ForeignKey(StockAdjustment, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    current_quantity = models.FloatField(null=True, blank=True)
    adjust_quantity = models.FloatField(null=True, blank=True)
    rate = models.FloatField(null=True, blank=True)
    rate_adjustment = models.FloatField(null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.stock_adjustment.adjustment_number} - {self.product.product_name if self.product else 'No Product'}"



class  BatchSellPack(TimestampedUUIDModel):
    batch = models.ForeignKey(Batch,on_delete=models.CASCADE,null=True)
    sell_pack = models.ForeignKey(SellPack,on_delete=models.CASCADE,null=True)
    sell_price = models.FloatField(null=True,blank=True)
    cost_price = models.FloatField(null=True,blank=True)
    