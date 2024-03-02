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
         'customer_name',
         'customer_type',
         'email',

     )

admin.site.register(User, MyUserAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Remarks, RemarksAdmin)
admin.site.register(JobCard, JobcardAdmin)



