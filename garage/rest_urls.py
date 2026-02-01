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
    path("add-branch/", CreateBranch.as_view(), name="add-branch"),
    path("edit-branch/<uuid:id>/", UpdateBranch.as_view(), name="edit-branch"),

    path("delete-branch/<uuid:id>/", DeleteBranch.as_view(), name="delete-branch"),

    path("add-job-type/", CreateJobType.as_view(), name="add-job-type"),
    path("edit-job-type/<uuid:id>/", UpdateJobType.as_view(), name="edit-job-type"),
    path("delete-job-type/<uuid:id>/", DeleteJobType.as_view(), name="delete-job-type"),


    path("add-team/", CreateTeam.as_view(), name="add-team"),
    path("list-team/", ListTeam.as_view(), name="list-team"),
    path("total-income/", TotalIncome.as_view(), name="total-income"),
    path("total-expense/", TotalExpense.as_view(), name="total-expense"),
    path("list-balances/", ListBalance.as_view(), name="list-balances"),
    path("list-transactions/", List_Transactions.as_view(), name="list-transactions"),


    

    path("add-deposit/", CreateDeposit.as_view(), name="add-deposit"),
    path("create-withdrawal/", CreateWithdrawal.as_view(), name="create-withdrawal"),
    path("opening-balance/", LastDayBalanceView.as_view(), name="opening-balance"),
    path("credit-outstanding/", CreditOutstandingView.as_view(), name="credit-outstanding"),
    path("create-user/", UserCreateAPIView.as_view(), name="user-create"),
    path("update-user/<uuid:pk>/", UserEditAPIView.as_view(), name="user-edit"),
    path("list-designations/", GetDepartment.as_view(), name="get-dept"),
    path("list-role/", ListRole.as_view(), name="list-role"),
    path("list-users/", ListUsers.as_view(), name="list-users"),
    path("list-time-zones/", ListTimezones.as_view(), name="list-time-zones"),
    path("create-brand/", CreateBrand.as_view(), name="create-brand"),
    path("list-brand/", ListBrand.as_view(), name="list-brand"),
    path("create-category/", CreateCategory.as_view(), name="create-category"),
    path("list-category/", ListCategory.as_view(), name="list-category"),
    path("create-vendor/", CreateVendor.as_view(), name="create-vendor"),
    path("list-vendor/", ListVendor.as_view(), name="list-vendor"),
    path("create-product/", CreateProductView.as_view(), name="create-product"),
    path("list-product/", ProductListView.as_view(), name="list-product"),
    path('sell-pack/create/', CreateSellPack.as_view(), name='create-sell-pack'),
    path('sell-part/create/', CreateSellPart.as_view(), name='create-sell-part'),
    path('list-sell-part/', ListSellPart.as_view(), name='list-sell-part'),
    path('list-sell-pack/', ListSellPack.as_view(), name='list-sell-pack'),
    path('add-purchase/', AddPurchaseAPIView.as_view(), name='add-product'),
    path('add-purchase-items/', AddPurchaseItems.as_view(), name='add-purchase-items'),
    path('edit-purchase-items/<uuid:item_id>/', EditPurchaseItems.as_view(), name='edit-purchase-items'),
    path('list-purchase-items/', ListPurchaseItems.as_view(), name='list-purchase-items'),
    path('delete-purchase-items/<uuid:item_id>/', DeletePurchaseItem.as_view(), name='delete-purchase-items'),
    path('list-purchase/', ListPurchase.as_view(), name='list-purchase'),
    path('edit-purchase/<uuid:purchase_id>/', EditPurchase.as_view(), name='edit-purchase'),
    path('delete-purchase/<uuid:item_id>/', DeletePurchase.as_view(), name='delete-purchase'),
    path("labour/create/", LabourCreateAPIView.as_view(), name='edit-purchase'),
    path("labour/list/", LabourListAPIView.as_view(), name='edit-purchase'),
    path("labour/<uuid:id>/update/", LabourUpdateAPIView.as_view(), name='edit-purchase'),
    path("labour/<uuid:id>/delete/", LabourSoftDeleteAPIView.as_view(), name='edit-purchase'),
    path("jobcards/<uuid:jobcard_id>/quotation-pdf/",jobcard_quotation_pdf, name='job-quotation'),
    path("units/", UnitListAPIView.as_view(), name="unit-list"),
    path("delete-jobcards/<uuid:id>/", DeleteJobCard.as_view(), name="delete-jobcards"),
    path("jobcards-render/<uuid:jobcard_id>/quotation-pdf/",jobcard_quotation_preview, name='jobcard_quotation_preview'),
    path("purchase/<uuid:purchase_id>/approve/",ApprovePurchase.as_view(),name="approve-purchase"),
    path("purchase/<uuid:purchase_id>/recieve/",RecievedPurchase.as_view(),name="recieve-purchase"),
    path("purchase/<uuid:purchase_id>/complete/",CompletePurchase.as_view(),name="recieve-purchase"),
    
    # Product Batch Details API
    path("product-batch-details/<uuid:product_id>/", ProductBatchDetails.as_view(), name="product-batch-details"),
    
    # Batch CRUD with nested BatchSellPack
    path("create-batch/", CreateBatch.as_view(), name="create-batch"),
    path("update-batch/<uuid:id>/", UpdateBatch.as_view(), name="update-batch"),

    # Stock Adjustment API
    path("create-stock-adjustment/", CreateStockAdjustment.as_view(), name="create-stock-adjustment"),
    path("list-stock-adjustments/", ListStockAdjustment.as_view(), name="list-stock-adjustments"),

    # Purchase Log API
    path("list-purchase-logs/", ListPurchaseLog.as_view(), name="list-purchase-logs"),

    # SellPack APIs
    path("update-sell-pack/<uuid:id>/", UpdateSellPack.as_view(), name="update-sell-pack"),
    path("delete-sell-pack/<uuid:id>/", DeleteSellPack.as_view(), name="delete-sell-pack"),

    # SellPart APIs
    path("update-sell-part/<uuid:id>/", UpdateSellPart.as_view(), name="update-sell-part"),
    path("delete-sell-part/<uuid:id>/", DeleteSellPart.as_view(), name="delete-sell-part"),

    # Purchase Delete API
    path("delete-purchase/<uuid:id>/", DeletePurchase.as_view(), name="delete-purchase"),

]