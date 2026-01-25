from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
        (
            None,
            {
                "fields": (
                    "id",
                    "user_img",
                    "role",
                    "branch",
                    "passport_nmbr",
                    "visa_type",
                    "visa_expiry",
                    "address",
                    "country",
                    "state",
                    "phone_personal",
                    "account",
                    "team",
                    "designation"
                )
            },
        ),
    )

class EmployeeAdmin(admin.ModelAdmin):
     list_display = (
         'id',
         'emp_name',
         'created_at',
         'updated_at',
         'role',
         'branch',

     )

class RemarksAdmin(admin.ModelAdmin):
     list_display = (
         'id',
         'remarks',
         'employee',


     )

class JobcardAdmin(admin.ModelAdmin):
     list_display = (
         'id',
         'email',

     )
class TechnicianAdmin(admin.ModelAdmin):
     list_display = (
         'id',
         'employee',
         'labour_charge',
         'job_card',

     )
class BranchAdmin(admin.ModelAdmin):
     list_display = (
         'id',
         'name',

     )

class CustomerAdmin(admin.ModelAdmin):
     list_display = (
         'id',
         'name',
         'customer_type',

     )

class JobTypeAdmin(admin.ModelAdmin):
     list_display = (
         'id',
         'name',
     )

class BillAmountAdmin(admin.ModelAdmin):
     list_display = (
         'id',
         'amount',
         'job_card',
         'created_at'
     )

class ContactPersonAdmin(admin.ModelAdmin):
     list_display = (
         'id',
         'created_at',
     )

class ExpenseAdmin(admin.ModelAdmin):
     list_display = (
         'id',
         'created_at',
     )

class Advance_amountAdmin(admin.ModelAdmin):
     list_display = (
         'id',
         'created_at',
     )

class AccountAdmin(admin.ModelAdmin):
     list_display = (
         'id',
         'created_at',
     )

class TeamAdmin(admin.ModelAdmin):
     list_display = (
         'id',
         'created_at',
     )




class InvoiceAdmin(admin.ModelAdmin):
     list_display = (
         'id',
         'created_at',
     )


class RecentTransactionAdmin(admin.ModelAdmin):
     list_display = (
         'id',
         'created_at',
     )

class BalanceAdmin(admin.ModelAdmin):
     list_display = (
         'id',
         'created_at',
     )

class DesignationAdmin(admin.ModelAdmin):
     list_display = (
         'id',
         'created_at',
     )


class RoleAdmin(admin.ModelAdmin):
     list_display = (
         'id',
         'created_at',
     )


class TimeZoneAdmin(admin.ModelAdmin):
     list_display = (
         'id',
         'name',
         'created_at',
     )


class BrandAdmin(admin.ModelAdmin):
     list_display = (
         'id',
         'name',
         'created_at',
     )

class CategoryAdmin(admin.ModelAdmin):
     list_display = (
         'id',
         'name',
         'created_at',
     )
class UnitsAdmin(admin.ModelAdmin):
     list_display = (
         'id',
         'name',
         'created_at',
     )
class VendorAdmin(admin.ModelAdmin):
     list_display = (
         'id',
        'name',
        'created_at',
     )


class ProductAdmin(admin.ModelAdmin):
     list_display = (
         'id',
         'created_at',
     )


class SellPackAdmin(admin.ModelAdmin):
     list_display = (
         'id',
         'name',
         'created_at',
     )

class SellPartAdmin(admin.ModelAdmin):
     list_display = (
         'id',
         'name',
         'created_at',
     )

class PurchaseAdmin(admin.ModelAdmin):
          list_display = (
         'id',
         'po_nmbr',
         'created_at',
     )
     

class ProductItemAdmin(admin.ModelAdmin):
          list_display = (
         'id',
         'purchase',
         'created_at',
     )
     

class LabourAdmin(admin.ModelAdmin):
          list_display = (
         'id',
     )
     


class PurchaseLogAdmin(admin.ModelAdmin):
          list_display = (
         'id',
         'purchase'
     )


admin.site.register(User, MyUserAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Remarks, RemarksAdmin)
admin.site.register(JobCard, JobcardAdmin)
admin.site.register(Technician, TechnicianAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(JobType, JobTypeAdmin)
admin.site.register(BillAmount, BillAmountAdmin)
admin.site.register(ContactPerson, ContactPersonAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Advance_amount, Advance_amountAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Income, InvoiceAdmin)
admin.site.register(RecentTransaction, RecentTransactionAdmin)
admin.site.register(Balance, BalanceAdmin)
admin.site.register(Designation, DesignationAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(TimeZone, TimeZoneAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Units, UnitsAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(SellPack, SellPackAdmin)
admin.site.register(SellPart, SellPartAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(ProductItem, ProductItemAdmin)
admin.site.register(Labour, LabourAdmin)
admin.site.register(PurchaseLog, PurchaseLogAdmin)





















