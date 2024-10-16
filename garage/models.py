from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from MsOne.models import TimestampedUUIDModel


class User(AbstractUser, TimestampedUUIDModel):

    user_img = models.ImageField(upload_to="users", null=True, blank=True)
    role = models.CharField(max_length=100, null=True, blank=True)
    branch = models.CharField(max_length=100, null=True, blank=True)
    passport_nmbr = models.CharField(max_length=100, null=True, blank=True)
    visa_type = models.CharField(max_length=100, null=True, blank=True)
    visa_expiry = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    phone_personal = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)

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
    branch = models.CharField(max_length=100,choices=branch_choices, null=True, blank=True)
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


class Remarks(TimestampedUUIDModel):

    remarks = models.TextField(null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

class Branch(TimestampedUUIDModel):
    name = models.CharField(max_length=200,null=True,blank=True)

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

class JobType(TimestampedUUIDModel):
    name = models.CharField(max_length=200,null=True,blank=False)

class JobCard(TimestampedUUIDModel):
    IN_PROGRESS = "In progress"
    CLOSED = "Closed"
    CREDIT = "Credit"
    status_choices = ((CLOSED, CLOSED), (CREDIT, CREDIT), (IN_PROGRESS, IN_PROGRESS))
    CASH = "Cash"
    CREDIT = "Credit"
    bill_choice = ((CASH,CASH),(CREDIT,CREDIT))
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
    job_type = models.ManyToManyField(JobType)
    bill_type = models.CharField(max_length=200,choices=bill_choice,null=True)
    advance_payment = models.FloatField(null=True,blank=True)

class BillAmount(TimestampedUUIDModel):
    job_type = models.ForeignKey(JobType,on_delete=models.SET_NULL,null=True)
    amount = models.FloatField(null=True,blank=True)
    job_card = models.ForeignKey(JobCard, on_delete=models.CASCADE)


class Technician(TimestampedUUIDModel):

    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    labour_charge = models.FloatField(default=0)
    job_card = models.ForeignKey(JobCard, on_delete=models.CASCADE)


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