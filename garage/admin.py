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
     )

class ContactPersonAdmin(admin.ModelAdmin):
     list_display = (
         'id',
         'created_at',
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









