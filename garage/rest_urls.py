from django.urls import path
from .views import *


urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="custom_login"),# login
    path("add_employee/", AddEmplpyee.as_view(), name="add_employee"),# add employee
    path("list_employee/", ListAllEmployee.as_view(), name="list_employee"),# list employee
    path("update_salary/<uuid:id>/", UpdatePayment.as_view(), name="update_salary"),#to create salary details of employees
    path("list_salary/<uuid:id>/", ListSalary.as_view(), name="list_salary"),#to list the salary details of the employee
    path("retrieve_employee/<uuid:id>/", RetrieveEmployee.as_view(), name="retrieve_employee"),#to get the details of a specify employee
    path("add_remarks/", AddRemark.as_view(), name="add_remark"),#to add remarks of an employee
    path("list_remarks/<uuid:id>/", ListRemark.as_view(), name="list-remarks"),#to list remarks of an employee
    path("add_jobcard/", AddJobcard.as_view(), name="add-jobcard"),#to add the jobcard
    path("list_jobcard/", ListJobcards.as_view(), name="list-jobcard"),#to list the jobcard
    path("retrieve_user/<uuid:id>/", RetrieveUser.as_view(), name="retrieve_user"),#to get the details of a user
    path("retrieve_jobs/<uuid:id>/", RetrieveJobs.as_view(), name="retrieve_jobs"),#to get the details of a job
    path("update_jobs/<uuid:id>/", UpdateJobsClose.as_view(), name="update_jobs"),
    path("update_normal_jobs/<uuid:id>/", UpdateJobs.as_view(), name="update_normal_jobs"),
    
    path("add_technicians/", AddTechnician.as_view(), name="add_technicians"),
    path("list_technicians/", ListTechnician.as_view(), name="list_technicians"),
    path("list_spareparts/", ListSpareparts.as_view(), name="list_spareparts"),
    path("list_issues/", ListIssues.as_view(), name="list_issues"),
    path("update_technician/<uuid:id>/", UpdateTechnician.as_view(), name="update_technician"),
    path("delete_technician/<uuid:id>/", DeleteTechniciane.as_view(), name="delete_technician"),
    path("add_spareparts/", AddSpareparts.as_view(), name="add_spareparts"),
    path("update_spareparts/<uuid:id>/", UpdateSpareparts.as_view(), name="update_spareparts"),
    path("delete_spareparts/<uuid:id>/", DeleteSpareparts.as_view(), name="delete_spareparts"),
    path("add_issues/", AddIssues.as_view(), name="add_issues"),
    path("update_issues/<uuid:id>/", UpdateIssues.as_view(), name="update_issues"),
    path("delete_issues/<uuid:id>/", DeleteIssues.as_view(), name="delete_issues"),
    path("list-branch/", ListBranch.as_view(), name="list-branch"),
    path("list-job-types/", ListJobType.as_view(), name="list-job-types"),
    path("spare-amount/", SpareAmount.as_view(), name="spare-amount"),
    path("list-other-expense/", ListOtherExpense.as_view(), name="list-other-expense"),
    path("total-expense/", TotalExpense.as_view(), name="total-expense"),
    path("add-other-expense/", AddOtherExpense.as_view(), name="add-other-expense"),
    path("list-customers/", ListCustomers.as_view(), name="list-customers"),
    path("add-customers/", AddCustomers.as_view(), name="add-customers"),
    path("edit-customers/<uuid:id>/", UpdateCustomer.as_view(), name="add-customers"),
    path("delete-customers/<uuid:id>/", DeleteCustomer.as_view(), name="add-customers"),
    path("add-expense/", AddExpense.as_view(), name="add-expense"),
    path("edit-expense/<uuid:id>/", UpdateExpense.as_view(), name="update-expense"),
    path("list-expense/", ListExpense.as_view(), name="list-expense"),
    path("delete-expense/<uuid:id>/", DeleteExpense.as_view(), name="delete-expense"),
    path("add-income/", AddIncome.as_view(), name="add-income"),
    path("list-income/", ListIncome.as_view(), name="list-income"),
    path("update-income/<uuid:id>/", UpdateIncome.as_view(), name="update-income"),
    path("delete-income/<uuid:id>/", DeleteIncome.as_view(), name="delete-income"),
    path("list-advance-payment/", ListAdvance_amount.as_view(), name="list-advance-payment"),
    path("add-advance-payment/", AddAdvance_amount.as_view(), name="add-advance-payment"),
    path("delete-advance-payment/<uuid:id>/", DeleteAdvance_amount.as_view(), name="delete-advance-payment"),
    path("dashboard-data/", DashboardDatas.as_view(), name="dashboard-datas"),
































    


    
    

]